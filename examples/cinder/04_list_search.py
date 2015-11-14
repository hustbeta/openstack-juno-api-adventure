#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import cinderclient.client

import local_settings

def to_dict(volume):
    """volume没有to_dict()方法，这里加一个，方便转为json"""
    attrs = ['attachments', 'availability_zone', 'bootable', 'consistencygroup_id',
             'created_at', 'description', 'encrypted', 'id', 'links', 'metadata', 'name',
             'os-vol-host-attr:host', 'os-vol-mig-status-attr:migstat',
             'os-vol-mig-status-attr:name_id', 'os-vol-tenant-attr:tenant_id',
             'os-volume-replication:driver_data', 'os-volume-replication:extended_status',
             'replication_status', 'size', 'snapshot_id', 'source_volid', 'status',
             'user_id', 'volume_type']
    return {attr: getattr(volume, attr) for attr in attrs}

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
cinder = cinderclient.client.Client('2', session=session)

q = cinder.volumes.list(search_opts={'project_id': '422b53b9339f427abca6a1eab3c1cdd1'})
#q = cinder.volumes.list(search_opts={'volume_type': 'sata'})
#q = cinder.volumes.list()
#q = cinder.volumes.list(search_opts={'tenant_id': '4f55e99ec6d444bc904acfe358eaac09'})
#q = cinder.volumes.list(search_opts={'os-vol-tenant-attr:tenant_id': '4f55e99ec6d444bc904acfe358eaac09'})
print json.dumps([to_dict(i) for i in q])

