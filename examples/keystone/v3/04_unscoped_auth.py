#!/usr/bin/env python
# -*- coding: utf-8 -*-
import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.exceptions
import keystoneclient.session
import keystoneclient.v3.client
import requests

import local_settings

def get_unscoped_client():
    keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                               username=local_settings.username,
                                               password=local_settings.password,
                                               unscoped=True)
    return keystone

def list_user_projects(user_id, token):
    """keystoneclient好像没有封装list_user_projects，只好使用原生HTTP API了"""
    url = local_settings.auth_url_v3 + 'users/%s/projects' % user_id
    headers = {
        'X-Auth-Token': token,
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        projects = [i for i in r.json()['projects'] if i['enabled']]
        ret = (200, projects)
        # [{"description": "Admin Tenant", "links": {"self": "http://10.202.19.11:5000/v3/projects/422b53b9339f427abca6a1eab3c1cdd1"}, "enabled": true, "id": "422b53b9339f427abca6a1eab3c1cdd1", "domain_id": "default", "name": "admin"}]
    else:  # 401, ......
        ret = (r.status_code, r.json())
        # {'error': {'message': '', 'code': 401, 'title': 'Unauthorized'}}
    return ret

def main():
    """
    1. 从username、password获取unscoped token
    2. 使用unscoped token获取该用户的projects列表
    3. 使用该用户的第一个可用project生成scoped token
    4. 试试这个scoped token吧！
    """
    keystone = get_unscoped_client()
    status_code, result = list_user_projects(keystone.user_id, keystone.auth_token)
    if status_code == 200:
        auth = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                                     token=keystone.auth_token,
                                                     project_id=result[0]['id'])
        session = keystoneclient.session.Session(auth=auth)
        # 注意下面的auth_url是必须的，否则会报错
        keystone2 = keystoneclient.client.Client(auth_url=local_settings.auth_url_v3,
                                                 session=session)
        users = keystone2.users.list()
        for u in users:
            print u.domain_id, u.name

main()

