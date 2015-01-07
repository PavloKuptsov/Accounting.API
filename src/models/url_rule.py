class UrlRule(object):
    url = u''
    view = None
    name = u''

    def __init__(self, url, view, name):
        self.url = url
        self.view = view
        self.name = name