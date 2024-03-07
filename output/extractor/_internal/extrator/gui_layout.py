import time

import PySimpleGUI as sg

def _menu():
    """
    Top menu of the gui
    :return: The top menu
    :rtype: list
    """
    menu_top_def = [
        # ["&File", ["&Open    Ctrl-O", "&Save    Ctrl-S", "---", '&Properties', "&Exit", ]],
        ["&Help", ["Info", "About"]],
    ]
    layout = [[sg.Menu(menu_top_def)]]
    return layout


def _gui_main_layout():
    """
    The main layout for the gui
    :return: The main layout for the gui
    :rtype: list
    """

    main = sg.Frame("Listening", [[
        sg.Column([
            [sg.ProgressBar(100, key="-BAR-", size=(25, 5), expand_x=True), sg.Checkbox("KILL", visible=False, key="-KILL-")],
            [sg.Button("Extract_Folder", key="-EXTRACT_FOLDER-", expand_x=True),
             sg.Button("Extract_File", key="-EXTRACT_FILE-", expand_x=True),
             sg.Button("Close", key="-CLOSE-", expand_x=True,
                       tooltip="Closes the whole program")],
        ])
    ]])

    layout = [[main]]

    return layout


def main_layout():
    """
    The main setup for the layout for the gui
    :return: The setup and layout for the gui
    :rtype: sg.Window
    """

    # sg.theme()
    top_menu = _menu()

    layout = [[
        top_menu,
        _gui_main_layout()
    ]]

    return sg.Window("ChemDraw Extractor", layout, finalize=True, resizable=True)


def worklist_progressbar(run, window):
    # Define minimum and maximum timer values
    min_timer = 0
    max_timer = 100

    # Initialize counter to 0
    counter = 0

    # Loop until run is False
    while run:

        # Check if counter has reached minimum or maximum timer values
        if counter == min_timer:
            runner = "pos"
        elif counter == max_timer:
            runner = "neg"

        # Increase or decrease counter based on the value of runner
        if runner == "pos":
            counter += 10
        elif runner == "neg":
            counter -= 10

        # Update the progress bar
        window["-WORKLIST_PROGRESSBAR-"].update(counter)

        # Wait for 100ms
        time.sleep(0.1)

        # Check if the worklist kill switch is activated
        if window["-WORKLIST_KILL-"].get():
            run = False
