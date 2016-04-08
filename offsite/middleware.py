# -*- coding: utf-8 -*-
'''
Created on 29 марта 2016 г.

@author: gudach
'''

import logging
import logging.handlers
from django.conf import settings
from ipware.ip import get_ip, get_real_ip

bytes=1024000
count=10
formatter = logging.Formatter("%(asctime)s-%(message)s")

MODELS_FILE = settings.BASE_DIR + '/users.log'
logmodels = logging.getLogger('users')
logmodels.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(MODELS_FILE, maxBytes=bytes, backupCount=count)
handler.setFormatter(formatter)
logmodels.addHandler(handler)


class TrackUsersMiddleware(object):

    def process_request(self, request):
        ip = get_real_ip(request, right_most_proxy=True) or get_ip(request, right_most_proxy=True)
        city = request.META.get('GEOIP_COUNTRY_CODE')
        logmodels.debug('%s %s %s' %(request.path, ip, city))
        