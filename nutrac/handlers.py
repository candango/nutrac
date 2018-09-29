from firenado import tornadoweb


class IndexHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.render("index.html")


class ProfileHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("Profile output")


class HomeHandler(tornadoweb.TornadoHandler):

    def get(self, user):
        self.write("Home output %s" % user)
