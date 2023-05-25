# Import the necessary libraries
import pytest
from flask import Flask, json
from flask_testing import TestCase
from main import app 
from datetime import datetime

class MyTest(TestCase):
    def create_app(self):
        return app

    def test_create_snippet(self):
        # creating a test snippet
        test_snippet = {
            "content": "print('hello, world!')",
            "language": "Python",
            "title": "Hello World",
            "author": "Test Author",
            "private": False
        }

        # POST request to the '/snippets'
        response = self.client.post('/snippets', data=json.dumps(test_snippet), content_type='application/json')

        # checking the response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['content'], test_snippet['content'])
        self.assertEqual(data['language'], test_snippet['language'])

    def test_get_snippet(self):
        # creating a test snippet
        currentTime = datetime.now()
        currentTime = currentTime.replace(microsecond=0)
        test_snippet = {
            "content": "print('hello, world!')",
            "language": "Python",
            "title": "Hello World",
            "author": "Test Author",
            "private": False
        }

        # making a POST request to the '/snippets' route
        creatResponse = self.client.post('/snippets', data=json.dumps(test_snippet), content_type='application/json')
        createdData = json.loads(creatResponse.data)

        getResponse = self.client.get('/snippets/'+createdData['id'])
        self.assertEqual(getResponse.status_code, 200)
        
        data = json.loads(getResponse.data)
        self.assertEqual(data['content'], test_snippet['content'])
        self.assertEqual(data['language'], test_snippet['language'])
        assert 'created_at' in data
        assert 'secret' not in data
        datetime_str = data['created_at']  # example datetime string
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        assert datetime_obj >= currentTime 

    # add more tests for other endpoints

# run the tests
if __name__ == '__main__':
    pytest.main()
