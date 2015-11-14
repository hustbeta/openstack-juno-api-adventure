#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.session
import keystoneclient.v3.client
import novaclient.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
nova = novaclient.client.Client('2', session=session)

res = nova.keypairs.list()
print json.dumps([i.to_dict() for i in res])

