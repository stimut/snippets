import hashlib

from google.appengine.ext import db


class Snippet(db.Model):
    """Every snippet is identified by the monday of the week it goes with."""
    created = db.DateTimeProperty()
    last_modified = db.DateTimeProperty(auto_now=True)
    display_name = db.StringProperty()        # display name of the user
    email = db.StringProperty(required=True)  # week+email: key to this record
    week = db.DateProperty(required=True)     # the monday of the week
    text = db.TextProperty()
    private = db.BooleanProperty(default=False)       # snippet is private?
    is_markdown = db.BooleanProperty(default=False)   # text is markdown?

    @property
    def email_md5_hash(self):
        m = hashlib.md5()
        m.update(self.email)
        return m.hexdigest()
