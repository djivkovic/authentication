from flask import Blueprint
from flask import request, jsonify
import requests
from auth import authenticate_user
from tour import add_checkpoint, create_tour, get_all_tours

tour_routes = Blueprint('tour', __name__)

# Route to handle creating new tour
@tour_routes.route('/showtours', methods=['GET'])
def create_get_all_tours():
    return get_all_tours(request)

# Route to handle creating new tour
@tour_routes.route('/createtour', methods=['POST'])
def create_tour_route():
    return create_tour(request)

# Route to handle add checkpoints on tour
@tour_routes.route('/addcheckpoint/<int:tour_id>', methods=['PUT'])
def add_checkpoint_route(tour_id):
    return add_checkpoint(request, tour_id)

