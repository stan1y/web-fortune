import random
import time
import datetime

from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from fortune import Wisdom

class TellHandler(webapp.RequestHandler):
    def get(self):
        random.seed(time.time())
        format = self.request.get("format")
        if not format: 
            format = 'html'
        
        countQuery = Wisdom.all()
        
        owner = self.request.get("owner")
        if owner: 
            countQuery.filter('owner =', owner)
        
        count = countQuery.count()
        if not count:
            self.response.out.write('It appreas that there is no wisdom with specified parameters.')
            return
            
        index = random.randint(1, count - 1)
        wisdom = Wisdom.all().fetch(offset=index, limit=1)[0]
        if format == 'json':
            self.response.headers['Content-Type'] = "application/json";
            self.response.out.write(json.dumps({
                'wisdom': wisdom.text,
                'owner': wisdom.owner.nickname(),
                'uploadedOn': wisdom.uploadedOn.strftime('%d-%m-%Y')
            }))
        elif format == 'jsonp':
            callback = self.request.get("callback")
            if not callback:
                callback = self.request.get("jsonp")
            if not callback:
                self.response.out.write('Please specify callback or jsonp argument to get padded json.')
                return
            self.response.headers['Content-Type'] = "text/javascript";
            prefix = "%s(" % callback if callback != '?' else '('
            self.response.out.write(prefix + json.dumps({
                'wisdom': wisdom.text,
                'owner': wisdom.owner.nickname(),
                'uploadedOn': wisdom.uploadedOn.strftime('%d-%m-%Y')
            }) + ");")
        elif format == 'html':
            self.response.out.write(template.render("templates/wisdom.html", {
                "wisdomText" : wisdom.text
            }))
        else: #plain
            self.response.headers['Content-Type'] = "text/plain";
            self.response.out.write(wisdom.text)
            
