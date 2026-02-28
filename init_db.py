import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()

# Create users table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# Create movies table
cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        genre TEXT,
        release_date INTEGER,
        rating REAL,
        image_url TEXT,
        duration INTEGER,
        director TEXT,
        cast TEXT,
        language TEXT,
        content_rating TEXT,
        country TEXT,
        icon TEXT
    )
""")

# Create watchlist table
cur.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, movie_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
""")

# Create watch history table
cur.execute("""
    CREATE TABLE IF NOT EXISTS watch_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        progress_minutes INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
""")

# Create user ratings table
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        rating INTEGER,
        review TEXT,
        date_rated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, movie_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
""")

# Insert sample movies - Real Movies with Real Data
movies = [
    # Format: (title, description, genre, release_date, rating, image_url, duration, director, cast, language, content_rating, country, icon)
    ("The Shawshank Redemption", "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "Drama", 1994, 9.3, "https://images.unsplash.com/photo-1536233135449-7a4e6f5bfc04?w=400&h=600&fit=crop", 142, "Frank Darabont", "Tim Robbins, Morgan Freeman", "English", "R", "USA", "🎭"),
    ("The Godfather", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his youngest and most reluctant son.", "Crime|Drama", 1972, 9.2, "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop", 175, "Francis Ford Coppola", "Marlon Brando, Al Pacino, Robert Duvall", "English|Italian", "R", "USA", "🔫"),
    ("The Dark Knight", "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological risks.", "Action|Crime", 2008, 9.0, "https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=400&h=600&fit=crop", 152, "Christopher Nolan", "Christian Bale, Heath Ledger, Aaron Eckhart", "English", "PG-13", "USA|UK", "🦇"),
    ("Schindler's List", "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his workforce.", "Drama|War", 1993, 8.9, "https://images.unsplash.com/photo-1516321318423-f06f70504646?w=400&h=600&fit=crop", 195, "Steven Spielberg", "Liam Neeson, Ralph Fiennes, Ben Kingsley", "English|Polish|German", "R", "USA", "⚔️"),
    ("Pulp Fiction", "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", "Crime|Drama", 1994, 8.9, "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop", 154, "Quentin Tarantino", "John Travolta, Samuel L. Jackson, Uma Thurman", "English|Spanish|French", "R", "USA", "🔪"),
    
    # Sci-Fi Classics
    ("Inception", "A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.", "Science Fiction|Thriller", 2010, 8.8, "https://images.unsplash.com/photo-1489599849228-ed4dc59b2e9b?w=400&h=600&fit=crop", 148, "Christopher Nolan", "Leonardo DiCaprio, Marion Cotillard, Ellen Page", "English", "PG-13", "USA|UK", "🤯"),
    ("Forrest Gump", "The presidencies of Kennedy and Johnson unfold from the perspective of an Alabama man with an IQ of 75.", "Drama|Romance", 1994, 8.8, "https://images.unsplash.com/photo-1548034328-c9db6910d146?w=400&h=600&fit=crop", 142, "Robert Zemeckis", "Tom Hanks, Gary Sinise, Sally Field", "English", "PG-13", "USA", "🏃"),
    ("Lord of the Rings: Fellowship", "A meek Hobbit from the Shire and eight companions embark on a journey to destroy the powerful One Ring.", "Fantasy|Adventure", 2001, 8.8, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 178, "Peter Jackson", "Elijah Wood, Ian McKellen, Viggo Mortensen", "English", "PG-13", "USA|New Zealand", "💍"),
    ("Fight Club", "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "Drama|Thriller", 1999, 8.8, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 139, "David Fincher", "Brad Pitt, Edward Norton, Helena Bonham Carter", "English", "R", "USA|Germany", "👊"),
    ("Goodfellas", "The story of Henry Hill and his life in the mob along with his wife Karen Hill and his mob partners.", "Crime|Drama", 1990, 8.7, "https://images.unsplash.com/photo-1489599849228-ed4dc59b2e9b?w=400&h=600&fit=crop", 146, "Martin Scorsese", "Robert De Niro, Ray Liotta, Paul Sorvino", "English|Italian", "R", "USA", "🤐"),
    
    ("The Matrix", "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "Science Fiction|Action", 1999, 8.7, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 136, "The Wachowskis", "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "English", "R", "USA|Australia", "💊"),
    ("Saving Private Ryan", "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper.", "War|Drama", 1998, 8.6, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 169, "Steven Spielberg", "Tom Hanks, Edward Burns, Tom Sizemore", "English|French|German", "R", "USA", "🪖"),
    ("The Green Mile", "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and miracle worker.", "Drama|Crime", 1999, 8.6, "https://images.unsplash.com/photo-1549887534-f2cb8b89a7bb?w=400&h=600&fit=crop", 189, "Frank Darabont", "Tom Hanks, David Morse, Michael Clarke Duncan", "English", "R", "USA", "⚖️"),
    ("Se7en", "Two detectives hunt a serial killer who uses the seven deadly sins as his motives.", "Crime|Thriller", 1995, 8.6, "https://images.unsplash.com/photo-1560169897-fc0cdbdfa4d5?w=400&h=600&fit=crop", 127, "David Fincher", "Brad Pitt, Morgan Freeman, Kevin Spacey", "English", "R", "USA", "🔍"),
    ("Parasite", "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "Thriller|Drama", 2019, 8.6, "https://images.unsplash.com/photo-1549887534-f2cb8b89a7bb?w=400&h=600&fit=crop", 132, "Bong Joon-ho", "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong", "Korean", "R", "South Korea", "🏠"),
    
    ("The Silence of the Lambs", "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", "Thriller|Crime|Drama", 1991, 8.6, "https://images.unsplash.com/photo-1516321318423-f06f70504646?w=400&h=600&fit=crop", 118, "Jonathan Demme", "Jodie Foster, Scott Glenn, Anthony Hopkins", "English", "R", "USA", "🦅"),
    ("Interstellar", "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "Science Fiction|Drama|Adventure", 2014, 8.6, "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=600&fit=crop", 169, "Christopher Nolan", "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "English", "PG-13", "USA|UK", "🚀"),
    
    # Action
    ("Gladiator", "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", "Action|Drama", 2000, 8.5, "https://images.unsplash.com/photo-1560169897-fc0cdbdfa4d5?w=400&h=600&fit=crop", 155, "Ridley Scott", "Russell Crowe, Joaquin Phoenix, Lucilla Giannini", "English", "R", "USA|Malta", "⚔️"),
    ("The Departed", "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in Boston.", "Crime|Thriller|Drama", 2006, 8.5, "https://images.unsplash.com/photo-1516321318423-f06f70504646?w=400&h=600&fit=crop", 151, "Martin Scorsese", "Leonardo DiCaprio, Matt Damon, Jack Nicholson", "English|Mandarin", "R", "USA", "👮"),
    ("The Shining", "A family isolated by heavy snow in a remote hotel descends into madness and violence.", "Horror|Thriller", 1980, 8.4, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 146, "Stanley Kubrick", "Jack Nicholson, Shelley Duvall, Danny Lloyd", "English", "R", "USA|UK", "👻"),
    ("Joker", "In Gotham City, frustrated comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral.", "Thriller|Drama|Crime", 2019, 8.4, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 122, "Todd Phillips", "Joaquin Phoenix, Robert De Niro, Zazie Beetz", "English", "R", "USA", "🃏"),
    ("Avengers: Endgame", "After the devastating events, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.", "Action|Adventure|Sci-Fi", 2019, 8.4, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 181, "Anthony & Joe Russo", "Robert Downey Jr., Chris Evans, Mark Ruffalo", "English", "PG-13", "USA", "⚡"),
    
    # Drama
    ("The Pursuit of Happyness", "A struggling salesman takes custody of his son as he's poised to begin a life-changing professional endeavor.", "Drama|Biography", 2006, 8.2, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 117, "Gabriele Muccino", "Will Smith, Thandiwe Newton, Jaden Smith", "English", "PG-13", "USA", "💼"),
    ("Avatar", "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following orders and protecting the world.", "Science Fiction|Adventure", 2009, 8.2, "https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=400&h=600&fit=crop", 162, "James Cameron", "Sam Worthington, Zoe Saldana, Sigourney Weaver", "English", "PG-13", "USA", "🌍"),
    ("The Wolf of Wall Street", "Based on the true story of Jordan Belfort, from his rise to a wealthy stockbroker to his fall involving crime and corruption.", "Drama|Crime|Biography", 2013, 8.2, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 180, "Martin Scorsese", "Leonardo DiCaprio, Jonah Hill, Margot Robbie", "English|Mandarin|French", "R", "USA", "💰"),
    ("La La Land", "While navigating their careers in Los Angeles, a pianist and an actress fall in love while pursuing their dreams.", "Romance|Drama|Musical", 2016, 8.0, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 128, "Damien Chazelle", "Ryan Gosling, Emma Stone", "English", "PG-13", "USA", "🎵"),
    
    # More Popular
    ("Dune", "Paul Atreides must travel to the dangerous planet Dune to ensure the future of his family and people against all opposition.", "Science Fiction|Adventure|Drama", 2021, 8.0, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 156, "Denis Villeneuve", "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac", "English", "PG-13", "USA|Canada|Hungary", "🪐"),
    ("The Avengers", "Earth's mightiest heroes must come together and learn to fight as a team to save the world from an alien invasion.", "Action|Adventure|Sci-Fi", 2012, 8.0, "https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=400&h=600&fit=crop", 143, "Joss Whedon", "Robert Downey Jr., Chris Evans, Chris Hemsworth", "English", "PG-13", "USA", "🦸"),
    ("The Exorcist", "When a young girl is possessed by a mysterious entity, two priests must save her soul from damnation.", "Horror|Thriller", 1973, 8.0, "https://images.unsplash.com/photo-1560169897-fc0cdbdfa4d5?w=400&h=600&fit=crop", 132, "William Friedkin", "Ellen Burstyn, Max von Sydow, Linda Blair", "English|Latin", "R", "USA", "😈"),
    ("Oppenheimer", "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during WWII.", "Drama|Biography", 2023, 8.1, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 180, "Christopher Nolan", "Cillian Murphy, Robert Downey Jr., Emily Blunt", "English", "R", "USA|UK", "☢️"),
    ("Mad Max: Fury Road", "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland.", "Action|Adventure|Sci-Fi", 2015, 8.1, "https://images.unsplash.com/photo-1560169897-fc0cdbdfa4d5?w=400&h=600&fit=crop", 120, "George Miller", "Tom Hardy, Charlize Theron, Nicholas Hoult", "English", "R", "Australia|USA", "🏜️"),
    
    ("The Grand Budapest Hotel", "A writer encounters the owner of an aging high-class hotel in Budapest, who tells him of his early years as a lobby boy.", "Comedy|Crime|Drama", 2014, 8.1, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 99, "Wes Anderson", "Ralph Fiennes, Tony Revolori, Jeff Goldblum", "English|French|German", "PG-13", "Germany|USA", "🏨"),
    ("The Wizard of Oz", "Dorothy Gale is swept away to a magical land in a tornado and embarks on a quest to return home.", "Fantasy|Musical", 1939, 8.1, "https://images.unsplash.com/photo-1548034328-c9db6910d146?w=400&h=600&fit=crop", 102, "Victor Fleming", "Judy Garland, Ray Bolger, Bert Lahr", "English", "G", "USA", "🌪️"),
    ("Toy Story", "A cowboy doll is temporarily replaced and forms a rivalry with a new spaceman action figure, but they must work together to be reunited with their owner.", "Comedy|Family|Animation", 1995, 8.3, "https://images.unsplash.com/photo-1536233135449-7a4e6f5bfc04?w=400&h=600&fit=crop", 81, "John Lasseter", "Tom Hanks, Tim Allen, Don Rickles", "English", "G", "USA", "🤠"),
    ("Singin' in the Rain", "In the early 1920s, a famous idol discovers his best friend is a woman while they perform together in a musical spectacular.", "Comedy|Musical|Romance", 1952, 8.3, "https://images.unsplash.com/photo-1548034328-c9db6910d146?w=400&h=600&fit=crop", 103, "Gene Kelly, Stanley Donen", "Gene Kelly, Donald O'Connor, Debbie Reynolds", "English", "G", "USA", "🎬"),
    
    ("The Notebook", "A poor yet passionate man falls in love with a rich young woman, but they are soon separated by their social differences.", "Romance|Drama", 2004, 7.8, "https://images.unsplash.com/photo-1549887534-f2cb8b89a7bb?w=400&h=600&fit=crop", 123, "Nick Cassavetes", "Ryan Gosling, Rachel McAdams, James Garner", "English", "PG-13", "USA", "💕"),
    ("Titanic", "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.", "Romance|Drama", 1997, 7.8, "https://images.unsplash.com/photo-1523264521851-91fcf91c4ef4?w=400&h=600&fit=crop", 194, "James Cameron", "Leonardo DiCaprio, Kate Winslet, Billy Zane", "English|Swedish|Italian|French|German", "PG-13", "USA", "🚢"),
    ("A Quiet Place", "In a world where creatures hunt by sound, a family must stay silent to survive and protect themselves.", "Horror|Drama|Sci-Fi", 2018, 7.5, "https://images.unsplash.com/photo-1549887534-f2cb8b89a7bb?w=400&h=600&fit=crop", 90, "John Krasinski", "Emily Blunt, John Krasinski, Millicent Simmonds", "English|American Sign Language", "PG-13", "USA", "🤫"),
    ("The Great Gatsby", "A mysterious millionaire throws lavish parties for a beautiful woman he once loved, hoping to win her back.", "Drama|Romance", 2013, 7.2, "https://images.unsplash.com/photo-1523264521851-91fcf91c4ef4?w=400&h=600&fit=crop", 143, "Baz Luhrmann", "Leonardo DiCaprio, Carey Mulligan, Toby Maguire", "English", "PG-13", "USA", "🥂"),
    
    # Additional popular titles
    ("12 Angry Men", "A jury holds the power to determine the fate of an accused man. When one juror begins to think beyond the obvious, others question their judgment.", "Drama|Crime", 1957, 9.0, "https://images.unsplash.com/photo-1516321318423-f06f70504646?w=400&h=600&fit=crop", 96, "Sidney Lumet", "Henry Fonda, Lee J. Cobb, Martin Balsam", "English", "Not Rated", "USA", "⚖️"),
    ("Memento", "A man with short-term memory loss attempts to track down his wife's murderer by using notes and tattoos.", "Thriller|Mystery", 2000, 8.4, "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop", 113, "Christopher Nolan", "Guy Pearce, Carrie-Anne Moss, Joe Pantoliano", "English", "R", "USA", "🧩"),
    ("The Prestige", "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything.", "Mystery|Thriller|Drama", 2006, 8.5, "https://images.unsplash.com/photo-1517604931442-7e0c6f169a0b?w=400&h=600&fit=crop", 130, "Christopher Nolan", "Christian Bale, Hugh Jackman, Michael Caine", "English", "PG-13", "USA|UK", "🎩"),
]

for movie in movies:
    try:
        cur.execute("INSERT INTO movies VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", movie)
    except sqlite3.IntegrityError:
        pass

db.commit()
db.close()

print("✅ Database initialized successfully!")
