import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC8a5d61dccb1aac15355a98d074eaf40e'
    TWILIO_SYNC_SERVICE_SID = 'ISc63dc928d03d465242d2eb1b0a03000b'
    TWILIO_API_KEY = 'SK715d9adb67dfd6a5f79ec33157a56f9f'
    TWILIO_API_SECRET = 'Ut4uFSVjy2w2aF5zrM3MhgntbovjJkGI'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
	text_from_notepad= request.form['text']
	with open('workfile.txt','w') as f:
		f.write(text_from_notepad)
	path_to_store= "workfile.txt"

	return send_file(path_to_store,as_attachment=True)
if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
