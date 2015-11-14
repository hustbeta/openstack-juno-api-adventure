#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.exceptions
import keystoneclient.session
import keystoneclient.v3.client
import novaclient.client

import local_settings

def get_unscoped_client():
    keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                               #username=local_settings.username,
                                               username='demo',
                                               password=local_settings.password,
                                               unscoped=True)
    return keystone

def list_user_projects(keystone):
    projects = keystone.projects.list(user=keystone.user_id)
    return projects

def main():
    """
    1. 从username、password获取unscoped token
    2. 使用unscoped token获取该用户的projects列表
    3. 使用该用户的第一个可用project生成scoped token
    4. 试试这个scoped token吧！
    """
    keystone = get_unscoped_client()
    keystone.management_url = local_settings.auth_url_v3
    projects = list_user_projects(keystone)
    auth = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                                 token=keystone.auth_token,
                                                 project_id=projects[0].id)
    session = keystoneclient.session.Session(auth=auth)
    nova = novaclient.client.Client('2', session=session)
    print json.dumps([i.to_dict() for i in nova.flavors.list()])
    auth2 = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                                   token=session.get_token(),
                                                   project_id=projects[1].id)
    session2 = keystoneclient.session.Session(auth=auth2)
    nova2 = novaclient.client.Client('2', session=session2)
    print json.dumps([i.to_dict() for i in nova2.flavors.list()])

main()

