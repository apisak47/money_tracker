from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-999'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://money_tracker_k9lj_user:DWYKZPVk8CvTdXo19ZBvdaS10M8B60cQ@dpg-d6kr4f14tr6s738qks9g-a.singapore-postgres.render.com/money_tracker_k9lj'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.routes import main
    app.register_blueprint(main)

    return app