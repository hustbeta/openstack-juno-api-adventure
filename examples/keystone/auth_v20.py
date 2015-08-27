#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Authenticate using v2.0 API, get token"""
import keystoneclient.v2_0.client

import local_settings

keystone = keystoneclient.v2_0.client.Client(auth_url=local_settings.auth_url,
                                             username=local_settings.username,
                                             password=local_settings.password,
                                             tenant_name=local_settings.tenant_name)
print keystone.auth_token
