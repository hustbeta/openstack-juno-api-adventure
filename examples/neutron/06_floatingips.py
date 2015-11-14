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
    q = neutron.list_floatingips(tenant_id='422b53b9339f427abca6a1eab3c1cdd1',
                                 fields=['id'])
    #q = neutron.list_pools()
    print type(q)
    print json.dumps(q)

session = get_session()
test_neutron(session)

