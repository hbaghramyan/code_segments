# importing necessary libraries
# Flask is a class that we use to create our app
# jsonify is a function we use to turn python dictionaries into HTTP responses (in JSON formate)
# request is a module we use to get data from HTTP requests
# make_response is a function we use to make HTTP responses
from flask import Flask, jsonify, request, make_response

# uuid is a library that helps us create unique strings of characters that we can use as IDs
import uuid

# datetime is a module that lets us work with dates and times
import datetime
import pytz

# current CET (Central European Time)
now = pytz.timezone('CET').localize(datetime.datetime.utcnow())

# Here, we are creating a new instance of the Flask class for our app
# __name__ is a special variable in Python that gets the name of the script
# If we run this script directly, __name__ will be "__main__"
# If we import this script into another script, __name__ will be the name of this script
# Flask uses __name__ to know where to find other files like templates
app = Flask(__name__)

# an empty dictionary to store the code snippets
snippets = {}

# Helper function to paginate the results
def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]

# This is a decorator provided by Flask. It tells Flask that this function is
# associated with the URL '/snippets' and should be called when a POST request
# is made to that URL. So, for example, if someone uses a tool like curl or
# Postman to send a POST request to 'http://localhost:5000/snippets', this
# function will be called.
# Endpoint to create a new code snippet
@app.route('/snippets', methods=['POST'])
def create_snippet():
    # The 'request' object is a Flask global object that represents the
    # incoming HTTP request. The '.get_json()' method is used to parse the
    # request data as JSON, turning it into a Python dictionary.
    # The app object is a global object that represents the Flask application. 
    # The request object is a global object that represents the incoming HTTP 
    # request. The two objects are connected because the request object is 
    # created by the app object when a request is received.
    data = request.get_json()

    # Check if required fields are present
    if "content" not in data or "language" not in data:
        response = make_response(jsonify({"error": "Missing required content"}), 400)
        return response

    # Check if the language is valid
    if data["language"] not in ["Java", "PHP", "Python", "JavaScript", "Plain Text"]:
        response = make_response(jsonify({"error": "Invalid language"}), 400)
        return response

    # A unique ID is generated for the new code snippet using the uuid library.
    # A UUID is a 128-bit number, but it is often represented as a string of 
    # 36 characters. The string representation of a UUID is made up of 5 groups 
    # of 8 hexadecimal digits, separated by hyphens.
    snippet_id = str(uuid.uuid4())

    # The new code snippet is stored in the 'snippets' dictionary. Each snippet
    # is itself a dictionary with keys for 'id', 'title', 'author', 'language',
    # 'content', and 'created_at'. The values for 'title' and 'author' are
    # taken from the request data, defaulting to an empty string if they are
    # not provided. The values for 'language' and 'content' are taken directly
    # from the request data. The 'created_at' value is the current date and time.
    snippets[snippet_id] = {
        'id': snippet_id,
        'title': data.get('title', ''),
        'author': data.get('author', ''),
        'language': data['language'],
        'content': data['content'],
        'created_at': str(now),
    }

    # A response is created using the 'jsonify' function, which turns the
    # Python dictionary into a JSON response. The response includes the
    # details of the newly created snippet.
    response = jsonify(snippets[snippet_id])

    # The 'Location' header is set on the response to the URL of the new
    # code snippet. This is a common practice when creating a new resource
    # in a RESTful API to let the client know where they can find the new resource.
    response.headers['URL'] = f'/snippets/{snippet_id}' 

    # An 'X-Secret' header is also set on the response. This could be used to
    # provide the client with a secret token that they can use to authenticate
    # future requests related to this snippet, such as deleting it.
    response.headers['X-Secret'] = str(uuid.uuid4())

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
def delete_snippet(snippet_id):
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
    secret = request.headers.get('X-Secret')
    if secret != snippets[snippet_id].get('secret'):
        return make_response(jsonify({'error': 'Invalid secret'}), 401)
    del snippets[snippet_id]
    return '', 204

# Endpoint to list all code snippets
@app.route('/snippets', methods=['GET'])
def list_snippets():
    # Set default values for page and per_page
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 20)), 100)
    language = request.args.get('language')
    keyword = request.args.get('keyword')

    # Filter snippets by language and keyword
    filtered_snippets = [snippet for snippet in snippets.values()
                        if (not snippet.get('private') and
                            (not language or snippet['language'] == language) and
                            (not keyword or keyword.lower() in snippet['title'].lower() or
                            keyword.lower() in snippet['content'].lower()))]

    # Paginate the results
    paginated_snippets = paginate(filtered_snippets, page, per_page)
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