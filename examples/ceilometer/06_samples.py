#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.session
import keystoneclient.v3.client
import ceilometerclient.client

import local_settings

keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                           username=local_settings.username,
                                           password=local_settings.password,
                                           unscoped=True)
keystone.management_url = local_settings.auth_url_v3
projects = keystone.projects.list(user=keystone.user_id)
auth = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                             token=keystone.auth_token,
                                             project_id=projects[0].id)
session = keystoneclient.session.Session(auth=auth)

client = ceilometerclient.client.get_client('2',
                                            token=session.get_token(),
                                            ceilometer_url='http://10.202.19.11:8777')
res = client.samples.list(meter_name='cpu_util',
                          q=[{
                              'field': 'resource_id',
                              'value': 'b2c8de4a-e6d9-430f-b961-a65025d24574',
                          }],
                          limit=10)
print type(res[0].counter_volume)
print type(res[0].timestamp)
print json.dumps([i.to_dict() for i in res])

