#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import cinderclient.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
cinder = cinderclient.client.Client('2', session=session)

q = cinder.volume_snapshots.list(search_opts={'os-extended-snapshot-attributes:project_id': '4f55e99ec6d444bc904acfe358eaac09'})
#q = cinder.volume_snapshots.list(search_opts={'name': '2222222'})
print json.dumps([{
    'created_at': i.created_at,
    'description': i.description,
    'human_id': i.human_id,
    'id': i.id,
    'metadata': i.metadata,
    'name': i.name,
    'os-extended-snapshot-attributes:progress': getattr(i, 'os-extended-snapshot-attributes:progress'),
    'os-extended-snapshot-attributes:project_id': getattr(i, 'os-extended-snapshot-attributes:project_id'),
    'progress': i.progress,
    'project_id': i.project_id,
    'size': i.size,
    'status': i.status,
    'volume_id': i.volume_id,
} for i in q])

