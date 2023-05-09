from flask import Flask, jsonify, request, make_response
import uuid
import datetime

app = Flask(__name__)

# Create an empty dictionary to store the code snippets
snippets = {}

# Helper function to paginate the results
def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]

# Endpoint to create a new code snippet
@app.route('/snippets', methods=['POST'])
def create_snippet():
    data = request.get_json()
    snippet_id = str(uuid.uuid4())
    snippets[snippet_id] = {
        'id': snippet_id,
        'title': data.get('title', ''),
        'author': data.get('author', ''),
        'language': data['language'],
        'content': data['content'],
        'created_at': datetime.datetime.utcnow()
    }
    response = jsonify(snippets[snippet_id])
    response.headers['Location'] = f'/snippets/{snippet_id}'
    response.headers['X-Secret'] = str(uuid.uuid4())
    return response, 201

# Endpoint to fetch a code snippet by its ID
@app.route('/snippets/<string:snippet_id>', methods=['GET'])
def get_snippet(snippet_id):
    if snippet_id not in snippets:
        return make_response(jsonify({'error': 'Snippet not found'}), 404)
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

app.run(debug=True)