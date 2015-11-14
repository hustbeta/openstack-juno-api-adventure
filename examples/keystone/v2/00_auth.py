#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Authenticate using v2.0 API, get token"""
import keystoneclient.v2_0.client

import local_settings

def get_token():
    keystone = keystoneclient.v2_0.client.Client(auth_url=local_settings.auth_url_v2,
                                                 username=local_settings.username,
                                                 password=local_settings.password,
                                                 tenant_name=local_settings.tenant_name)
    return keystone

keystone = get_token()
print keystone.auth_token
print keystone
print keystone.users.get('d6a5511a2fd546269cf7c3903b1fe0aa').to_dict()
