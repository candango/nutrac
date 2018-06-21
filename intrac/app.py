import intrac.handlers
import firenado.tornadoweb

class IntracComponent(firenado.tornadoweb.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/', intrac.handlers.IndexHandler),
        ]
