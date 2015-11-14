#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import cinderclient.client
import keystoneclient.auth.identity.v3
import keystoneclient.session
import novaclient.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
cinder = cinderclient.client.Client('2', session=session)
nova = novaclient.client.Client('2', session=session)

server = nova.servers.get('f893cbec-b8dc-4bb4-8ee1-baa43c91bc30')
volumes = getattr(server, 'os-extended-volumes:volumes_attached')
last_letters = [u'g']
for i in volumes:
    volume = cinder.volumes.get(i['id'])
    attachments = getattr(volume, 'attachments')
    for attachment in attachments:
        device = attachment['device']
        last_letters.append(device[-1])
last_letters = sorted(list(set(last_letters)))
if last_letters:
    device_last_letter = chr(ord(last_letters[-1]) + 1)
else:
    device_last_letter = 'b'

volume = cinder.volumes.get('38fe7fea-9c20-439c-89ca-3adee472d949')
print volume, dir(volume)
ret = volume.attach('f893cbec-b8dc-4bb4-8ee1-baa43c91bc30', None)
print type(ret), dir(ret)
print ret

