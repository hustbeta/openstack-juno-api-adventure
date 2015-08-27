#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Authenticate using v2.0 API, get token"""
import keystoneclient.v2_0.client

import local_settings

def get_token():
    keystone = keystoneclient.v2_0.client.Client(auth_url=local_settings.auth_url,
                                                 username=local_settings.username,
                                                 password=local_settings.password,
                                                 tenant_name=local_settings.tenant_name)
    return keystone.auth_token

print get_token()
