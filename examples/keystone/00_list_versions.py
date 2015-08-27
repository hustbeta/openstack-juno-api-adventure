#!/usr/bin/env python
# -*- coding: utf-8 -*-
import keystoneclient.discover
import requests

import local_settings

def requests_versions():
    r = requests.get(local_settings.admin_auth_url)
    '''
    r.json() looks like:
    {
        "versions": {
            "values": [
                {
                    "id": "v3.0",
                    "links": [
                        {
                            "href": "http://10.202.19.11:5000/v3/",
                            "rel": "self"
                        }
                    ],
                    "media-types": [
                        {
                            "base": "application/json",
                            "type": "application/vnd.openstack.identity-v3+json"
                        },
                        {
                            "base": "application/xml",
                            "type": "application/vnd.openstack.identity-v3+xml"
                        }
                    ],
                    "status": "stable",
                    "updated": "2013-03-06T00:00:00Z"
                },
                {
                    "id": "v2.0",
                    "links": [
                        {
                            "href": "http://10.202.19.11:5000/v2.0/",
                            "rel": "self"
                        },
                        {
                            "href": "http://docs.openstack.org/",
                            "rel": "describedby",
                            "type": "text/html"
                        }
                    ],
                    "media-types": [
                        {
                            "base": "application/json",
                            "type": "application/vnd.openstack.identity-v2.0+json"
                        },
                        {
                            "base": "application/xml",
                            "type": "application/vnd.openstack.identity-v2.0+xml"
                        }
                    ],
                    "status": "stable",
                    "updated": "2014-04-17T00:00:00Z"
                }
            ]
        }
    }
    '''
    if r.status_code in (200, 300):
        # official docs says the status code should be 200,
        # while on my Juno the status code is 300
       return r.json()
    else:
        print 'error', r.status_code
        print r.headers
        print r.text

def keystoneclient_versions():
    # same as r.json()['versions']['values']
    return keystoneclient.discover.available_versions(local_settings.auth_url)

print keystoneclient_versions()

