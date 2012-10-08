#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from lib import randomimgur
from google.appengine.api import urlfetch
import json
import jinja2
import logging

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Handler(webapp2.RequestHandler):
    def render(self, template_name, template_values):
        template = jinja_environment.get_template(template_name)       
        self.response.out.write(template.render(template_values))

class MainHandler(Handler):
    def get(self):
        img = '/static/down.png'
        url = 'http://www.reddit.com/'
        title = 'There seems to be a problem with imgur.com'
        caption = 'Just try to kill some time at reddit.'
        while True:
            imgur = 'http://api.imgur.com'\
                    '/2/image/%s.json' % randomimgur.get_hash()
            response = urlfetch.fetch(imgur, allow_truncated=True)
            try:
                response_json = json.loads(response.content)
                if 'image' in response_json:
                    url = img = response_json['image']['links']['original']
                    title = response_json['image']['image']['title']
                    caption = response_json['image']['image']['caption']
                    break
                else:
                    logging.info('image not found.')
            except:
                logging.error('imgur down?')
                break
        self.render('templ/index.htm', {'img': img,
                                        'url': url,
                                        'title': title,
                                        'caption': caption})

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
