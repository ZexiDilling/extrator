from datetime import time
import PySimpleGUI as sg
from pathlib import Path
from ChemDrawExtrator import pp_extration
from gui_layout import main_layout
from pop_up import popup_extra


def main_control():
    """
    :return:
    """

    window = main_layout()

    while True:

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "-CLOSE-":
            break

        if event == "-EXTRACT_FOLDER-" or event == "-EXTRACT_FILE-":
            if event == "-EXTRACT_FOLDER-":
                data_type = "folder"
            else:
                data_type = "file"
            data_location = sg.popup_get_file("Please select a file")
            if data_location:
                data_location = Path(data_location)
                #
                temp_chemdraw_folder = pp_extration(data_location, data_type)
                # Thread(target=, args=(), daemon=True).start()
                # Thread(target=progressbar, args=(config, True, window,), daemon=True).start()

                popup_extra(temp_chemdraw_folder)

        if event == "Info":
            with open("help.txt", "r") as file:
                info = file.read()
            sg.Popup(info, title="Information")

        if event == "About":
            with open("about.txt", "r") as file:
                about_content = file.read()
            sg.Popup(about_content, title="About")


def progressbar(run, window):
    """
    The progress bar, that shows the program working
    :param run: If the bar needs to be running or not
    :type run: bool
    :param window: Where the bar is displayed
    :type window: PySimpleGUI.PySimpleGUI.Window
    :return:
    """
    min_timer = 0
    max_timer = 100
    counter = 0

    while run:
        if counter == min_timer:
            runner = "pos"
        elif counter == max_timer:
            runner = "neg"

        if runner == "pos":
            counter += 10
        elif runner == "neg":
            counter -= 10

        window["-BAR-"].update(counter)

        time.sleep(0.1)
        if window["-KILL-"].get():
            run = False
