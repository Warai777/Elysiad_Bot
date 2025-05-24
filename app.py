from flask import Flask
from routes.auth_routes import auth
from routes.journal_routes import journal_bp
from routes.inventory_routes import inventory_bp
from routes.container_routes import container_bp
from routes.save_routes import save_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register all blueprints
app.register_blueprint(auth)
app.register_blueprint(journal_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(container_bp)
app.register_blueprint(save_bp)

if __name__ == '__main__':
    app.run(debug=True)