#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

import local_settings

def requests_versions():
    r = requests.get(local_settings.nova_url)
    '''
    r.json() looks like:
    {
        'versions': [
            {
                'id': 'v2.0',
                'links': [
                    {
                        'href': 'http://10.202.19.11:8774/v2/',
                        'rel': 'self'
                    }
                ],
                'status': 'CURRENT',
                'updated': '2011-01-21T11:33:21Z'
            }
        ]
    }
    '''
    # It seems that Juno only exposes V2.0 API
    if r.status_code == 200:
        return r.json()
    else:
        print 'error', r.status_code
        print r.headers
        print r.text

print requests_versions()

