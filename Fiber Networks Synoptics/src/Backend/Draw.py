import ezdxf as ez
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties, LayoutProperties
from ezdxf.enums import TextEntityAlignment


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
        blockref.add_auto_attribs(attribs)
        return blockref

    def draw(self, filename: str, path: str):
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
        jso200 = self.blockref("JSO", (0, 0), {'layer': 'SINOP_JSFO', 'xscale': 10, 'yscale': 10}, {'NAME': "JSO%d" % 200})
        jfo200 = self.blockref("JFO", (60, -60), {'layer': 'SINOP_JSFO', 'xscale': 10, 'yscale': 10}, {'NAME': "JFO%d" % 200})
        pdo2001 = self.blockref("PDO", (60, 0), {'layer': 'SINOP_PDO', 'xscale': 10, 'yscale': 10}, {'NAME': "PDO%d" % 2001})
        pdo2002 = self.blockref("PDO", (120, -60), {'layer': 'SINOP_PDO', 'xscale': 10, 'yscale': 10}, {'NAME': "PDO%d" % 2002})
        pdo2003 = self.blockref("PDO", (120, -120), {'layer': 'SINOP_PDO', 'xscale': 10, 'yscale': 10}, {'NAME': "PDO%d" % 2003})
        pdo2004 = self.blockref("PDO", (60, -120), {'layer': 'SINOP_PDO', 'xscale': 10, 'yscale': 10}, {'NAME': "PDO%d" % 2004})
        jso200.add_attrib('TIPO', 'JSO200').set_placement((0, 8), align=TextEntityAlignment.MIDDLE_CENTER)
        jfo200.add_attrib('TIPO', 'JFO200').set_placement((60, -52), align=TextEntityAlignment.MIDDLE_CENTER)
        jfo200.add_attrib('CABO', 'VDF-BRA1-JSO200-95001').set_placement((52, -60), align=TextEntityAlignment.BOTTOM_RIGHT)
        pdo2001.add_attrib('TIPO', 'PDO2001').set_placement((60, 8), align=TextEntityAlignment.MIDDLE_CENTER)
        pdo2001.add_attrib('CABO', 'VDF-BRA1-95001').set_placement((52, 0), align=TextEntityAlignment.BOTTOM_RIGHT)
        pdo2002.add_attrib('TIPO', 'PDO2002').set_placement((120, -52), align=TextEntityAlignment.MIDDLE_CENTER)
        pdo2002.add_attrib('CABO', 'VDF-BRA1-JSO200-95002').set_placement((112, -60), align=TextEntityAlignment.BOTTOM_RIGHT)
        pdo2003.add_attrib('TIPO', 'PDO2003').set_placement((120, -112), align=TextEntityAlignment.MIDDLE_CENTER)
        pdo2003.add_attrib('CABO', 'VDF-BRA1-JSO200-95003').set_placement((112, -120), align=TextEntityAlignment.BOTTOM_RIGHT)
        pdo2004.add_attrib('TIPO', 'PDO2004').set_placement((60, -112), align=TextEntityAlignment.MIDDLE_CENTER)
        pdo2004.add_attrib('CABO', 'VDF-BRA1-JSO200-95004').set_placement((52, -120), align=TextEntityAlignment.BOTTOM_RIGHT)
        self.line((0, 0), (60, 0), 'SINOP_CONDUTA')
        self.line((0, 0), (60, -60), 'SINOP_AEREO')
        self.line((0, 0), (60, -120), 'SINOP_AEREO')
        self.line((60, -60), (120, -60), 'SINOP_AEREO')
        self.line((60, -60), (120, -120), 'SINOP_AEREO')
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
