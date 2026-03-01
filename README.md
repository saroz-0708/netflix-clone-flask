# Netflix Clone App

A Flask-based Netflix clone application with user authentication, watchlist management, and movie ratings.

## Features

- User registration and login
- Movie browsing and search
- Watchlist management
- Watch history tracking
- Movie ratings and reviews
- Continue watching functionality

## Setup & Installation

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirement.txt
```

2. **Initialize the database:**
```bash
python init_db.py
```

3. **Run the application:**
```bash
python app.py
```

The app will start on `http://localhost:5000`

### Environment Variables

Create a `.env` file (or set these in your deployment environment):

```
PORT=5000
SECRET_KEY=your_unique_secret_key_here
FLASK_ENV=production
```

## Deployment on Railway

1. **Push your code to GitHub**

2. **Create a Railway project and connect your GitHub repo**

3. **Set environment variables in Railway:**
   - Go to Variables in your Railway project
   - Add `PORT` (Railway sets this automatically)
   - Add `SECRET_KEY` with a strong random string
   - Add `FLASK_ENV=production`

4. **Your Procfile is already configured:**
   - The `Procfile` tells Railway to run: `gunicorn app:app`

5. **Deploy!**
   - Railway will automatically deploy on each push
   - Your app will be available at the Railway-provided URL

## Important Notes for Production

- Do NOT use the hardcoded secret key in production
- Always set a strong `SECRET_KEY` in your Railway variables
- The database uses SQLite which persists on the Railway filesystem
- For a production app, consider migrating to PostgreSQL

## File Structure

```
netflix_clone/
├── app.py              # Main Flask application
├── init_db.py          # Database initialization
├── requirement.txt     # Python dependencies
├── Procfile            # Deployment configuration
├── static/
│   └── style.css       # CSS styles
└── templates/
    ├── home.html
    ├── login.html
    ├── register.html
    ├── movie.html
    ├── profile.html
    ├── search.html
    └── watchlist.html
```

## Troubleshooting

### App won't start on Railway
- Check that `PORT` environment variable is set
- Verify `SECRET_KEY` is configured
- Check Railway logs for specific error messages

### Database errors
- Ensure init_db.py runs successfully
- Check database permissions
- Verify database path is correct

### Dependencies missing
- Run `pip install -r requirement.txt` locally
- Make sure requirement.txt is in the root directory
