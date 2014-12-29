#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2
import logging

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

"""BeautifulSoup のインスタンスを作るためのメソッド群"""

LWWS_URL = "http://weather.livedoor.com"
IGNORE_SCRIPT_TAG_P = re.compile(u"<script (.+\n)+</script>")


def get_day_forecast(day_name):
    #f = open('html/%s.xml' % day_name)
    url = "%s/forecast/webservice/rest/v1?city=63&day=%s" % (LWWS_URL, day_name)
    logging.info("[url]: %s" % url)
    f = urllib2.urlopen(url)
    bs = BeautifulStoneSoup(f.read())
    f.close()
    return bs

def get_week_forecast():
    #f = open('html/week.xml')
    url = "%s/forecast/rss/13/63.xml" % LWWS_URL
    logging.info("[url]: %s" % url)
    f = urllib2.urlopen(url)
    bs = BeautifulStoneSoup(f.read())
    f.close()
    return bs

def get_zenkoku_forecast():
    #f = open('html/zenkoku.xml')
    url = "%s/forecast/rss/index.xml" % LWWS_URL
    logging.info("[url]: %s" % url)
    f = urllib2.urlopen(url)
    bs = BeautifulStoneSoup(f.read())
    f.close()
    return bs

def get_index_information(target):
    #f = open('html/%s.html' % target)
    url = "%s/indexes/%s/13/63.html" % (LWWS_URL, target)
    logging.info("[url]: %s" % url)
    f = urllib2.urlopen(url)
    u_striped_content = IGNORE_SCRIPT_TAG_P.sub(u"", f.read().decode("euc-jp"))
    bs = BeautifulSoup(u_striped_content)
    f.close()
    return bs

def get_warn_information():
    #f = open('html/warn.html')
    url = "%s/warn/13.html" % LWWS_URL
    logging.info("[url]: %s" % url)
    f = urllib2.urlopen(url)
    u_striped_content = IGNORE_SCRIPT_TAG_P.sub(u"", f.read().decode("euc-jp"))
    bs = BeautifulSoup(u_striped_content)
    f.close()
    return bs

def get_warn_history(location_id):
    #f = open('html/%d.html' % location_id)
    url ="%s/warn/13/%d.html" % (LWWS_URL, location_id)
    logging.info("[url]: %s" % url)
    f = urllib2.urlopen(url)
    u_striped_content = IGNORE_SCRIPT_TAG_P.sub(u"", f.read().decode("euc-jp"))
    bs = BeautifulSoup(u_striped_content)
    f.close()
    return bs


if __name__ == "__main__":
    print get_day_forecast('today')
    print get_day_forecast('tomorrow')
    print get_day_forecast('dayaftertomorrow')
    print get_week_forecast()
    print get_zenkoku_forecast()
    print get_index_information('star')
    print get_warn_information()
    print get_warn_history()
