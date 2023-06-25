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
        print(identifier + ': ' + str(coords))
        self.blockref(equipment, coords, {'layer': layer, 'xscale': 10, 'yscale': 10},
                      {'TIPO': [identifier, (coords[0], coords[1]+8), TextEntityAlignment.MIDDLE_CENTER],
                       'CABO': [cable, (coords[0]-8, coords[1]), TextEntityAlignment.BOTTOM_RIGHT]})

    def draw_line(self, start, end):
        self.line((start[0], start[1]), (end[0], end[1]), 'SINOP_AEREO')

    def iterate(self, pdo: dict, jso: dict, identifier: str, coords: list):
        fork = 0
        for key in pdo.keys():
            if re.match(r'^JSO', key):
                continue
            elif key != identifier:
                coords[0] += 100
                if len(jso[key]) > 2:
                    if fork > 0:
                        coords[1] -= 100
                        self.iterate(jso[key], jso, key, [coords[0], coords[1]])
                        coords[1] += 100
                    else:
                        fork += 1
                        self.iterate(jso[key], jso, key, [coords[0], coords[1]])
                else:
                    self.iterate(jso[key], jso, key, [coords[0], coords[1]])
                coords[0] -= 100
            else:
                cable = jso[key][key]
                fork = 0
                if re.match(r'^PDO', key):
                    self.draw_block('PDO', 'SINOP_PDO', key, cable, coords)
                if re.match(r'^JFO', key):
                    self.draw_block('JFO', 'SINOP_JSFO', key, cable, coords)
                break

    def iterate_dict(self, jso: dict, coords):
        coords[0] += 100
        for key in jso[next(iter(jso))]:
            if key == next(iter(jso)) or re.match(r'^JSO', key):
                continue
            else:
                self.iterate(jso[key], jso, key, coords)
                coords[1] -= 100

    def draw(self, filename: str, path: str, jso_zone: dict):
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
        coords = [0, 0]
        self.iterate_dict(jso_zone, coords)

        self.document.saveas(path + filename + ".dxf")

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
