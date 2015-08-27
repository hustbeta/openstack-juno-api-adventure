#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

import local_settings

def details():
    r = requests.get(local_settings.auth_url_v3)
    if r.status_code == 200:
        return r.json()

print details()

