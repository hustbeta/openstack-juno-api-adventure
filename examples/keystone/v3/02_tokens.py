#!/usr/bin/env python
# -*- coding: utf-8 -*-
import keystoneclient
import keystoneclient.v3.client

import local_settings

def authenticate():
    """Authenticate from keystone service, return a client object."""
    keystone = keystoneclient.v3.client.Client(username=local_settings.username,
                                            password=local_settings.password,
                                            project_name=local_settings.tenant_name,
                                            auth_url=local_settings.auth_url_v3)
    return keystone

def get_token(keystone):
    return keystone.auth_token

def validate_token(keystone, token):
    """Validate a given token

    Original validate_token() return keystoneclient.access.AccessInfoV3 object.
    Returned object looks like:
    {
        "methods": ["password"],
        "roles": [{"id": "38b32e0fa648456bad0914ffdb45184a", "name": "admin"}],
        "auth_token": "06ec8f8797004f25a4d75273afc48568",
        "expires_at": "2015-08-27T08:27:48.287542Z",
        "project": {
            "domain": {"id": "default", "name": "Default"},
            "id": "422b53b9339f427abca6a1eab3c1cdd1",
            "name": "admin"
        },
        "catalog": [{"endpoints": [...], "type": "identity", "id": ..., "name": "keystone"}],
        "extras": {},
        "user": {
            "domain": {"id": "default", "name": "Default"},
            "id": "d6a5511a2fd546269cf7c3903b1fe0aa",
            "name": "admin"
        },
        "version": "v3",
        "audit_ids": ["gsq-0nT3Q9yrnsO-fppaHw"],
        "issued_at": "2015-08-27T07:27:48.287573Z"
    }
    """
    try:
        access_info_v3 = keystone.tokens.validate(token)
        return True
    except keystoneclient.openstack.common.apiclient.exceptions.NotFound:
        return False

def get_revoked(keystone):
    """Returns {'signed': CMS(Cryptographic Message Formatted) formatted string}

    I don't know how to use the return value currently.
    """
    return keystone.tokens.get_revoked()

keystone = authenticate()
token = get_token(keystone)
token1 = '06ec8f8797004f25a4d75273afc48568'  # 'expires_at': '2015-08-27T08:27:48.287542Z'
token2 = '12e4329c37d44d4ebfdd08baf5324ecd'  # revoked
print validate_token(keystone, token2)

