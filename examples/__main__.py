#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import importlib

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenStack code examples')
    parser.add_argument('package_name',
                        help='package name of the example file')
    args = parser.parse_args()
    package_name = args.package_name
    m = importlib.import_module(package_name)
