from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Set up a response at the root / path. Takes GET method.
@app.route('/', methods=['GET'])
def hello_world():
    return 'Flask Dockerized'

# Pass a static JSON dict. Takes GET method.
@app.route('/api/person', methods=['GET'])
def return_person():
    person = {'fname': 'Lester', 'lname': 'Bangs', 'year': 1982}
    return jsonify(person)

# Pass a simple array that's been jsonified. Takes GET method.
@app.route('/api/place', methods=['GET'])
def return_place():
    return jsonify(city='Charlottesville',lat=38.0401199,long=-78.5025264)

# Take a string var and echo back. Takes POST method.
@app.route('/api/user/<username>', methods=['POST'])
def show_user(username):
    return jsonify(user=username)

# Take an int var and echo back. Takes GET or POST method.
@app.route('/api/post/<int:post_id>', methods=['GET','POST'])
def show_post(post_id):
    return jsonify(postid=post_id)

# Take a github user/org and return results. Takes POST method.
@app.route('/api/github/<username>', methods=['POST'])
def show__github_user(username):
    qurl = 'https://api.github.com/users/' + str(username)
    r = requests.get(qurl)
    return r.json()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
