# importing necessary libraries
from flask import Flask, jsonify, request, make_response

# to create unique strings of characters that we can use as IDs and secrets
import uuid

import copy

# datetime is a module that lets us work with dates and times
from datetime import datetime

app = Flask(__name__)

# an empty dictionary to store the code snippets
snippets = {}

# function to paginate the results
def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]

@app.route('/snippets', methods=['POST'])
def create_snippet():
    data = request.get_json()

    # Check if required fields are present
    if "content" not in data or "language" not in data:
        response = make_response(jsonify({"error": "Missing required content"}), 400)
        return response

    # Check if the language is valid
    if data["language"] not in ["Java", "PHP", "Python", "JavaScript", "Plain Text"]:
        response = make_response(jsonify({"error": "Invalid language"}), 400)
        return response

    snippet_id = str(uuid.uuid4())
    secret = str(uuid.uuid4())
    now = datetime.now()

    snippets[snippet_id] = {
        'id': snippet_id,
        'title': data.get('title', ''),
        'author': data.get('author', ''),
        'language': data['language'],
        'content': data['content'],
        'created_at': now.strftime("%Y-%m-%d %H:%M:%S"),
        'private': data.get('private', False),
        'secret': secret,
    }
    snippets_resp = snippets[snippet_id].copy()
    del snippets_resp['secret']
    response = jsonify(snippets_resp)
    response.headers['location'] = f'/snippets/{snippet_id}' 
    response.headers['secret'] = secret
    return response, 201

# Endpoint to fetch a code snippet by its ID
@app.route('/snippets/<string:snippet_id>', methods=['GET'])
def get_snippet(snippet_id):
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    snippets_resp = snippets[snippet_id].copy()
    
    del snippets_resp['secret']
    return jsonify(snippets_resp)


# Endpoint to delete a code snippet by its ID and secret
@app.route('/snippets/<string:snippet_id>', methods=['DELETE'])
def delete_snippet(snippet_id):

    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    
    secret = request.headers.get('secret')

    if secret != snippets[snippet_id].get('secret'):
        return make_response(jsonify({'error': 'Invalid secret'}), 401)
    
    del snippets[snippet_id]

    return '', 204

# Endpoint to update a code snippet by its ID and secret
@app.route('/snippets/<string:snippet_id>', methods=['PUT'])
def update_snippet(snippet_id):
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    secret = request.headers.get('secret')
    if secret != snippets[snippet_id].get('secret'):
        return make_response(jsonify({'error': 'Invalid secret'}), 401)
    
    # retrieving the data 
    data = request.get_json()

    # Check if required fields are present
    if "content" not in data or "language" not in data:
        response = make_response(jsonify({"error": "Missing required content"}), 400)
        return response

    # Check if the language is valid
    if data["language"] not in ["Java", "PHP", "Python", "JavaScript", "Plain Text"]:
        response = make_response(jsonify({"error": "Invalid language"}), 400)
        return response

    # Create a new unique ID for the updated snippet
    new_snippet_id = str(uuid.uuid4())
    # Create a new unique secret for the updated snippet
    new_secret = str(uuid.uuid4())
    now = datetime.now()

    # Create a new snippet with the updated data
    snippets[new_snippet_id] = {
        'id': new_snippet_id,
        'title': data.get('title', ''),
        'author': data.get('author', ''),
        'language': data['language'],
        'content': data['content'],
        'created_at': now.strftime("%Y-%m-%d %H:%M:%S"),
        'private': data.get('private', False),
        'secret': new_secret,
    }

    # Delete the old snippet
    del snippets[snippet_id]

    snippets_resp = snippets[new_snippet_id].copy()
    del snippets_resp['secret']
    response = jsonify(snippets_resp)
    response.headers['location'] = f'/snippets/{new_snippet_id}' 
    response.headers['secret'] = new_secret

    return response, 200


# Endpoint to list all code snippets
@app.route('/snippets', methods=['GET'])
def list_snippets():
    # Set default values for page and per_page
    page = int(request.args.get('page', 1)) # which page of snippets to return
    per_page = min(int(request.args.get('per_page', 20)), 100) # how many snippets to include on each page
    language = request.args.get('language')
    keyword = request.args.get('keyword')

    # Get the start and end dates
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # convert the dates to datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
    
    # filter snippets by language, keyword, and date range
    filtered_snippets = [snippet for snippet in snippets.values()
                        if (not snippet.get('private') and
                            (not language or snippet['language'] == language) and
                            (not keyword or keyword.lower() in snippet['title'].lower() or
                             keyword.lower() in snippet['content'].lower()) and
                            (not start_date or datetime.strptime(snippet['created_at'], "%Y-%m-%d %H:%M:%S") >= start_date) and
                            (not end_date or datetime.strptime(snippet['created_at'], "%Y-%m-%d %H:%M:%S") <= end_date))]
    
    filtered_snippets_resp = copy.deepcopy(filtered_snippets)
    for snippet in filtered_snippets_resp:
        if 'secret' in snippet:
            del snippet['secret']

    # Paginate the results
    paginated_snippets = paginate(filtered_snippets_resp, page, per_page)
    total_snippets = len(filtered_snippets_resp)

    # Calculate the total number of pages
    total_pages = (total_snippets + per_page - 1) // per_page

    # Build the response object
    response = {
        'snippets': paginated_snippets,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_snippets': total_snippets,
        }
    }

    # Return the paginated results as JSON
    return jsonify(response)
if __name__ == '__main__':
        app.run(debug=True)


# Improvements to be considered

# 1. To save the snippets in a database
# 2. add pagination function to go forward and back to the pages
# 3. Add more tests
