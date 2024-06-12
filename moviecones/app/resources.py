from flask import request, jsonify
from flask_restful import Resource
from app.models import db, User, Movie
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if User.query.filter_by(username=username).first():
            return {'message': 'User already exists'}, 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={'username': user.username})
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response

class MovieListResource(Resource):
    @jwt_required()
    def get(self):
        movies = Movie.query.all()
        return [{'id': movie.id, 'title': movie.title, 'description': movie.description, 'release_date': movie.release_date, 'rating': movie.rating} for movie in movies]

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_movie = Movie(
            title=data['title'],
            description=data['description'],
            release_date=data['release_date'],
            rating=data['rating']
        )
        db.session.add(new_movie)
        db.session.commit()
        return {'id': new_movie.id, 'title': new_movie.title, 'description': new_movie.description, 'release_date': new_movie.release_date, 'rating': new_movie.rating}, 201

class MovieResource(Resource):
    @jwt_required()
    def get(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return {'id': movie.id, 'title': movie.title, 'description': movie.description, 'release_date': movie.release_date, 'rating': movie.rating}

    @jwt_required()
    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return '', 204

    @jwt_required()
    def put(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        data = request.get_json()
        movie.title = data['title']
        movie.description = data['description']
        movie.release_date = data['release_date']
        movie.rating = data['rating']
        db.session.commit()
        return {'id': movie.id, 'title': movie.title, 'description': movie.description, 'release_date': movie.release_date, 'rating': movie.rating}
