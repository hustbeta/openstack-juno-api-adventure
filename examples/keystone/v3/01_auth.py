#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Authenticate using username/password, or using token"""
import keystoneclient
import keystoneclient.v3.client

import local_settings

def auth_user(username, password, project_name):
    """Authenticate using username/password"""
    try:
        keystone = keystoneclient.v3.client.Client(username=username,
                                                   password=password,
                                                   project_name=project_name,
                                                   auth_url=local_settings.auth_url_v3)
    except keystoneclient.openstack.common.apiclient.exceptions.Unauthorized:
        return None
    return keystone

def auth_token(token):
    """Authenticate using token"""
    try:
        keystone = keystoneclient.v3.client.Client(token=token,
                                                   auth_url=local_settings.auth_url_v3)
    except keystoneclient.openstack.common.apiclient.exceptions.Unauthorized:
        return None
    return keystone

keystone = auth_token('06ec8f8797004f25a4d75273afc48568')
print keystone

