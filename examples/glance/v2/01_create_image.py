#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import glanceclient

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
glance = glanceclient.Client('2', session=session)

image = glance.images.create(name='testfdsf$-!@#$%^&*(){}[]"":;龘',
                             container_format='bare',
                             description='description...',
                             disk_format='qcow2',
                             min_disk=1,
                             min_ram=128,
                             os_distro='ubuntu',
                             protected=True,
                             visibility='public')
print image

