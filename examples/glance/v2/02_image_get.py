#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import glanceclient

import local_settings

auth = keystoneclient.auth.identity.v3.Password(#auth_url=local_settings.auth_url_v3,
                                                auth_url='http://192.168.65.10:5000/v3',
                                                username=local_settings.username,
                                                #password=local_settings.password,
                                                password='ADMIN_PASS',
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
glance = glanceclient.Client('2', session=session)

image = glance.images.get('397ceee8-ee08-4919-b163-d10c20b42029')
print image, dir(image)

