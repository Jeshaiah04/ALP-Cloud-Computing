import requests

def fetch_movies():
    # URL sementara untuk pengujian
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)
    movies = response.json()
    return movies

def push_to_database():
    from app.models import db, Movie
    movies = fetch_movies()
    
    for movie in movies:
        new_movie = Movie(
            title=movie['title'],
            description=movie.get('body', ''),  # Ubah sesuai dengan struktur data Anda
            release_date='2024-01-01',  # Tanggal rilis contoh
            rating=5.0  # Rating contoh
        )
        db.session.add(new_movie)
    db.session.commit()
