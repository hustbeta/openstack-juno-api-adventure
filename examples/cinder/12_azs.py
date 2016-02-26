#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import cinderclient.client
from cinderclient.v2.contrib import list_extensions

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
cinder = cinderclient.client.Client('2', session=session)

def to_dict(pool):
    ret = {
        'HUMAN_ID': pool.HUMAN_ID,
        'NAME_ATTR': pool.NAME_ATTR,
        'human_id': pool.human_id,
        'name': pool.name,
    }
    properties = dir(pool)
    for attr in ('alias', 'description', 'links', 'namespace', 'summary', 'updated'):
        if attr in properties:
            ret[attr] = getattr(pool, attr)
    return ret

manager = list_extensions.ListExtManager(cinder)
#res = manager.show_all()
#print json.dumps([to_dict(i) for i in res])
res = cinder.availability_zones.list(detailed=False)
print dir(res[0])
print json.dumps([{'zoneName': i.zoneName, 'zoneState': i.zoneState} for i in res])
#res = cinder.availability_zones.list(detailed=True)
#print res[0]

