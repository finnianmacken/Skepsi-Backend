import json
import jwt
import requests
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import os


def get_token_auth_header(info):
    auth_header = info.context.META.get('authorization')
    parts = auth_header.split()
    token = parts[1]

    return token

def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('skepsi.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('skepsi.us.auth0.com')
    decoded_token = jwt.decode(token, public_key, audience='http://127.0.0.1:8000/', issuer=issuer, algorithms=['RS256'])
    return decoded_token


def extract_permissions(token):
    decoded_token = jwt_decode_token(token)
    if 'permissions' in decoded_token.keys():
        return decoded_token['permissions']


class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()
