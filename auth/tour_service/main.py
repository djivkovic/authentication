from flask import Flask
from routes import tour_routes

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(tour_routes)
    app.run(host='0.0.0.0', port=8084)
