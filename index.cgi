#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/path/to/lib/python')

import re
import datetime
import urllib2
import random
import logging
import logging.handlers
import traceback
import cgi
import cgitb; cgitb.enable()

import twitter
from genshi.template import TemplateLoader
from genshi.template import TextTemplate


from lib import TwitterWrapper


TWITTER_USERNAME = "idounokiseki"
TWITTER_PASSWORD = ""

LOG_FILE = "tweet.log"
g_dry_run = False


imakoko_p = re.compile(u'^.*L:(.+)\s*')
kuten_p = re.compile(u'.+[\.。](.+)')
nau_p = re.compile(u'(.+)なう[\.。]?')
num_p = re.compile(u'(.+)[1234567890１２３４５６７８９０]+$')
line_break_p = re.compile(u'\n')
d_quote_p = re.compile(u'"')
link_p = re.compile(u'(https?://.+)[ 　]')


def get_error_msg():
    msgs = [u"へるぷみー、検索できないよ！"]
    return u"%s (%s)" % (random.choice(msgs), datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"))


class Render(object):
    def error_html(self):
        print 'Content-Type: text/html; charset=utf-8\n'

        loader = TemplateLoader(['./templates/'])
        tmpl = loader.load('error.html.tmpl')
        stream = tmpl.generate(error_msg=get_error_msg())
        print stream.render('html', doctype='html-transitional', strip_whitespace=False)

    def index_html(self, name, result_dic):
        print 'Content-Type: text/html; charset=utf-8\n'
        
        loader = TemplateLoader(['./templates/'])
        tmpl = loader.load('index.html.tmpl')
        list = []
        for k in result_dic.keys():
            list.append('"%s": "%s"' % (k, result_dic[k]))
        
        stream = tmpl.generate(name=name, datas="{%s}" % ','.join(list))
        print stream.render('html', doctype='html-transitional', strip_whitespace=False)


def search(name):
    dic = {}
    if name is None:
        # 検索対象なし
        return {}

    # Twitter から指定ユーザの呟きを検索
    t_wrapper = None
    try:
        t_wrapper = TwitterWrapper.TwitterWrapper(TWITTER_USERNAME, TWITTER_PASSWORD)
	t_wrapper.set_dry_run(g_dry_run)
	
	statuses = t_wrapper.get_user_timeline(name, 20)
	for s in statuses:
	    # イマココ
	    m = imakoko_p.search(s.text)
	    if m:
	        location = m.group(1)
		text = line_break_p.sub('<br>', s.text)
		text = d_quote_p.sub('\\"', text)
		dic[location] = text
	    else:
	        # なう
	        m = nau_p.search(s.text)
		if m:
		    location = m.group(1)
		    kuten_m = kuten_p.search(location)
		    if kuten_m:
		        location = kuten_m.group(1)
		    text = line_break_p.sub('<br>', s.text)
		    text = d_quote_p.sub('\\"', text)
		    dic[location] = text
	return dic
    except urllib2.HTTPError, e:
        # なぜかこのエラーになる場合がある
        logging.error("http exception!")
        for line in traceback.format_exc().splitlines():
            logging.error(line)
    except:
        logging.error("unknown exception!")
        for line in traceback.format_exc().splitlines():
            logging.error(line)
        raise
        

def request_dispatch():
    render = Render()
    try:
        req_form = cgi.FieldStorage()
	name = req_form.getvalue('name', None)
	if req_form.has_key('name'):
	    name = cgi.escape(name)
	result_dic = search(name)
	render.index_html(name, result_dic)
    except:
        render.error_html()


def main():
    # TimedRotating は設定通りに rotate されないので、バグっている気がするが、しばらくこのままで
    timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, "D", 7, 15, "utf8")
    # こちらは出来ているっぽい
    #log_handler = logging.handlers.RotatingFileHandler(LOG_FILE, "a", 100, 5, "utf8")
    timed_rotating_handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-7s %(message)s"))
    stream_handler = logging.StreamHandler()
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(timed_rotating_handler)
    #root.addHandler(stream_handler)

    logging.info("== idounokiseki start ==")
    request_dispatch()
    logging.info("== idounokiseki finish ==")


if __name__ == "__main__":
    main()

