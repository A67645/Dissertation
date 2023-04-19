# Splitting Zone or JSO Zone class file
# from Cable import Cable
import re

from JSO import JSO
import ezdxf
import random
import openpyxl
import AttributeProcessing as ap


class SplittingZone:

    def __init__(self, entity):  # Instance Variables definition
        self.jso = JSO(entity)
        self.index = entity.get_attrib_text("TIPO")
        self.jfo_list = list()
        self.pdo_list = list()
        self.document = ezdxf.new('R2018')
        self.model_space = self.document.modelspace()
        self.link_table = self.link_table()

    def add_pdo(self, pdo):
        if pdo not in self.pdo_list:
            self.pdo_list.append(pdo)

    def add_jfo(self, jfo):
        if jfo not in self.jfo_list:
            self.jfo_list.append(jfo)

    @staticmethod
    def get_random_point():
        """Returns random x, y coordinates."""
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        return x, y

    def to_string(self) -> str:
        result = "\tIndex: " + self.index + "\n" + "\tJSO: " + self.jso.entity.get_attrib_text("TIPO") + "\n"
        for pdo in self.pdo_list:
            result += "\t\tPDO" + pdo.identifier + "\n"
        for jfo in self.jfo_list:
            result += "\t\t" + jfo.identifier + "\n"
        return result

    def create_synoptics(self):
        placing_points = [self.get_random_point() for _ in range(len(self.pdo_list))]
        block = self.document.blocks.new(name='PDO_SIN')
        i = 0
        for pdo in self.pdo_list:
            entity = pdo.entity
            attribs = entity.attribs
            self.model_space.add_auto_blockref('PDO_SIN', placing_points[i], values=attribs, dxfattribs={
                'xscale': entity.dxf.xscale,
                'yscale': entity.dxf.yscale,
                'rotation': 0
            })
            i += 1
        for flag_ref in self.model_space.query('INSERT[name=="PDO_SIN"]'):
            print("FLAG REFERENCE: " + str(flag_ref))
        filename = r"C:\Users\thech\Desktop\MIEI\Dissertation\Fiber Networks Synoptics\\" + self.index + ".dxf"
        # self.document.saveas(filename)

    def link_table(self):
        row_start = 13
        filename = r"C:\Users\thech\Desktop\MIEI\Dissertation\Fiber Networks Synoptics\doc\dxf\exemplo VODAFONE\04 - Tabelas de juntas de Rede Secundária\Tabelas de Ligação da " + self.index + ".xlsx"
        workbook = openpyxl.load_workbook(filename)
        zone_dict = {}
        for sheet in workbook.worksheets:
            if sheet.title == "ESQ":
                continue
            equipment_dict = {}
            for row in range(row_start, sheet.max_row):
                line = []
                for col in sheet.iter_cols(1, 14):
                    line.append(col[row].value)
                if all(item is None for item in line):
                    continue
                if line[0] == '' or line[13] == '' or line[7] == '':
                    continue
                equipment_dict[line[13]] = []
                if line[7] and line[13] != sheet.title and re.match('^VDF', line[7]):
                    print(line[13])
                    print(line[7])
                    equipment_dict[line[13]].append(line[7])
                elif line[0] and line[13] == sheet.title and re.match('^VDF', line[0]):
                    print(line[13])
                    print(line[0])
                    equipment_dict[line[13]].append(line[0])
                if len(equipment_dict[line[13]]) > 0:
                    print(equipment_dict)
                    zone_dict[sheet.title] = equipment_dict
        return zone_dict
