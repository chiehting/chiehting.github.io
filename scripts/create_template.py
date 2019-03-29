#!/usr/bin/env python

import os, sys, yaml, json, datetime

argv = sys.argv
yaml_data = open(os.path.dirname(os.path.realpath(__file__)) + '/templates/post_template.yaml', 'r')
data = yaml.load(yaml_data, Loader=yaml.FullLoader)


def parameter_value(key):
    values = {
        'date' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
    }
    return values.get(key, '')

parameter = ''
pages_parameter = data.get('defaule').get('parameter') + data.get('pages').get('parameter')
for key in pages_parameter:
    index,value = [key, parameter_value(key)] if isinstance(key, str) else key.popitem()
    parameter += "{}: {}\n".format(index,value)

content = '---\n{}---\n'.format(parameter);
filename = datetime.datetime.now().strftime('%Y-%m-%d-')
filename += argv[1] if len(argv) > 1 else ''

f= open(filename + '.md','w+')
f.write(content)
f.close()
