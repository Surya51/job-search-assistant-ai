from datetime import datetime, timezone, timedelta
from flask import current_app
import jwt

ALGORITHM = 'HS256'

def create_jwt(payload):
  expiration_minutes = float(current_app.config.get('EXPIRATION_MINUES'))
  payload['password'] = ''
  payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
  return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm=ALGORITHM)

def decode_jwt(token, data_required = False):
  if token is None:
    return { 'isValid': False, 'noToken': True, 'error': 'No token' }
  try:
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
    decoded = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=[ALGORITHM])
    if (data_required):
        return  {'isValid': True, 'data': decoded}
    return {'isValid': True}
  except jwt.ExpiredSignatureError:
    return {'isValid': False, "error": "Token has expired"}
  except jwt.InvalidTokenError:
    return {'isValid': False, "error": "Invalid token"}
