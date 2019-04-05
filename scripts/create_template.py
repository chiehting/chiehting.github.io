#!/usr/bin/env python

import os, yaml, json, datetime

yaml_data = open(os.path.dirname(os.path.realpath(__file__)) + '/configuration/post_template.yaml', 'r')
data = yaml.load(yaml_data, Loader=yaml.FullLoader)
file_types = {'1':'post','2':'page'}

filename = input("file name: ") or "tmp"
file_type = input("file type (1:post, 2:page): ") or '1'

def parameter_value(key):
    values = {
        'date' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
    }
    return values.get(key, '')

parameter = ''
pages_parameter = data.get('defaule').get('parameter') + data.get(file_types[file_type]).get('parameter')
for key in pages_parameter:
    index,value = [key, parameter_value(key)] if isinstance(key, str) else key.popitem()
    parameter += "{}: {}\n".format(index,value)

content = '---\n{}---\n'.format(parameter);
filename = datetime.datetime.now().strftime('%Y-%m-%d-') + filename

f= open(filename + '.md','w+')
f.write(content)
f.close()
