# coding=utf-8
# 00_ksclient_get_auto_token_1.py

import keystoneclient.v2_0.client as ksclient
import admin_openrc as env


endpoint = env.ENDPOINT
admin_token = env.ADMIN_TOKEN


# keystone = ksclient.Client(
#     auth_url=env.OS_AUTH_URL,
#     username=env.OS_USERNAME,
#     password=env.OS_PASSWORD,
#     tenant_name=env.OS_TENANT_NAME
# )
#
# 这里换个方式,直接通过token获取权限
keystone = ksclient.Client(endpoint=endpoint, token=admin_token)

# 创建角色
user_role = keystone.roles.create("user")
admin_role = keystone.roles.create("admin")

# 创建租户
tenant = keystone.tenants.create(
    tenant_name="tenants",
    description="tenants tenants tenants",
    enabled=True
)

admin_user = keystone.users.create(
    name="admin",
    password="password",
    email="foo@bar.com",
    tenant_id=tenant.id
)
keystone.roles.add_user_role(admin_user, admin_role, tenant)

