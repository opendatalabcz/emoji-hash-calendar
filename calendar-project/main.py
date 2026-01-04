from flask import Flask
from flasgger import Swagger
from controllers.calendar_controller import calendar_bp
from flask_cors import CORS


# TODO - test for non all day events      ✔️
# TODO - fix why it adds extra day to end  ✔️
# TODO - add dict for different languages -> language detection
# TODO - error handling in importer

# TODO - filter event info like google calls etc

# TODO - add other transformers_class
# TODO - embedding method

# TODO - add user defined mapping
# TODO - different languages

# TODO - frontend website
# TODO - add box for users to try sentence -> emoji before actual transformation

# TODO - return .ics to be downloadable

# TODO - docker

# TODO - GraphAPI integration

# TODO - user accounts?
# TODO - database for calendars and users?
# TODO - database for custom mappings

# TODO - logs
# TODO - huge .ics files


app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

app.register_blueprint(calendar_bp, url_prefix="/calendar")

@app.route("/")
def home():
    # TODO
    return "Welcome to Calendar Transformer!"

if __name__ == "__main__":
    app.run(debug=True)
