from flask import jsonify, current_app
import psycopg2
from auth import authenticate_user
from db_specs import db_config

# Function to handle getting all tours along with their tags
def get_all_tours(request):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Fetch all tours along with their tags
        cursor.execute("""
            SELECT tours.*, array_agg(tags.name) AS tags
            FROM tours
            LEFT JOIN tags ON tours.id = tags.tour_id
            GROUP BY tours.id
        """)
        
        # Convert the result to a dictionary for better readability
        tours_with_tags = []
        for row in cursor.fetchall():
            tour = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'duration': row[3],
                'difficulty': row[4],
                'price': row[5],
                'status': row[6],
                'guide_id': row[7],
                'tags': row[8] if row[8] is not None else []  # Convert NULL to empty list
            }
            tours_with_tags.append(tour)
        
        cursor.close()
        conn.close()
        
        return jsonify({'tours': tours_with_tags}), 200
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({'message': 'Error retrieving tours', 'error': str(e)}), 500


def insert_tags_for_tour(tour_id, tags):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Insert each tag for the given tour ID
        for tag in tags:
            cursor.execute("INSERT INTO tags (name, tour_id) VALUES (%s, %s)",
                           (tag, tour_id))
        
        # Commit the changes and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Tags inserted successfully'}), 200
    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        
        # Return an error message
        return jsonify({'message': 'Error inserting tags', 'error': str(e)}), 500


# Function to handle creating new tours
def create_tour(request):    

    token = request.cookies.get('token')
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    # Authenticate the user
    authenticated, user_info = authenticate_user(token)
    if not authenticated:
        return jsonify({'message': 'Unauthorized'}), 401
    
    if user_info['role'] != 'guide':
        return jsonify({'message': 'Unauthorized'}), 401

    # Extract data from request
    title = request.json.get('title')
    description = request.json.get('description')
    duration = request.json.get('duration')
    difficulty = request.json.get('difficulty')
    tags = request.json.get('tags')
    price = request.json.get('price')
    status = request.json.get('status', 'draft')  # default to 'draft' if not provided

    if not all([title, description, duration, difficulty, price]):
        return jsonify({'message': 'Incomplete data provided'}), 400

    user_id = int(user_info['id'])

    # Connect to PostgreSQL and insert the new tour post
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tours (title, description, duration, difficulty, price, status, guide_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                       (title, description, duration, difficulty, price, status, user_id))
        
        # Fetch the newly inserted tour ID
        tour_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        # Insert tags for the newly created tour
        insert_tags_for_tour(tour_id, tags)

        return jsonify({'message': 'Tour created successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Error creating tour', 'error': str(e)}), 500


# Function to handle adding checkpoints
def add_checkpoint(request):
    token = request.cookies.get('token')
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    # Authenticate the user
    authenticated, user_info = authenticate_user(token)
    if not authenticated:
        return jsonify({'message': 'Unauthorized'}), 401

    if user_info['role'] != 'guide':
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = int(user_info['id'])
    
    # Extract data from request
    tour_id = request.json.get('tour_id')
    coordinates_set = set(request.json.get('coordinates'))

    if not all([tour_id, coordinates_set]):
        return jsonify({'message': 'Incomplete data provided'}), 400
    
    # Check if the tour is made by that user
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tours WHERE guide_id = %s",
                       (user_id))
        creator = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({'message': 'Error checking if user created the specific tour with id %s' % tour_id, 'error': str(e)}), 500

    if not creator:
        return jsonify({'message': 'You need to be the creator of this tour before adding checkpoints'}), 403

    # Connect to PostgreSQL and insert the new checkpoint
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO checkpoints (tour_id, user_id, coordinates, name) VALUES (%s, %s, %s, %s)", 
                       (tour_id, user_id, coordinates_set))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Checkpoint added successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Error adding checkpoint', 'error': str(e)}), 500



# TODO: Function to handle editing tours

# TODO: Function to handle deleting checkpoints
'''
def edit_tour(request, comment_id):
    token = request.cookies.get('token')
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    # Authenticate the user
    authenticated, user_info = authenticate_user(token)
    if not authenticated:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = int(user_info['id'])

    # Extract new comment text from request
    new_comment_text = request.json.get('comment_text')

    # Connect to PostgreSQL and update the comment
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        # Update comment only if the user_id matches and the comment_id exists
        cursor.execute("UPDATE comments SET comment_text = %s, last_edited_at = CURRENT_TIMESTAMP WHERE id = %s AND user_id = %s", 
                       (new_comment_text, comment_id, user_id))
        if cursor.rowcount == 0:  # Check if any rows were updated
            return jsonify({'message': 'Unauthorized: You are not the owner of this comment or the comment does not exist'}), 401
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Comment edited successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error editing comment', 'error': str(e)}), 500
'''
