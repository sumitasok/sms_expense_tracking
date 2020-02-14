matcher_1 = {
    'matcher' :{
        'expression': "^ALERT:You've spent Rs.([0-9.]+) on ([a-zA-Z\/]+) Card ([x0-9]+) at ([\sA-Za-z0-9]+) on (\d\d\d\d-\d\d-\d\d:\d\d:\d\d:\d\d)"
    },
    'identifiers': [
        {
            'key': 'price',
            'vtype': 'float'
        },
        {
            'key': 'action',
            'vtype': 'string'
        },
        {
            'key': 'account',
            'vtype': 'string'
        },
        {
            'key': 'merchant',
            'vtype': 'string'
        },
        {
            'key': 'datetime',
            'vtype': 'datetime',
            'format': '%Y-%m-%d:%H:%M:%S'
        }
    ]
}

import re

def parse(txt, matcher):
    x = re.findall(matcher['matcher']['expression'], txt)

    analytics = {}
    for i, value in enumerate(x[0]):
        analytics[matcher['identifiers'][i]['key']] = value

    return analytics

# parse(txt, matcher_1)