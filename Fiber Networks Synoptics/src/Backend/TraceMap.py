# Trace Map class file
from Central import Central
from Cable import Cable
from JFO import JFO
from JSO import JSO
from PDO import PDO
from SplittingZone import SplittingZone
import sys
import ezdxf
import re


class TraceMap:
    def __init__(self, path):
        self.dxf_file = self.open_dxf(path)
        self.model_space = self.dxf_file.modelspace()
        self.identifier = ""
        self.splitting_junctions = list()
        self.fusion_junctions = list()
        self.central = None
        self.primary_cables = list()
        self.secondary_cables = list()
        self.pdo_list = list()
        self.splitting_zones = list()

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

    @staticmethod
    def print_insert(entity):
        print([(attrib.dxf.tag, attrib.dxf.text) for attrib in entity.attribs])
        print("______________________________________________________________")

    def print_lists(self):
        self.print_central()
        self.print_primary_cables()
        self.print_secondary_cables()
        self.print_fusion_junctions()
        self.print_splitting_junctions()
        self.print_pdo_list()

    def print_splitting_zone(self, jso: str) -> str:
        for sz in self.splitting_zones:
            if jso == sz.index:
                return sz.to_string()

    def link_table(self, jso: str) -> dict:
        result = {}
        for sz in self.splitting_zones:
            if sz.index == jso:
                result = sz.link_table
        return result

    def parser(self, link_tables_path: str):
        for block in self.model_space.query("INSERT"):
            if re.match('^Central', block.dxf.layer):
                self.central = Central(block)
            if re.match('^06 - PDO', block.dxf.layer):
                self.pdo_list.append(PDO(block))
            if re.match('^06 - JSO', block.dxf.layer):
                self.splitting_junctions.append(JSO(block))
            if re.match('^06 - JFO', block.dxf.layer):
                self.fusion_junctions.append(JFO(block))
        for block in self.model_space.query("LWPOLYLINE"):
            if re.match('^05 - Cabos Primários', block.dxf.layer):
                self.primary_cables.append(Cable())
            if re.match('^05 - Cabos Secundários', block.dxf.layer):
                self.secondary_cables.append(Cable())
            if re.match('^05 - Cabos Mistos', block.dxf.layer):
                self.primary_cables.append(Cable())
        for jso in self.splitting_junctions:
            sz = SplittingZone(jso.entity, link_tables_path)
            for pdo in self.pdo_list:
                if pdo.entity.get_attrib_text("TIPO") == jso.entity.get_attrib_text("TIPO"):
                    sz.add_pdo(pdo)
            for jfo in self.fusion_junctions:
                if jfo.entity.get_attrib_text("TIPO") == jso.entity.get_attrib_text("TIPO"):
                    sz.add_jfo(jfo)
            self.splitting_zones.append(sz)

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

    def get_splitting_zone(self, identifier: str):
        for sz in self.splitting_zones:
            if sz.index == identifier:
                return sz

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
        for jfo in self.fusion_junctions:
            self.print_insert(jfo.entity)
        print("----------------------------------------------------------------------")

    def print_splitting_junctions(self):
        print("SPLITTING JUNCTIONS")
        for jso in self.splitting_junctions:
            self.print_insert(jso.entity)
        print("----------------------------------------------------------------------")

    def print_pdo_list(self):
        print("PDO LIST")
        for pdo in self.pdo_list:
            self.print_insert(pdo.entity)
        print("----------------------------------------------------------------------")
