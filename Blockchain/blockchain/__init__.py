from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Register routes
    from app.routes import blockchain_blueprint
    app.register_blueprint(blockchain_blueprint)
    
    return app
