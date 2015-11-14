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
alarm = client.alarms.get('57a8b4c2-ae6c-4341-940b-0f87277d9378')
alarm_id = alarm.alarm_id
print json.dumps(alarm.to_dict())
operators = ['lt', 'le', 'eq', 'ne', 'gt', 'ge']
operators.remove(alarm.threshold_rule['comparison_operator'])
meters = ['cpu_util', 'disk.read.bytes.rate', 'disk.write.bytes.rate']
meters.remove(alarm.threshold_rule['meter_name'])
threshold = [11.1, 22.2, 33.3, 44.4, 55.5, 66.6, 77.7, 88.8, 99.9]
threshold.remove(alarm.threshold_rule['threshold'])
new_alarm = client.alarms.update(alarm_id,
                                 description='new description-%d' % random.randint(1, 5000),
                                 enabled=not alarm.enabled,
                                 comparison_operator=random.choice(operators),
                                 meter_name=random.choice(meters),
                                 threshold=random.choice(threshold))
print json.dumps(new_alarm.to_dict())

