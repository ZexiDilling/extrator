import os
import sys
from pathlib import Path
# from shutil import copy, rmtree, which
import shutil
import zipfile
import pyunpack
from PySimpleGUI import PopupOK

from processsing import proc


def pp_extration(data_location, data_type):
    if data_type == "folder":
        files = data_location.glob("*.pptx")
        folder = data_location
    else:
        files = []
        files.append(data_location.absolute())
        folder = Path(data_location.parent.absolute())
    temp_folder_name = "temp_chemdraw_extraction_folder"
    temp_folder = folder / temp_folder_name

    index = 1
    while temp_folder.exists():
        temp_name_counter = f"{temp_folder_name}_{index}"
        temp_folder = folder / temp_name_counter
        index += 1

    temp_folder.mkdir()

    for file in files:

        name = file.name.removesuffix(".pptx")
        temp_chemdraw_folder = folder/f"{name}_chemdraw"
        index = 1
        while temp_chemdraw_folder.exists():
            name = f"{name}"
            temp_chemdraw_folder = folder / f"{name}_chemdraw_{index}"
            index += 1
        temp_chemdraw_folder.mkdir()
        temp_file = Path(shutil.copy(file, temp_folder))

        temp_file = temp_file.rename(temp_file.with_suffix(".zip"))

        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        ole_files = temp_folder.glob("*/**")
        rar_files = []
        for ole_file in ole_files:
            temp_ole_file = ole_file.parts[-1]
            if temp_ole_file.endswith("embeddings"):
                temp_files = ole_file.glob("**/*.bin")
                for file in temp_files:
                    rar_temp_file = file
                    rar_temp_file = rar_temp_file.rename(rar_temp_file.with_suffix(".rar"))
                    rar_files.append(rar_temp_file)
        temp_folder_rar = temp_folder/'rar'
        temp_folder_rar.mkdir()
        cdx_counter = 1
        patool_executable = shutil.which('patool')
        patool_executable = rf"{patool_executable}"
        script_directory = os.path.dirname(os.path.abspath(__file__))
        patool_executable_new = rf"{script_directory}\extrator\venv\Scripts"
        for files in rar_files:
            files = _fullpath(files)
            patool_cmd = [
            sys.executable,
            patool_executable_new,
            "--non-interactive",
            "extract",
            files,
            "--outdir=" + str(temp_folder_rar),
            #                     '--verbose',
        ]
            proc(patool_cmd).call()

            temp_rar_files = temp_folder_rar.glob("*")

            for temp_file in temp_rar_files:
                temp_temp_file = temp_file.parts[-1]
                if temp_temp_file.endswith("CONTENTS"):
                    temp_file = temp_file.rename(f"{temp_file}_{cdx_counter}")
                    temp_file = temp_file.rename(temp_file.with_suffix(".cdx"))
                    temp_file.rename(temp_chemdraw_folder/temp_file.name)
                    cdx_counter += 1
    # Missing - getting information from the chemdraw file

    shutil.rmtree(temp_folder)
    if data_type == "file":
        return temp_chemdraw_folder
    else:
        return folder



def _fullpath(x: str) -> str:
    x = os.path.expandvars(x)
    x = os.path.expanduser(x)
    x = os.path.normpath(x)
    x = os.path.abspath(x)
    return x


if __name__ == "__main__":
    pass
