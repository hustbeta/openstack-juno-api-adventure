# coding=utf-8
# 00_ksclient_get_auto_token.py

import keystoneclient.v2_0.client as ksclient

keystone = ksclient.Client(
    auth_url='http://10.0.0.11:35357/v2.0',
    username='admin',
    password='admin_pass',
    tenant_name='admin'
)

print keystone.auth_token


print keystone.users.list()
print keystone.roles.list()
print keystone.tenants.list()
print keystone.services.list()
print keystone.endpoints.list()
print keystone.extensions.list()
'''
[<User {u'username': u'glance', u'id': u'7048295efa6a468e9ee46492e6b1e441', u'enabled': True, u'name': u'glance', u'email': None}>, 
<User {u'username': u'demo', u'name': u'demo', u'enabled': True, u'tenantId': u'41c264c22adb4a69aa059d74066f74c4', u'id': u'bcddf434d142466a9229983863faa9b9', u'email': u'foo@bar.com'}>, 
<User {u'username': u'admin', u'id': u'fe879d74165a45fb818f6c392ee87788', u'enabled': True, u'name': u'admin', u'email': u'foo@bar.com'}>]
'''
