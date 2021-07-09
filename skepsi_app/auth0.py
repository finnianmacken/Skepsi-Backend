import json, requests
from requests.exceptions import RequestException, HTTPError, URLRequired

# Configuration Values
domain = 'skepsi.us.auth0.com'
audience = f'https://{domain}/api/v2/'
client_id = 'KWGb4t1YqUcPYfzssrN4IOtjVQtHpAPm'
client_secret = '3XFVjVJC8-Rm4Xe_WaO3bJWRhpsa8HKsoyLu8I_Kx_rozSUykmdrR0oOLtfyiy7n'
grant_type = "client_credentials"  # OAuth 2.0 flow to use

# Get an Access Token from Auth0
base_url = f"https://{domain}"
payload = {
    'grant_type': grant_type,
    'client_id': client_id,
    'client_secret': client_secret,
    'audience': audience
}

def get_token():
    response = requests.post(f'{base_url}/oauth/token', data=payload)

    print(response)
    oauth = response.json()
    access_token = oauth.get('access_token')
    return access_token

#  Add the token to the Authorization header of the request


def delete_user(user_id):
    access_token = get_token()
    domain = 'skepsi.us.auth0.com'
    base_url = f"https://{domain}"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    id = user_id

    try:
        res = requests.delete(f'{base_url}/api/v2/users/{id}', headers=headers)
        print(res)
    except HTTPError as e:
        print(f'HTTPError: {str(e.code)} {str(e.reason)}')
    except URLRequired as e:
        print(f'URLRequired: {str(e.reason)}')
    except RequestException as e:
        print(f'RequestException: {e}')
    except Exception as e:
        print(f'Generic Exception: {e}')
