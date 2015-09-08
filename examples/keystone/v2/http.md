在阅读文档之前,首先应当对`HTTP`协议请求的一些常用方式有一定的了解.

### HTTP协议请求方式
```
GET:    请求指定的页面信息，并返回实体主体。
HEAD:   只请求页面的首部。
POST:   请求服务器接受所指定的文档作为对所标识的URI的新的从属实体。
PUT:    从客户端向服务器传送的数据取代指定的文档的内容。
DELETE: 请求服务器删除指定的页面。
OPTIONS:允许客户端查看服务器的性能。
TRACE:  请求服务器在响应中的实体主体部分返回所得到的内容。
PATCH:  实体中包含一个表，表中说明与该URI所表示的原内容的区别。
MOVE:   请求服务器将指定的页面移至另一个网络地址。
COPY:   请求服务器将指定的页面拷贝至另一个网络地址。
LINK:   请求服务器建立链接关系。
UNLINK: 断开链接关系。
WRAPPED:允许客户端发送经过封装的请求。
Extension-mothed:在不改动协议的前提下，可增加另外的方法。
```
---

### [Identyty API V3](http://developer.openstack.org/api-ref-identity-v3.html)
1. **Aokens**
1. **Service catalog**
1. **Endpoints**
1. **Domains**
1. **Projects**
1. **Users**
1. **Groups**
1. **Credentials**
1. **Roles**
1. **Policies**

OpenStack Identify V3部分的API都是有一定的规律的,
基本上都是通过request.method来判断进行什么样的操作,
总的来说 在**POST**和**PUT**的时候进行新增操作,
在**GET**的时候进行查询操作,在**PATCH**的时候进行更新操作,
在**DELETE**的时候进行删除操作.