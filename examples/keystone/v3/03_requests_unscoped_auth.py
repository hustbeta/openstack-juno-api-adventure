#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests

import local_settings

def get_unscoped_token():
    url = local_settings.auth_url_v3 + 'auth/tokens'
    data = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'domain': {
                            'name': 'Default',
                        },
                        'name': local_settings.username,
                        'password': local_settings.password,
                    },
                },
            },
        },
    }
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print 'get_unscoped_token:', r.status_code
    if r.status_code == 201:
        user_id = r.json()['token']['user']['id']
        token = r.headers['x-subject-token']
        return user_id, token

def validate_token(token):
    print 'validate_token:', token
    url = local_settings.auth_url_v3 + 'auth/tokens'
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'X-Auth-Token': token,
        'X-Subject-Token': token,
    }
    r = requests.get(url, headers=headers)
    print r.headers
    print r.status_code
    print r.text

def list_projects(token):
    url = local_settings.auth_url_v3 + 'projects'
    headers = {
        'X-Auth-Token': token,
    }
    r = requests.get(url, headers=headers)
    print r.headers
    print r.status_code
    print r.text

def show_user_details(user_id, token):
    url = local_settings.auth_url_v3 + 'users/%s' % user_id
    headers = {
        'X-Auth-Token': token,
    }
    r = requests.get(url, headers=headers)
    print r.headers
    print r.status_code
    print r.text

def list_user_projects(user_id, token):
    url = local_settings.auth_url_v3 + 'users/%s/projects' % user_id
    headers = {
        'X-Auth-Token': token,
    }
    r = requests.get(url, headers=headers)
    print r.headers
    print r.status_code
    print r.text

user_id, token = get_unscoped_token()
#list_projects(token)  # 403 Forbidden
list_user_projects(user_id, token)  # 200 OK
#show_user_details(user_id, token)  # 403 Forbidden

