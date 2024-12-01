from .routers.login_register import register
from flask import Flask, Blueprint
from .extends import db, login_manager, migrate, bcrypt, jwt
from .config import Config
from flask_jwt_extended import create_access_token

home = Blueprint("main_blueprint", __name__)

@home.route("/", methods=['GET'])
def home_m():
    access_token = create_access_token(identity="УЦАуцауцАУЦАУЦЦ")
    return {"message": access_token}



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(register)
    app.register_blueprint(home)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    run_app = create_app()
    run_app.run(host="192.168.0.111", port=6043, load_dotenv=True)
