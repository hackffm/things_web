import tornado.web


class HandlerThingsPage(tornado.web.RequestHandler):
    def initialize(self, helper, port, nodes_handler, debug=False):
        self.debug = debug
        self.helper = helper
        self.name = 'HandlerThings'
        self.port = port
        self.nodes_handler = nodes_handler

    def get(self):
        ip_first = self.helper.interfaces_first()
        things_qty = 0
        things_verified = []
        nodes_verified = []
        nodes_not_verified =[]
        self.nodes_handler.nodes_verify()
        for ns in self.nodes_handler.nodes_not_verified:
            nodes_not_verified.append([ns.id])
        for ns in self.nodes_handler.nodes_verified:
            nodes_verified.append([ns.id])
            for thing in ns.things:
                things_verified.append([ns.id, thing.id])
                things_qty += 1

        if self.debug:
            print(self.name)
            print('things verified\n' + str(things_verified))
            print('things not verified\n' + str(nodes_not_verified))
        self.render("things.html",
                    ip_first=ip_first,
                    title=self.name,
                    port=self.port,
                    things_verified=things_verified,
                    nodes_not_verified=nodes_not_verified,
                    nodes_verified=nodes_verified,
                    things_qty=things_qty)
