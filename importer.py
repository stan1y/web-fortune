import logging
import datetime

from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import util

from fortune import Wisdom

log = logging.getLogger(__name__)

class ImportHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            logging.warn('upload with no logged in user')
            print 'Not logged in'
            return
        
        upload_files = self.get_uploads('file')
        source = self.request.get("source")
        format = self.request.get("format")
        
        if len(upload_files) < 1:
            logging.warn('no file uploaded')
            self.redirect("/")
            return
            
        blob = upload_files[0]
        logging.info('received file %s as %s' % (source, format))
        
        blobReader = blob.open()
        for wisdomText in blobReader:
            wisdomText = wisdomText.strip().decode('utf-8')
            logging.debug('processing [%s]' % wisdomText)
            wisdom = Wisdom(source = source,
                format = format,
                owner = user,
                uploadedOn = datetime.date.today(),
                text = wisdomText)
            wisdom.put()
        self.redirect('/')
