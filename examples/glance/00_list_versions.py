#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

import local_settings

def requests_versions():
    r = requests.get(local_settings.glance_url)
    '''
    r.json() looks like:
    {
        "versions": [
            {
                "status": "CURRENT",
                "id": "v2.2",
                "links": [{"href": "http://10.202.19.11:9292/v2/", "rel": "self"}]
            },
            {
                "status": "SUPPORTED",
                "id": "v2.1",
                "links": [{"href": "http://10.202.19.11:9292/v2/", "rel": "self"}]
            },
            {
                "status": "SUPPORTED",
                "id": "v2.0",
                "links": [{"href": "http://10.202.19.11:9292/v2/", "rel": "self"}]
            },
            {
                "status": "CURRENT",
                "id": "v1.1",
                "links": [{"href": "http://10.202.19.11:9292/v1/", "rel": "self"}]
            },
            {
                "status": "SUPPORTED",
                "id": "v1.0",
                "links": [{"href": "http://10.202.19.11:9292/v1/", "rel": "self"}]
            }
        ]
    }
    '''
    if r.status_code == 300:
        return r.json()
    else:
        print 'error', r.status_code
        print r.headers
        print r.text

print requests_versions()

