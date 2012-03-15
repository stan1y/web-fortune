#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import users

from importer import ImportHandler
from teller import TellHandler
from fortune import Wisdom

class UploadHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/"))
            return
            
        username = user.nickname()
        upload_url = blobstore.create_upload_url("/import") 
        self.response.out.write(template.render("templates/upload.html", {
            "username" : username,
            "upload_url": upload_url
        }))

class MainHandler(webapp.RequestHandler):
    def get(self):
        
        page_num = self.request.get('page_num')
        if not page_num: 
            page_num = 1
        else:
            page_num = int(page_num)
        page_size = self.request.get('page_size')
        if not page_size: 
            page_size = 50
        else:
            page_size = int(page_size)
        
        user = users.get_current_user()
        if user:
            username = user.nickname()
            wisdoms_count = Wisdom.all().filter("owner =", user).count()
            wisdoms_page = Wisdom.all().fetch(offset = (page_num - 1) * page_size, limit = page_size )
        else:
            username = None
            wisdoms_page = None
            wisdoms_count = 0

        total_wisdoms_count = Wisdom.all().count()
        
        self.response.out.write(template.render("templates/index.html", {
            "username" : username,
            "login_url" : users.create_login_url("/"),
            "logout_url" : users.create_logout_url("/"),
            "wisdoms_count" : wisdoms_count,
            "wisdoms_page" : wisdoms_page,
            "total_wisdom_count": total_wisdoms_count,
            "page_size": page_size,
            "page_num": page_num,
            "first_page": page_num == 1,
            "prev_page": page_num - 1,
            "next_page": page_num + 1
        }))

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/upload', UploadHandler),
        ('/import', ImportHandler),
        ('/tell', TellHandler)
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
