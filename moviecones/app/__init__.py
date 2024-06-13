from flask import Flask, jsonify, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config
from app.models import db
from app.resources import MovieListResource, MovieResource, UserRegister, UserLogin
from app.web import web
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    api = Api(app)
    api.add_resource(MovieListResource, '/api/movies')
    api.add_resource(MovieResource, '/api/movies/<int:movie_id>')
    api.add_resource(UserRegister, '/api/register')
    api.add_resource(UserLogin, '/api/login')
    
    app.register_blueprint(web)

    # Setup Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "MovieCones API",
            'dom_id': '#swagger-ui',
            'deepLinking': True,
            'persistAuthorization': True,
            'layout': "StandaloneLayout"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/api/docs')
    def swagger_ui():
        return render_template('swagger_ui.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
