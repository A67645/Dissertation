import ezdxf as ez
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties, LayoutProperties
from ezdxf.enums import TextEntityAlignment
import re


class Drawing:
    def __init__(self):
        self.document = ez.new('R2018')
        self.modelspace = self.document.modelspace()
        self.coords = [0, 0]
        self.coord_map = dict()

    # layers as a list of tuples containing layer name and attributes such as color, linetype, etc.
    def layers(self, layers: list):
        for layer in layers:
            entity = self.document.layers.add(layer[0])
            entity.color = layer[1]
            # entity.dxf.linetype = layer[2]

    def line(self, start, end, layer: str):
        self.modelspace.add_line(start, end, dxfattribs={'layer': layer})

    def block(self, name: str, equipment: str):
        block = self.document.blocks.new(name)
        if equipment == "PDO":
            block.add_circle((0, 0), 0.5, dxfattribs={'layer': "SINOP_PDO"})
        elif equipment == "JSO" or equipment == "JFO":
            block.add_circle((0, 0), 0.5, dxfattribs={'layer': "SINOP_JSFO"})
        return block

    def blockref(self, name: str, coords, dxfattribs: dict, attribs: dict):
        blockref = self.modelspace.add_blockref(name, coords, dxfattribs)
        for key, value in attribs.items():
            blockref.add_attrib(key, value[0]).set_placement(value[1], align=value[2])

        return blockref

    def draw_block(self, equipment, layer, identifier, cable, coords):
        xy = [coords[0], coords[1]]
        print("draw block " + identifier + ' at ' + str(xy))
        self.blockref(equipment, xy, {'layer': layer, 'xscale': 10, 'yscale': 10},
                      {'TIPO': [identifier, (xy[0], xy[1]+8), TextEntityAlignment.MIDDLE_CENTER],
                       'CABO': [cable, (xy[0]-8, xy[1]), TextEntityAlignment.BOTTOM_RIGHT]})
        self.coord_map[identifier] = [xy[0], xy[1]]
        print(str(self.coord_map[identifier]))

    def draw_line(self, start, end):
        self.line((start[0], start[1]), (end[0], end[1]), 'SINOP_AEREO')

    def iterate(self, pdo: dict, jso: dict, identifier: str, max_fork: int):
        fork = 1
        print("iterator for block " + identifier)
        for key in pdo.keys():
            if re.match(r'^JSO', key):
                continue
            elif key != identifier:
                self.coords[0] += 100
                print("pdo list: " + str(pdo))
                if len(pdo) > 2:
                    print("fork value for " + key + " is " + str(fork))
                    if fork >= max_fork:
                        max_fork = fork
                        print("Max_Fork value updated to: " + str(max_fork))
                    if fork > 1:
                        self.coords[1] -= 100
                        print("block " + key + " recursive call as a fork")
                        max_fork = self.iterate(jso[key], jso, key, max_fork)
                        self.coords[1] += 100
                        fork += 1
                    else:
                        fork += 1
                        print("block " + key + " recursive call as first block of a fork")
                        max_fork = self.iterate(jso[key], jso, key, max_fork)
                else:
                    print("block " + key + " recursive call as next block of a pair")
                    max_fork = self.iterate(jso[key], jso, key, max_fork)
                self.coords[0] -= 100
            else:
                cable = jso[key][key]
                if re.match(r'^PDO', key):
                    xy = self.coords
                    self.draw_block('PDO', 'SINOP_PDO', key, cable, xy)
                if re.match(r'^JFO', key):
                    xy = self.coords
                    self.draw_block('JFO', 'SINOP_JSFO', key, cable, xy)
                # if len(pdo) > 2:
                    # self.coords[1] -= 100*max_fork
                break
        return max_fork

    def iterate_dict(self, jso: dict, max_fork, pdo_list=None):
        self.coords[0] += 100
        for key in jso[next(iter(jso))]:
            if key == next(iter(jso)) or re.match(r'^JSO', key):
                continue
            else:
                max_fork = self.iterate(jso[key], jso, key, max_fork)
                self.coords[1] -= 100*max_fork
                print("max fork is: " + str(max_fork))
                max_fork = 1

    def cables(self, link_table: dict, sz):
        print(str(self.coord_map))
        for block in link_table.keys():
            for index in link_table[block].keys():
                # (sz.is_pdo(index) or sz.is_jfo(index)) and (sz.is_pdo(block) or sz.is_jfo(block)) and
                if not re.match(r'^JSO', index):
                    self.draw_line(self.coord_map[block], self.coord_map[index])
                    print("Line Drawn from " + block + "at " + str(self.coord_map[block]) + "to " + index + "at " + str(self.coord_map[index]))

    def draw(self, filename: str, path: str, jso_zone: dict, sz):
        layers = [
            ('SINOP_AEREO', 1, 'DASHED'),
            ('SINOP_CONDUTA', 160, 'DOTTED'),
            ('SINOP_PDO', 4, 'CONTINUOUS'),
            ('SINOP_JSFO', 30, 'CONTINUOUS')
        ]
        self.layers(layers)
        self.modelspace.add_text("Synoptics Map Prototype", height=2, dxfattribs={'layer': '0'}).set_placement((25, 20))
        jso = self.block("JSO", "JSO")
        pdo = self.block("PDO", "PDO")
        jfo = self.block("JFO", "JFO")
        jsoXXX = self.blockref("JSO", (0, 0), {'layer': 'SINOP_JSFO', 'xscale': 10, 'yscale': 10},
                               {'TIPO': [next(iter(jso_zone)), (0, 8), TextEntityAlignment.MIDDLE_CENTER]})
        self.coord_map[next(iter(jso_zone))] = [0, 0]
        self.coords = [0, 0]
        max_fork = 1
        self.iterate_dict(jso_zone, max_fork)

        if sz.index != 'JSO209' and sz.index != 'JSO210' and sz.index != 'JSO212' and sz.index != 'JSO215':
            self.cables(jso_zone, sz)

        self.document.saveas(path + filename + ".dxf")

    def draw_to_dir(self, filename, folder_path: str, jso_zone, sz):
        self.draw(filename, folder_path, jso_zone, sz)

    @staticmethod
    def convert_dxf2img(names, img_format='.png', img_res=300):
        for name in names:
            doc = ezdxf.readfile(name)
            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise Exception("The DXF document is damaged and can't be converted!")
            else:
                fig = plt.figure()
                ctx = RenderContext(doc)
                # Better control over the LayoutProperties used by the drawing frontend
                layout_properties = LayoutProperties.from_layout(msp)
                layout_properties.set_colors(bg='#000000')
                ax = fig.add_axes([0, 0, 1, 1])
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, layout_properties=layout_properties, finalize=True)
                img_name = "preview"  # select the image name that is the same as the dxf file name
                first_param = img_name + img_format  #concatenate list and string
                fig.savefig(first_param, dpi=img_res)
