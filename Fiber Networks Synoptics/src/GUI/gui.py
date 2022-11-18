import PySimpleGUI as sg
import json
import os
import io
from PIL import Image

def load_file(filename):
    with open(filename, "r") as fs:
        dict = json.load(fs)
    config = dict["config1.json"]
    return config

def view_config(config, filename):

    sg.theme('DarkAmber') # Definir cor da janela

    config_headings = ["key", "value"]
    config_lines = config
    data_cols_width = [90, 65]
    config_layout = [[sg.Table(values=config, headings=config_headings, max_col_width=35,
                               auto_size_columns=True,
                               display_row_numbers=False,
                               justification='center',
                               num_rows=len(config),
                               key='-TABLE-',
                               row_height=35)],  
                     [sg.Button("Exit")]
                    ]
    config_window = sg.Window(filename, config_layout, size = (600, 600))

    while True:

        event, values = config_window.read()

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

def create_config():
    config = []

    file_types = [("JSON (*.json)", "*.json"),
                  ("All files (*.*)", "*.*")]

    config_layout = [
                     [sg.Text("File Name:"), sg.InputText(key = "-filename-")],
                     [sg.Text("ISP Name:"), sg.InputText(key = "-ISPname-")],
                     [sg.Text("Central Station Block Format:"), sg.InputText(key = "-CSBformat-")],
                     [sg.Text("Fusion Block Format:"), sg.InputText(key = "-FBformat-")],
                     [sg.Text("Splitting Block Format:"), sg.InputText(key = "-SBformat-")],
                     [sg.Text("Costumer Block Format:"), sg.InputText(key = "-CBformat-")],
                     [sg.Text("Cable Block Format:"), sg.InputText(key = "-CTBformat-")],
                     [sg.Text("Splitting Cable Block Format:"), sg.InputText(key = "-SCBformat-")],
                     [sg.Button("Save")],
                     [sg.Button("Exit")]
                    ]

    config_window = sg.Window("Config File Creator", config_layout, size = (600, 600))

    while True:
        event, values = config_window.read()

        if event == "EXIT" or event == sg.WIN_closed:
            if config != []:
                return
            else:
                sg.popup("Incomplete config, operation aborted!")
                return

        if event == "Save":
            if values["-filename-"] != "" and values["-ISPname-"] != "" and values["-CSBformat-"] != "" and values["-FBformat-"] != "" and values["-SBformat-"] != "" and values["-CBformat-"] != "" and values["-CTBformat-"] != "" and values["-SLBformat-"] != "":
                file_dict = { "config1.json" : [
                                    ["ISP Name", values["-ISPname-"]],
                                    ["Central Station Block Format", values["-CSBformat-"]],
                                    ["Fusion Block Format", values["-FBformat-"]],
                                    ["Splitting Block Format", values["-SBformat-"]],
                                    ["Costumer Block Format", values["-CBformat-"]],
                                    ["Cable Tag Format", values["-CTBformat-"]],
                                    ["Splitting Cable Tag Format", values["-SLBformat-"]]
                                   ]
                            } 
                json_object = json.dumps(file_dict, indent = 4)

                with open(values["-filename-"]
    return

def gui():

    sg.theme('DarkAmber') # Definir cor da janela

    config = []
    file_types = [("JSON (*.json)", "*.json"),
                  ("All files (*.*)", "*.*")]
    menu_layout = [
                    [sg.Image("img\logo.png", size=(100,100))],
                    [sg.Input(size=(25, 1), key="-FILE-"), 
                     sg.FileBrowse(file_types = file_types),
                     sg.Button("Load Config")],
                    [sg.Button("Create Config")],
                    [sg.Button("View Config")],
                    [sg.Button("EXIT")]
                  ]
    menu_window = sg.Window("FNSynoptics", menu_layout, size = (600, 600))

    while True:
        event, values = menu_window.read()

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break
        
        if event == "Load Config":
            config = load_file(values["-FILE-"])
            
        if event == "View Config" and config != []:
            view_config(config, values["-FILE-"])

        if event == "Create Config":
            config = create_config()

def main():
    gui()

main()