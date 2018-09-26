from firenado import tornadoweb


class IndexHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("IndexHandler output")


class ProfileHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("Profile output")


class ProjectsHandler(tornadoweb.TornadoHandler):

    def get(self, user):
        self.write("Projects output %s" % user)
