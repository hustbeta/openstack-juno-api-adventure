#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import keystoneclient.v3.client
import neutronclient.neutron.client

import local_settings

def get_session():
    keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                               username=local_settings.username,
                                               password=local_settings.password,
                                               unscoped=True)
    keystone.management_url = keystone.auth_url
    projects = keystone.projects.list(user=keystone.auth_ref.user_id)
    projects.sort(key=lambda project: project.name.lower())

    auth = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                                 token=keystone.auth_token,
                                                 project_id=projects[0].id)
    session = keystoneclient.session.Session(auth=auth)

    return session

def test_neutron(session):
    neutron = neutronclient.neutron.client.Client('2.0', session=session)
    print json.dumps(neutron.list_ports(device_id='49e06f25-fe57-4223-8703-5b4a2b3d4fdb'))
    for port in neutron.list_ports(device_id='49e06f25-fe57-4223-8703-5b4a2b3d4fdb')['ports']:
        print type(port)
    print neutron.delete_port('392cb454-7fef-4f53-b89a-b6aebbaad10b')

session = get_session()
test_neutron(session)

