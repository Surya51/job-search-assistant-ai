import os
from flask import Blueprint, jsonify, request
from flask_cors import CORS

from assistant.db import add_assessment_data, get_assessment_data_by_guid, get_latest_assessment, getStringGuid
from assistant.jwt import decode_jwt
from assistant.utils import get_token_data

UPLOAD_FOLDER = 'uploads'
upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {'pdf'}  # Allowed file types, for time being allowing only pdf file.

CORS(upload_bp)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    token_data = get_token_data(True)
    if(not token_data.get('success')):
        return jsonify(token_data), 401

    prev_file_path = request.form.get('prev_file_path')
    jobDesc = request.form.get('jd')

    file_path = errorMsg = None
    
    file = request.files.get('file')

    if not prev_file_path:
        if not file:
            errorMsg = 'No file part in the request'
        if file and file.filename == '':
            errorMsg = 'No selected file'
        if file and not allowed_file(file.filename):
            errorMsg = 'File type not allowed'
    else:
        file_path = prev_file_path

    if not errorMsg and not jobDesc:
        errorMsg = 'No job description'

    if errorMsg is not None:
        return jsonify({'success': False, 'error': errorMsg}), 400

    if file and allowed_file(file.filename):
        filename = f'{getStringGuid()}.pdf'
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

    assessment_guid = add_assessment_data(file_path, jobDesc, token_data.get('data')['guid'])

    if assessment_guid is None:
        return jsonify({'success': False, 'error': 'Unable to upload with the given description'}), 400

    return jsonify({'success': True, 'message': 'File uploaded successfully', 'data': {'assessment_guid': assessment_guid}}), 200

@upload_bp.route('/get-previous-assess-data')
def get_previous_data():
    token_data = get_token_data(True)
    if not token_data.get('success'):
        return jsonify(token_data), 401

    user_guid = token_data.get('data')['guid']
    response = get_latest_assessment(user_guid)

    hasData = True if response is not None else False

    return jsonify({'success': True, 'hasData': hasData, 'data': response}), 200