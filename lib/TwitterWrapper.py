#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import twitter


class TwitterWrapper(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
	self.dry_run = False

    def set_dry_run(self, dry_run):
        self.dry_run = dry_run

    def get_user_timeline(self, user_name, count):
        api = twitter.Api(self.username, self.password)
        return api.GetUserTimeline(user_name, count)
        
    def post_update(self, u_comment):
        if self.dry_run:
            logging.info("[dry-run]: %s (%d length)" % (u_comment, len(u_comment)))
            return None # 呟かない
        logging.info("[post_update]: %s (%d length)" % (u_comment, len(u_comment)))
        api = twitter.Api(self.username, self.password)
        return api.PostUpdate(u_comment)
    
