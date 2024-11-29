from flask import request

from assistant.jwt import decode_jwt


def get_token_data(data_required = False):
    token = request.headers.get('Authorization')
    decoded = decode_jwt(token, data_required=data_required)
    if(decoded.get('isValid')):
        return {'success': True, 'data': decoded.get('data')}
    else:
        return {'success': False, 'error': decoded.get('error')}