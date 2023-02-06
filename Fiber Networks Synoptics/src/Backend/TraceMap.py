# Trace Map class file
from Central import Central
from SplittingZone import SplittingZone


class TraceMap:
    def __init__(self, map_identifier, central_identifier):
        self.splitting_zones = list()
        self.fusion_junctions = list()
        self.identifier = map_identifier
        self.Central = Central(central_identifier)

    def add_splitting_zone(self, splitting_zone):
        if splitting_zone not in self.splitting_zones:
            self.splitting_zones.append(splitting_zone)

    def add_fusion_junctions(self, fusion_junction):
        if fusion_junction not in self.fusion_junctions:
            self.fusion_junctions.append(fusion_junction)

    def draw(self):
        print("Drawn")
