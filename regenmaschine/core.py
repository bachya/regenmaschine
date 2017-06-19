"""
File: core.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

import json

import requests


def get_access_token(email, password, device_ip=None, api_version=4):
    """Retrieves an access token (either from the device or remotely)"""
    if device_ip:
        url = 'https://{}:8080/api/{}/auth/login'.format(
            device_ip, api_version)
        body = json.dumps({'pwd': password, 'remember': 1})
        verify = False
    else:
        url = 'https://my.rainmachine.com/login/auth'
        body = json.dumps({
            'user': {
                'email': email,
                'pwd': password,
                'remember': 1
            }
        })
        verify = True

    response = requests.post(
        url=url,
        headers={'Content-Type': 'application/json'},
        data=body,
        verify=verify)

    response.raise_for_status()
    return response.json()
