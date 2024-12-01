import os

from dotenv import load_dotenv
from flask import jsonify
from flask_cors import CORS

from assistant import assess, auth, upload
from assistant.db import inti_db

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
MONGO_URI = os.getenv('MONGO_URI')
ACCESS_TOKEN = os.getenv('HF_ACCESS_TOKEN')
EXPIRATION_MINUES = os.getenv('EXPIRATION_MINUES')
CLOUD_PROJECT_ID = os.getenv('CLOUD_PROJECT_ID')
CLOUD_PROJECT_NAME = os.getenv('CLOUD_PROJECT_NAME')
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')

def create_app(app):
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MONGO_URI=MONGO_URI,
        ACCESS_TOKEN=ACCESS_TOKEN,
        EXPIRATION_MINUES=EXPIRATION_MINUES,
        CLOUD_STORAGE_BUCKET=CLOUD_STORAGE_BUCKET,
        CLOUD_PROJECT_ID=CLOUD_PROJECT_ID,
        CLOUD_PROJECT_NAME=CLOUD_PROJECT_NAME
    )

    os.makedirs(upload.UPLOAD_FOLDER, exist_ok=True)

    CORS(app)
    inti_db(app)

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(upload.upload_bp)
    app.register_blueprint(assess.assess_bp)

    @app.route("/")
    def health():
        return jsonify({'health': 'App health is good. You can proceed..'}), 200

    return app