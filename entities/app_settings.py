import datetime
import os

from google.appengine.ext import db
from google.appengine.api import users


class AppSettings(db.Model):
    """Application-wide preferences."""
    created = db.DateTimeProperty()
    last_modified = db.DateTimeProperty(auto_now=True)
    # Application settings
    domains = db.StringListProperty(required=True)
    hostname = db.StringProperty(required=True)           # used for emails
    default_private = db.BooleanProperty(default=False)   # new-user default
    default_markdown = db.BooleanProperty(default=True)   # new-user default
    default_email = db.BooleanProperty(default=True)      # new-user default
    # Chat and email settings
    email_from = db.StringProperty(default='')
    slack_channel = db.StringProperty(default='')
    slack_token = db.StringProperty(default='')
    slack_slash_token = db.StringProperty(default='')

    @staticmethod
    def get(create_if_missing=False, domains=None):
        """Return the global app settings, or raise ValueError if none found.

        If create_if_missing is true, we create app settings if none
        are found, rather than raising a ValueError.  The app settings
        are initialized with the given value for 'domains'.  The new
        entity is *not* put to the datastore.
        """
        retval = AppSettings.get_by_key_name('global_settings')
        if retval:
            return retval
        elif create_if_missing:
            # We default to sending email, and having it look like it's
            # comint from the current user.  We add a '+snippets' in there
            # to allow for filtering
            email_address = users.get_current_user().email()
            email_address = email_address.replace('@', '+snippets@')
            email_address = 'Snippet Server <%s>' % email_address
            # We also default to server hostname being the hostname that
            # you accessed the site on here.
            hostname = '%s://%s' % (os.environ.get('wsgi.url_scheme', 'http'),
                                    os.environ['HTTP_HOST'])
            return AppSettings(key_name='global_settings',
                               created=datetime.datetime.now(),
                               domains=domains,
                               hostname=hostname,
                               email_from=email_address)
        else:
            raise ValueError("Need to set global application settings.")
