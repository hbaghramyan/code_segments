from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

code_snippets = []

@app.route('/',  methods=['GET'])
def hello_world():
    return 'Hello World!', 201

@app.route('/snippets', methods=['GET'])
def get_snippets():

    return jsonify(code_snippets)

@app.route('/snippets', methods=['POST'])
def add_snippet():
    snippet_data = request.get_json()

    # Validate the request data
    if 'content' not in snippet_data or 'language' not in snippet_data:
        return jsonify({'error': 'Invalid request'}), 400

    if snippet_data['language'] not in ['Java', 'PHP', 'Python', 'JavaScript', 'Plain Text']:
        return jsonify({'error': 'Invalid language'}), 400

    # Create the code snippet
    snippet = {
        'content': snippet_data['content'],
        'language': snippet_data['language'],
        'title': snippet_data.get('title'),
        'author': snippet_data.get('author'),
        'created_at': datetime.utcnow().isoformat()
    }

    # Add the snippet to the in-memory data store
    code_snippets.append(snippet)

    return jsonify(snippet), 201

if __name__ == '__main__':
    app.run(debug=True)
