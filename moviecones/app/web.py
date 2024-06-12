from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, get_jwt_identity
from app.models import db, User, Movie

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')

@web.route('/')
def home():
    return render_template('index.html')

@web.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('User already exists')
            return redirect(url_for('web.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('User created successfully')
        return redirect(url_for('web.login'))
    
    return render_template('register.html')

@web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Invalid credentials')
            return redirect(url_for('web.login'))
        
        access_token = create_access_token(identity={'username': user.username})
        response = make_response(redirect(url_for('web.movies')))
        set_access_cookies(response, access_token)
        return response
    
    return render_template('login.html')

@web.route('/logout')
def logout():
    response = redirect(url_for('web.login'))
    response.set_cookie('access_token', '', expires=0)
    return response

@web.route('/movies')
@jwt_required()
def movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@web.route('/movies/<int:movie_id>')
@jwt_required()
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_detail.html', movie=movie)
