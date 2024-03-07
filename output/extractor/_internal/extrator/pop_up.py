import PySimpleGUI as sg
import os


def open_folder(folder_path):
    if os.path.exists(folder_path):
        os.startfile(folder_path)


def popup_extra(folder_path):

    layout = [
        [sg.Text("Example Popup")],
        [sg.Button("OK"), sg.Button("Open File Location")],
    ]

    window = sg.Window("Popup Example", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "OK":
            break

        elif event == "Open File Location":
            open_folder(folder_path)
            break

    window.close()
