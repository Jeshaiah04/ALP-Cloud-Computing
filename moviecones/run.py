from app import create_app, scraper
from app.models import db, User
from flask_jwt_extended import create_access_token

app = create_app()

def print_bearer_tokens():
    with app.app_context():
        users = User.query.all()
        for user in users:
            access_token = create_access_token(identity={'username': user.username})
            print(f'Bearer token for {user.username}: {access_token}')

with app.app_context():
    from app.models import db
    db.create_all()
    scraper.push_to_database()
    print_bearer_tokens()

if __name__ == '__main__':
    app.run(debug=True)
