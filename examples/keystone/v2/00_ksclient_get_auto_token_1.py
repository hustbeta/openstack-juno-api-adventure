# coding=utf-8
# 00_ksclient_get_auto_token_1.py

import keystoneclient.v2_0.client as ksclient
import admin_openrc as env
# import demo_openrc as env

keystone = ksclient.Client(
    auth_url=env.OS_AUTH_URL,
    username=env.OS_USERNAME,
    password=env.OS_PASSWORD,
    tenant_name=env.OS_TENANT_NAME
)
                           
print keystone.auth_token
