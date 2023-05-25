# importing necessary libraries
# Flask is a class that we use to create our app
# jsonify is a function we use to turn python dictionaries into HTTP responses (in JSON formate)
# request is a module we use to get data from HTTP requests
# make_response is a function we use to make HTTP responses
from flask import Flask, jsonify, request, make_response
import uuid
import datetime
import pytz

# current CET (Central European Time)
now = pytz.timezone('CET').localize(datetime.datetime.utcnow())
app = Flask(__name__)

# an empty dictionary to store the code snippets
snippets = {}

# helper function to paginate the results
def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]

# Endpoint to create a new code snippet
@app.route('/snippets', methods=['POST'])
def create_snippet():
    data = request.get_json()

    # check if required fields are present
    if "content" not in data or "language" not in data:
        response = make_response(jsonify({"error": "Missing required content"}), 400)
        return response

    # check if the language is valid
    if data["language"] not in ["Java", "PHP", "Python", "JavaScript", "Plain Text"]:
        response = make_response(jsonify({"error": "Invalid language"}), 400)
        return response

    snippet_id = str(uuid.uuid4())
    secret = str(uuid.uuid4())

    snippets[snippet_id] = {
        'id': snippet_id,
        'title': data.get('title', ''),
        'author': data.get('author', ''),
        'language': data['language'],
        'content': data['content'],
        'created_at': str(now),
        'private': data.get('private', False),
        'secret': secret,
    }

    response = jsonify(snippets[snippet_id])

    response.headers['Location'] = f'/snippets/{snippet_id}' 

    # A 'secret' header is also set on the response. This could be used to
    # provide the client with a secret token that they can use to authenticate
    # future requests related to this snippet, such as deleting it.
    response.headers['secret'] = secret

    # The function returns the response and a status code of 201. The 201 status
    # code is the standard response for an HTTP POST request that results in the
    # creation of a new resource.
    return response, 201

# Endpoint to fetch a code snippet by its ID
# This is a Flask decorator that maps a URL rule to the decorated function.
# In this case, the function is mapped to the URL '/snippets/<string:snippet_id>'
# where <string:snippet_id> is a variable part in the URL that gets passed as
# an argument to the function. The 'methods' argument tells Flask that this
# function should be called when a GET request is sent to this URL.
@app.route('/snippets/<string:snippet_id>', methods=['GET'])
# This is the function that gets called when a GET request is sent to the URL.
# The 'snippet_id' argument is the variable part of the URL that was defined
# in the decorator.
# The key here is in the URL pattern: /snippets/<string:snippet_id>. 
# In Flask, you can include variable sections in a URL by marking 
# sections with <variable_name>. These variable sections will be 
# captured as arguments to the function. In this case, 
# <string:snippet_id> is a variable section, and Flask will 
# capture this part of the URL as a string argument to the function.
def get_snippet(snippet_id):
    # This is a check to see if the provided snippet_id exists in the dictionary
    # of snippets. If it doesn't, it returns a 404 response with an error message.
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    # If the snippet_id exists in the dictionary, it returns a JSON response
    # with the details of the snippet. The 'jsonify' function turns the Python
    # dictionary into a JSON response.
    return jsonify(snippets[snippet_id])

# Endpoint to delete a code snippet by its ID and secret
@app.route('/snippets/<string:snippet_id>', methods=['DELETE'])
# This function will be called when a DELETE request is sent to the above URL.
# The 'snippet_id' argument is the variable part of the URL that was defined in the decorator.
def delete_snippet(snippet_id):

    # This checks if the provided snippet_id exists in the dictionary of snippets.
    # If it doesn't, it returns a 404 response with an error message.
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    
    # This retrieves the 'secret' header from the HTTP request. This is assumed to be the 
    # secret key that authenticates the deletion.
    secret = request.headers.get('secret')

    # This checks if the provided secret matches the one stored in the snippet's data.
    # If it doesn't match, it returns a 401 response with an error message.
    if secret != snippets[snippet_id].get('secret'):
        return make_response(jsonify({'error': 'Invalid secret'}), 401)
    
    # If the snippet_id exists in the dictionary and the provided secret is valid, 
    # it deletes the snippet from the dictionary.
    del snippets[snippet_id]

    # After deleting the snippet, it returns a 204 response to signify that the deletion 
    # was successful. 204 is the status code for 'No Content', which means that the server 
    # has successfully fulfilled the request and there is no additional content to send in the response.
    return '', 204

# Endpoint to update a code snippet by its ID and secret
@app.route('/snippets/<string:snippet_id>', methods=['PUT'])
def update_snippet(snippet_id):
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    secret = request.headers.get('X-Secret')
    if secret != snippets[snippet_id].get('secret'):
        return make_response(jsonify({'error': 'Invalid secret'}), 401)
    
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

    # Create a new snippet with the updated data
    snippets[new_snippet_id] = {
        'id': new_snippet_id,
        'title': data.get('title', ''),
        'author': data.get('author', ''),
        'language': data['language'],
        'content': data['content'],
        'created_at': str(now),
        'private': data.get('private', False),
        'secret': new_secret,
    }

    # Delete the old snippet
    del snippets[snippet_id]

    response = jsonify(snippets[new_snippet_id])
    response.headers['URL'] = f'/snippets/{new_snippet_id}' 
    response.headers['X-Secret'] = str(uuid.uuid4())

    return response, 200


# Endpoint to list all code snippets
@app.route('/snippets', methods=['GET'])
def list_snippets():
    # Set default values for page and per_page
    # These two lines get the 'page' and 'per_page' query parameters from the request.
    # If they are not provided, they default to 1 and 20, respectively.
    # The 'per_page' value is also capped at a maximum of 100.
    page = int(request.args.get('page', 1)) # which page of results to return
    per_page = min(int(request.args.get('per_page', 20)), 100)

    # These lines get the 'language' and 'keyword' query parameters from the request.
    language = request.args.get('language')
    keyword = request.args.get('keyword')

    # This block of code filters the list of snippets based on the 'language' and 'keyword'
    # query parameters. If a 'language' is provided, it only includes snippets in that language.
    # If a 'keyword' is provided, it only includes snippets where the keyword appears in the title or content.
    filtered_snippets = [snippet for snippet in snippets.values()
                        if (not snippet.get('private') and
                            (not language or snippet['language'] == language) and
                            (not keyword or keyword.lower() in snippet['title'].lower() or
                            keyword.lower() in snippet['content'].lower()))]

    # The 'paginate' function is called to get a subset of the filtered snippets
    # based on the 'page' and 'per_page' query parameters.
    paginated_snippets = paginate(filtered_snippets, page, per_page)

    # Total number of snippets after filtering.
    total_snippets = len(filtered_snippets)

    # Calculate the total number of pages
    total_pages = (total_snippets + per_page - 1) // per_page

    # Build the pagination URLs
    prev_url = None
    if page > 1:
        prev_url = f"/snippets?page={page-1}&per_page={per_page}"
        if language:
            prev_url += f"&language={language}"
        if keyword:
            prev_url += f"&keyword={keyword}"
    next_url = None
    if page < total_pages:
        next_url = f"/snippets?page={page+1}&per_page={per_page}"
        if language:
            next_url += f"&language={language}"
        if keyword:
            next_url += f"&keyword={keyword}"

    # Build the response object
    response = {
        'snippets': paginated_snippets,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_snippets': total_snippets,
            'prev_url': prev_url,
            'next_url': next_url
        }
    }

    # Return the paginated results as JSON
    return jsonify(response)
if __name__ == '__main__':
    app.run(debug=True)