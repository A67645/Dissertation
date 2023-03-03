# Trace Map class file
from Central import Central
from Cable import Cable
from SplittingZone import SplittingZone
import sys
import ezdxf
import re
# import pandas


class TraceMap:
    def __init__(self, path):
        self.dxf_file = self.open_dxf(path)
        self.model_space = self.dxf_file.modelspace()
        self.identifier = ""
        self.splitting_junctions = list()
        self.fusion_junctions = list()
        self.central = Central()
        self.primary_cables = list()
        self.secondary_cables = list()
        self.pdo_list = list()
        self.insert_map = {}
        self.lwpolyline_map = {}

    @staticmethod
    def open_dxf(path):
        try:
            trace_map = ezdxf.readfile(path)
            return trace_map
        except IOError:
            print(f"No valid file was found at {path}.")
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted dxf file.")
            sys.exit(2)

    @staticmethod
    def print_entity(entity):
        if entity.dxf.layer != "Base_Cartografica":
            print("\tType: %s\n" % entity.dxftype)
            print("\tAttributes: %s\n" % entity.dxfattribs())
            print("\t________________________________")

    def print_type(self):
        for block in self.model_space.query("INSERT"):
            print(str(block))
            for attrib in block.attribs:
                print("Tag: {}, Value: {}".format(attrib.dxf.tag, attrib.dxf.text))

    def parse_to_list(self):
        for entity in self.model_space:
            layer = entity.dxf.layer
            if layer == "Central":
                self.central = Central(entity)
            if re.match('^05 - Cabos Vectores', layer):
                cable = Cable(entity, '05 - Cabos Vectores', re.search('[A-Z]{3,}', layer))
                self.primary_cables.append(cable)
            if re.match('^05 - Cabos Secundários', layer):
                cable = Cable(entity, '05 - Cabos Secundários', re.search('[A-Z]{3,}', layer))
                self.secondary_cables.append(cable)
            if re.match('^06 - JFO', layer):
                self.add_fusion_junction(entity)
            if re.match('^06 - JSO', layer):
                self.add_splitting_junction(entity)
            if re.match('^06 - PDO', layer):
                self.pdo_list.append(entity)

    def print_lists(self):
        self.print_central()
        self.print_primary_cables()
        self.print_secondary_cables()
        self.print_fusion_junctions()
        self.print_splitting_junctions()
        self.print_pdo_list()

    def print_maps(self):
        print("INSERT MAP")
        for key,value in self.insert_map:
            print("Layer: {} | Entity: {}".format(key, value))
        print("______________________________________________________________________________")
        print("LWPOLYLINE MAP")
        for key, value in self.insert_map:
            print("Layer: {} | Entity: {}".format(key, value))

    def parser(self):
        for block in self.model_space.query("INSERT"):
            self.insert_map[block.dxf.layer] = block
        for block in self.model_space.query("LWPOLYLINE"):
            self.insert_map[block.dxf.layer] = block

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_identifier(self) -> str:
        return self.identifier

    def add_splitting_junction(self, splitting_junction):
        if splitting_junction not in self.splitting_junctions:
            self.splitting_junctions.append(splitting_junction)

    def add_fusion_junction(self, fusion_junction):
        if fusion_junction not in self.fusion_junctions:
            self.fusion_junctions.append(fusion_junction)

    def print_central(self):
        print("CENTRAL")
        self.print_entity(self.central.get_entity())
        print("--------------------------------------------------------------------")

    def print_primary_cables(self):
        print("PRIMARY CABLES")
        for cable in self.primary_cables:
            self.print_entity(cable.get_entity())
        print("---------------------------------------------------------------------")

    def print_secondary_cables(self):
        print("SECONDARY CABLES")
        for cable in self.secondary_cables:
            self.print_entity(cable.get_entity())
        print("----------------------------------------------------------------------")

    def print_fusion_junctions(self):
        print("FUSION JUNCTIONS")
        for entity in self.fusion_junctions:
            self.print_entity(entity)
        print("----------------------------------------------------------------------")

    def print_splitting_junctions(self):
        print("SPLITTING JUNCTIONS")
        for entity in self.splitting_junctions:
            self.print_entity(entity)
        print("----------------------------------------------------------------------")

    def print_pdo_list(self):
        print("PDO LIST")
        for entity in self.pdo_list:
            self.print_entity(entity)
        print("----------------------------------------------------------------------")
