from openmdao.api import Group, IndepVarComp

class TorqueHoverEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

class VerticalHoverEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']
