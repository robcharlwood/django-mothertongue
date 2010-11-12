VERSION = (0, 0, 6)
AUTHOR = "Rob Charlwood"
COPYRIGHT = "2010"
PROJECT_NAME = "mothertongue"

def get_version(svn=False, limit=3):
    "Returns the version as a human-format string."
    v = '.'.join([str(i) for i in VERSION[:limit]])
    if svn and limit >= 3:
        from django.utils.version import get_svn_revision
        import os
        svn_rev = get_svn_revision(os.path.dirname(__file__))
        if svn_rev:
            v = '%s.%s' % (v, svn_rev)
    return v

def get_author():
    return u'%s' % AUTHOR

def get_copyright():
    return u'%s' % COPYRIGHT

def get_appname():
    return u'%s' % PROJECT_NAME    