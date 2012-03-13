import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Wisdom(db.Model):
  source = db.StringProperty(required=True)
  text = db.StringProperty(required=True)
  format = db.StringProperty(required=True, 
    choices=set(["plain", "markdown"]))
  uploadedOn = db.DateProperty(required=True)
  owner = db.UserProperty(required=True)
  
  