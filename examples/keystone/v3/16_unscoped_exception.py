#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.exceptions
import keystoneclient.session
import keystoneclient.v3.client

import local_settings

def get_unscoped_client(username, password):
    keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                               username=username,
                                               password=password,
                                               unscoped=True)
    return keystone

def list_user_projects_ksc(keystone):
    projects = keystone.projects.list(user=keystone.user_id)
    return projects

def main():
    # 1. 用错误的用户名获取unscoped client，抛出keystoneclient.exceptions.Unauthorized
    try:
        keystone = get_unscoped_client('fdafewjifodjas', 'fdsfds')
    except keystoneclient.exceptions.Unauthorized:
        print '1 pass'
    except:
        print '1 fail'
        traceback.print_exc()
    # 2. 正确的用户名，错误的密码：keystoneclient.exceptions.Unauthorized
    try:
        keystone = get_unscoped_client(local_settings.username, local_settings.password + 'fds')
    except keystoneclient.exceptions.Unauthorized:
        print '2 pass'
    except:
        print '2 fail'
        traceback.print_exc()
    # 3. 被禁用的用户：keystoneclient.exceptions.Unauthorized
    try:
        keystone = get_unscoped_client('inactive', 'oseasy')
    except keystoneclient.exceptions.Unauthorized:
        print '3 pass'
    except:
        print '3 fail'
        traceback.print_exc()
    return

main()

