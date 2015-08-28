#!/usr/bin/env python
# -*- coding: utf-8 -*-
import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.session
import keystoneclient.v3.client
import novaclient.v2.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
nova = novaclient.v2.client.Client(session=session)

print dir(nova)
for version in nova.versions.list():
    print version.__dict__
