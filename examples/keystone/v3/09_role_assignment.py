#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.exceptions
import keystoneclient.session
import keystoneclient.v3.client

import local_settings

def get_unscoped_client():
    keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                               username=local_settings.username,
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
    # 注意下面的auth_url是必须的，否则会报错
    keystone2 = keystoneclient.client.Client(auth_url=local_settings.auth_url_v3,
                                             session=session)
    projects = keystone2.projects.list()
    for project in projects:
        print 'project:', project.id, project.name
        print json.dumps([i.to_dict() for i in keystone2.role_assignments.list(project=project)])
        print '-' * 40
    ra = keystone2.role_assignments.list(project='4f55e99ec6d444bc904acfe358eaac09')[0]
    print type(ra.user), type(ra.role)

main()

