# Main class for FNSynoptics backend structure.
from TraceMap import TraceMap
import AttributeProcessing as ap
import ezdxf as ez
from ezdxf.gfxattribs import GfxAttribs
from Draw import Drawing
import PySimpleGUI as sg


def draw_test():
    # Create new document and modelspace, referencing the DXF version
    doc = ez.new('R2018')
    msp = doc.modelspace()
    # Define document layers
    sinop_aereo = doc.layers.add("SINOP_AEREO")
    sinop_aereo.color = 1
    sinop_pdo = doc.layers.add("SINOP_PDO")
    sinop_pdo.color = 1
    # Create Line
    msp.add_line((0, 0), (100, 0), dxfattribs={"layer": "SINOP_AEREO"})
    # Create Block and Block References with attributes
    pdo = doc.blocks.new(name="PDO")
    pdo.add_circle((0, 0), 0.5, dxfattribs={'layer': "SINOP_PDO"})
    pdo.add_attdef("TIPO", (0.5, -0.5), dxfattribs={'height': 0.5, 'color': 3})
    pdo3001 = msp.add_blockref("PDO", (0, 0), dxfattribs={'xscale': 10, 'yscale': 10})
    pdo3001.add_auto_attribs({'NAME': "PDO%d" % 3001})
    pdo3002 = msp.add_blockref("PDO", (100, 0), dxfattribs={'xscale': 10, 'yscale': 10})
    pdo3002.add_auto_attribs({'NAME': "PDO%d" % 3002})
    # Save Document
    doc.saveas("new_name.dxf")


def draw():
    # Create a new DXF 2018 document
    doc = ez.new("R2018")
    # Add new entities to the modelspace
    msp = doc.modelspace()
    doc.layers.add(name="SINOP_AÉRIO", color=256, linetype="AERO2")
    doc.layers.add(name="SINOP_JSFO", color=4, linetype="ByLayer")
    doc.layers.add(name="SINOP_PDO", color=256, linetype="ByLayer")
    cabo = msp.add_line((0, 0), (50, 0), dxfattribs={"layer": "SINOP_AÉRIO"})
    jso = doc.blocks.new(name="JSO201")
    jso.add_circle((0, 0), 10, dxfattribs={"layer": "SINOP_JSFO"})
    jso = doc.blocks.new(name="PDO")
    jso.add_circle((50, 0), 5, dxfattribs={"layer": "SINOP_PDO"})
    msp.add_blockref('JSO201', (0, 0), dxfattribs={"layer": "SINOP_JSFO"})
    msp.add_blockref('PDO', (50, 0), dxfattribs={"layer": "SINOP_PDO"})
    # doc.saveas(r"C:\Users\thech\Desktop\MIEI\Dissertation\Fiber Networks Synoptics\doc\blockref_tutorial.dxf")
    doc.saveas(r"C:\Users\User\Desktop\Dissertation\Fiber Networks Synoptics\doc\blockref_tutorial.dxf")


def main():
    # path = r"C:\Users\thech\Desktop\MIEI\Dissertation\Fiber Networks Synoptics\doc\dxf\exemplo VODAFONE\01 - Traçado de Rede Secundária\01 - Traçado de Rede Secundária_PEN15_V2.dxf"
    path = r"C:\Users\User\Desktop\Dissertation\Fiber Networks Synoptics\doc\dxf\exemplo VODAFONE\01 - Traçado de Rede Secundária\01 - Traçado de Rede Secundária_PEN15_V2.dxf"
    trace_map = TraceMap(path)
    font = ('Helvetica', 12, 'bold italic')
    sg.set_options(font=font)
    layout = [[sg.Image('logo_proef_oval.png', background_color='#010060')],
              [sg.Button('Processar Traçado', button_color='#17DAA4')],
              [sg.Button('Zona de Splitting', button_color='#17DAA4'), sg.Input(key='-ZONA-')],
              [sg.Button('Tabela de Splitting', button_color='#17DAA4'), sg.Input(key='-TABELA-')],
              [sg.Button('Sinótico', button_color='#17DAA4'), sg.Input(key='-LIGACAO-')],
              [sg.Button('SAIR', button_color='#17DAA4')]]
    window = sg.Window('Fiber Networks Synoptics', layout, size=(800, 600), background_color='#010060')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'SAIR':
            break
        if event == "Processar Traçado":
            trace_map.parser()
            sg.popup('Traçado Processado com Sucesso!')
        if event == 'Zona de Splitting':
            sg.popup(trace_map.print_splitting_zone(values['-ZONA-']))
        if event == 'Tabela de Splitting':
            for sz in trace_map.splitting_zones:
                if sz.index == values['-TABELA-']:
                    sg.popup(str(sz.link_table))
        if event == 'Sinótico':
            drawing = Drawing()
            drawing.draw(values['-LIGACAO-'], r"dxf\\", trace_map.link_table(values['-LIGACAO-']))
            drawing.convert_dxf2img(['dxf\\' + values['-LIGACAO-'] + '.dxf'], img_format='.png', img_res=150)
            sg.popup_no_buttons("Pré-visão de um Sinótico", title='Preview', text_color='#F7F6F2', keep_on_top=True,
                                image="preview.png")
    window.close()
    # trace_map.print_splitting_zones()


main()
