# Optical Central class file

class Central:
    def __init__(self, central_identifier):
        self.trailing_cable = Cable()
        self.central_identifier = central_identifier

    def set_trailing_cable(self, cable):
        self.trailing_cable = cable

    def set_central_identifier(self, identifier):
        self.central_identifier = identifier

    def get_trailing_cable(self):
        return self.trailing_cable

    def get_central_identifier(self):
        return self.central_identifier
