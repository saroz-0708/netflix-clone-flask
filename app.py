from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# 🔹 AUTO CREATE DATABASE ON FIRST RUN (IMPORTANT FOR RENDER)
if not os.path.exists("database.db"):
    import init_db

app = Flask(__name__)
app.secret_key = "netflix_secret"


# ---------- DATABASE HELPERS ----------
def get_db():
    return sqlite3.connect("database.db")


def get_db_row_factory():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


# ---------- AUTH ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        db.close()

        if user and check_password_hash(user[3], password):
            session["user"] = user[1]
            session["user_id"] = user[0]
            return redirect("/home")

        return "Invalid Login. <a href='/'>Try again</a>"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO users VALUES (NULL,?,?,?)",
                (name, email, password),
            )
            db.commit()
            db.close()
            return redirect("/")
        except sqlite3.IntegrityError:
            db.close()
            return "Email already exists. <a href='/register'>Try another</a>"

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------- HOME ----------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM movies ORDER BY rating DESC LIMIT 50")
    movies = cur.fetchall()

    cur.execute("""
        SELECT m.* FROM movies m
        JOIN watch_history wh ON m.id = wh.movie_id
        WHERE wh.user_id = ?
        ORDER BY wh.watched_at DESC
        LIMIT 10
    """, (session["user_id"],))
    continue_watching = cur.fetchall()

    db.close()
    return render_template(
        "home.html",
        movies=movies,
        continue_watching=continue_watching
    )


# ---------- MOVIE ----------
@app.route("/movie/<int:id>")
def movie(id):
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM movies WHERE id=?", (id,))
    movie = cur.fetchone()
    if not movie:
        db.close()
        return "Movie not found", 404

    cur.execute(
        "SELECT id FROM watchlist WHERE user_id=? AND movie_id=?",
        (session["user_id"], id)
    )
    in_watchlist = cur.fetchone() is not None

    cur.execute(
        "SELECT rating, review FROM user_ratings WHERE user_id=? AND movie_id=?",
        (session["user_id"], id)
    )
    user_rating = cur.fetchone()

    cur.execute(
        "SELECT AVG(rating) FROM user_ratings WHERE movie_id=?",
        (id,)
    )
    avg = cur.fetchone()
    user_avg_rating = avg[0] if avg and avg[0] else None

    db.close()

    return render_template(
        "movie.html",
        movie=movie,
        in_watchlist=in_watchlist,
        user_rating=user_rating,
        user_avg_rating=user_avg_rating
    )


# ---------- SEARCH ----------
@app.route("/search")
def search():
    if "user" not in session:
        return redirect("/")

    query = request.args.get("q", "").strip()

    db = get_db()
    cur = db.cursor()

    if query:
        cur.execute("""
            SELECT * FROM movies
            WHERE title LIKE ? OR genre LIKE ? OR description LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    else:
        cur.execute("SELECT * FROM movies")

    movies = cur.fetchall()
    db.close()

    return render_template("search.html", movies=movies, query=query)


# ---------- PROFILE ----------
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT m.* FROM movies m
        JOIN watchlist w ON m.id = w.movie_id
        WHERE w.user_id=?
        ORDER BY w.date_added DESC
    """, (session["user_id"],))
    watchlist = cur.fetchall()

    db.close()
    return render_template(
        "profile.html",
        username=session["user"],
        watchlist=watchlist
    )


# ---------- WATCHLIST ----------
@app.route("/watchlist")
def watchlist():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT m.* FROM movies m
        JOIN watchlist w ON m.id = w.movie_id
        WHERE w.user_id=?
        ORDER BY w.date_added DESC
    """, (session["user_id"],))
    movies = cur.fetchall()

    db.close()
    return render_template("watchlist.html", movies=movies)


# ---------- API ----------
@app.route("/api/watchlist/add/<int:movie_id>", methods=["POST"])
def add_to_watchlist(movie_id):
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "INSERT INTO watchlist (user_id, movie_id) VALUES (?, ?)",
            (session["user_id"], movie_id)
        )
        db.commit()
        db.close()
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({"error": "Already added"}), 400


@app.route("/api/watchlist/remove/<int:movie_id>", methods=["POST"])
def remove_from_watchlist(movie_id):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "DELETE FROM watchlist WHERE user_id=? AND movie_id=?",
        (session["user_id"], movie_id)
    )
    db.commit()
    db.close()
    return jsonify({"success": True})


@app.route("/api/watch-history/add/<int:movie_id>", methods=["POST"])
def add_to_watch_history(movie_id):
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    progress = data.get("progress", 0)

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO watch_history (user_id, movie_id, progress_minutes)
            VALUES (?, ?, ?)
        """, (session["user_id"], movie_id, progress))
        db.commit()
    except:
        cur.execute("""
            UPDATE watch_history
            SET watched_at=CURRENT_TIMESTAMP, progress_minutes=?
            WHERE user_id=? AND movie_id=?
        """, (progress, session["user_id"], movie_id))
        db.commit()

    db.close()
    return jsonify({"success": True})


@app.route("/api/rating/add/<int:movie_id>", methods=["POST"])
def add_rating(movie_id):
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    rating = data.get("rating")
    review = data.get("review", "")

    if not rating or rating < 1 or rating > 10:
        return jsonify({"error": "Invalid rating"}), 400

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO user_ratings (user_id, movie_id, rating, review)
            VALUES (?, ?, ?, ?)
        """, (session["user_id"], movie_id, rating, review))
        db.commit()
    except sqlite3.IntegrityError:
        cur.execute("""
            UPDATE user_ratings
            SET rating=?, review=?
            WHERE user_id=? AND movie_id=?
        """, (rating, review, session["user_id"], movie_id))
        db.commit()

    db.close()
    return jsonify({"success": True})


# ---------- RUN ----------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)