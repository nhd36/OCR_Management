import jwt

def decode_user(jwt_token):
    decoded_jwt = jwt.decode(jwt_token, 'super-secret', algorithm='HS256')
    username = decoded_jwt['identity']
    return username
