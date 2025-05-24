from flask import Flask
from routes.auth_routes import auth

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register blueprints
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)