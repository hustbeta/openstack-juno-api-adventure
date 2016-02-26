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

def pool_to_dict(pool):
    ret = {
        'HUMAN_ID': pool.HUMAN_ID,
        'NAME_ATTR': pool.NAME_ATTR,
        'human_id': pool.human_id,
        'name': pool.name,
    }
    properties = dir(pool)
    for attr in ('QoS_support', 'allocated_capacity_gb', 'driver_version',
                 'free_capacity_gb', 'location_info', 'pool_name',
                 'reserved_percentage', 'storage_protocol', 'timestamp',
                 'total_capacity_gb', 'vendor_name', 'volume_backend_name'):
        if attr in properties:
            ret[attr] = getattr(pool, attr)
    return ret

res = cinder.pools.list(detailed=False)
print json.dumps([pool_to_dict(i) for i in res])
res = cinder.pools.list(detailed=True)
print json.dumps([pool_to_dict(i) for i in res])

