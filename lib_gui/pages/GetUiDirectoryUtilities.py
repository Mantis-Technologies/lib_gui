import os


def GetCannaCheckUiImagePath(fileName: str) -> str:
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    lib_gui_dir = os.path.dirname(script_dir)
    imagesFolderPath = os.path.join(lib_gui_dir, "CannaCheck_UI_images_1.2")
    return os.path.join(imagesFolderPath, fileName)
