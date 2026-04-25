from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from db import db
from controllers.calendar_controller import calendar_bp
from controllers.user_controller import user_bp

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

#create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar_transformer.db'
db.init_app(app)

#register blueprints
app.register_blueprint(calendar_bp, url_prefix="/calendar")
app.register_blueprint(user_bp, url_prefix="/user")


@app.route("/")
def home():
    return "<h1>Welcome to Calendar Transformer!</h1>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
