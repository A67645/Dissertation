# Splitting Zone or JSO Zone class file
from Cable import Cable


class SplittingZone:

    def __init__(self):  # Instance Variables definition
        self.leading_cable = Cable()  # Cable entering the splitting zone
        self.trailing_cables = list()  # Cables exiting the splitting zone
        self.pdo_list = list()

    def add_trailing_cable(self, cable):
        if cable not in self.trailing_cables:
            self.trailing_cables.append(cable)

    def add_pdo(self, pdo):
        if pdo not in self.pdo_list:
            self.pdo_list.append(pdo)
