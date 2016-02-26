#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import time

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

server = nova.servers.create(name='test-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                             min_count=1,
                             image='397ceee8-ee08-4919-b163-d10c20b42029',
                             flavor='465c0d60-b4f9-4adb-ba68-a6a4ec9a835d',
                             meta={'description': 'fdsfsdfsdf'},
                             availability_zone='pulsar',
                             nics=[{'net-id': '3961edd3-99e1-4d3e-abac-9069c85d1aa6'}])

server_id = server.id
ret = []
i = 0
while True:
    progress = nova.servers.get(server_id)
    if progress.status != 'ACTIVE':
        i += 1
        print i
        ret.append(progress.to_dict())
        time.sleep(1.0)
    else:
        break

print json.dumps(ret)

