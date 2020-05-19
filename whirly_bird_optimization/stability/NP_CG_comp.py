from openmdao.api import ExplicitComponent


class NPCGComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('')