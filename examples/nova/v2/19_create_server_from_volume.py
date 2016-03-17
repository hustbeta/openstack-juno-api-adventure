#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
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

server = nova.servers.create('test-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                             None, 'a62526d0-363e-400d-81bf-37b1c1ab033e',
                             meta={'description': 'fdsfsdfsdf'},
                             min_count=1, max_count=1,
                             availability_zone='nova',
                             block_device_mapping_v2=[{
                                 'boot_index': 0,
                                 'device_name': '/dev/vda',
                                 'uuid': 'ec315455-8d70-42e4-b443-f6e32fa46844',
                                 'source_type': 'volume',
                                 'destination_type': 'volume',
                                 #'volume_size': 1,
                             }],
                             nics=[{'net-id': '94da5a5a-d09c-496d-bb4b-c0bd79270f2c'}])
print json.dumps(server.to_dict())

