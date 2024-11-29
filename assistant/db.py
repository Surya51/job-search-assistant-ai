from bson import UUID_SUBTYPE, Binary
from flask import current_app
from pymongo import MongoClient
import uuid

def inti_db(app):
    client = MongoClient(app.config.get("MONGO_URI"))
    app.db = client.get_database("JobSearchAssistant")

def get_user_by_username(username):
    try:
        user = current_app.db.users.find_one({'username': username})
        return _convertBsonFields(user)
    except Exception as e:
        return e

def get_user_by_guid(user_guid):
    try:
        query_guid = _getBinaryGuid(user_guid)
        user = current_app.db.users.find_one({'guid': query_guid})
        return _convertBsonFields(user)
    except Exception as e:
        return e

def add_user(name, username, password):
    guid = _getBinaryGuid()
    current_app.db.users.insert_one({'guid': guid, 'name': name, 'username': username, 'password': password})

def add_assessment_data(filepath, jobDesc, user_guid):
    try:
        guid = _getBinaryGuid()
        user_binary_guid = _getBinaryGuid(user_guid)
        current_app.db.assessment_data.insert_one({'guid': guid, 'user_guid': user_binary_guid, 'file_path': filepath, 'job_description': jobDesc})
        return getStringGuid(guid)
    except Exception as e:
        return e

def get_assessment_data_by_guid(assessment_guid):
    try:
        guid = _getBinaryGuid(assessment_guid)
        assessment = current_app.db.assessment_data.find_one({'guid': guid})
        return _convertBsonFields(assessment)
    except Exception as e:
        return e

def get_latest_assessment(user_guid):
    try:
        user_binary_guid = _getBinaryGuid(user_guid)
        assessment = current_app.db.assessment_data.find_one({'user_guid': user_binary_guid}, sort=[('_id', -1)])
        return _convertBsonFields(assessment)
    except Exception as e:
        return e
    
def save_user_responses(assessment_guid, qnas):
    try:
        assess_binary_guid = _getBinaryGuid(assessment_guid)
        current_app.db.assessment_data.update_one({'guid': assess_binary_guid}, {
            '$addToSet': { 'question_and_answers': qnas }
        })
    except Exception as e:
        return e

# Region: These below methods are to expose to other files.
def createNewGuid():
    return _getBinaryGuid()

def getStringGuid(guid_binary = None):
    guid = uuid.uuid4() if guid_binary is None else uuid.UUID(bytes=guid_binary)
    return str(guid)

#end Region

# Region: These are Private methods to this file.
def _getBinaryGuid(guid_str = None):
    guid = uuid.uuid4() if guid_str is None else uuid.UUID(guid_str)
    return Binary(guid.bytes, subtype=UUID_SUBTYPE)

def _convertBsonFields(data):
    if data is None:
        return data
    partial_name = 'guid'
    if isinstance(data, list):
        for obj in data:
            matching_keys = [key for key in obj.keys() if partial_name in key] if matching_keys is None else matching_keys
            obj["_id"] = str(obj["_id"])
            for key in matching_keys:
                obj[key] = str(uuid.UUID(bytes=obj[key]))
    else:
        data["_id"] = str(data["_id"])
        matching_keys = [key for key in data.keys() if partial_name in key]
        for key in matching_keys:
            data[key] = str(uuid.UUID(bytes=data[key]))
    return data
