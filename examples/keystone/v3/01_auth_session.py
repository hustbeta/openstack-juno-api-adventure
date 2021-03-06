#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Authenticate using username/password, or using token, with or without session.

Note that auth without session is deprecated.
"""
import time

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.session
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

def auth_user_with_session(username, password, project_name):
    """Authenticate using username/password

    This method doesn't verify username/password.
    Instead, client will authenticate on first request,
    and re-authenticate automatically when the token expires.
    """
    auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                    username=username,
                                                    password=password,
                                                    user_domain_name='Default',
                                                    project_domain_name='Default',
                                                    project_name=project_name)
    session = keystoneclient.session.Session(auth=auth)
    keystone = keystoneclient.v3.client.Client(session=session)

    return keystone

def auth_token(token):
    """Authenticate using token"""
    try:
        keystone = keystoneclient.v3.client.Client(token=token,
                                                   auth_url=local_settings.auth_url_v3)
    except keystoneclient.openstack.common.apiclient.exceptions.Unauthorized:
        return None
    return keystone

def auth_token_with_session(token):
    """Authenticate using token."""
    # TODO Failed, need investigating.
    auth = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                                 token=token)
    session = keystoneclient.session.Session(auth=auth)
    keystone = keystoneclient.v3.client.Client(session=session)

    return keystone

keystone = auth_user_with_session(local_settings.username,
                                  local_settings.password,
                                  local_settings.tenant_name)

try:
    result = keystone.domains.list()
    print result

    # set token expiration to a very short period, and wait for expiration here
    for i in range(1, 40):
        time.sleep(1)

    result = keystone.projects.list()
    print result
except keystoneclient.openstack.common.apiclient.exceptions.Unauthorized:
    print 'authentication failed'

