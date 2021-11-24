from meerk40t.camera.gui.camerapanel import CameraInterface

try:
    import wx
except ImportError as e:
    from meerk40t.core.exceptions import Mk40tImportAbort

    raise Mk40tImportAbort("wxpython")


def plugin(kernel, lifecycle):
    if lifecycle == "register":
        kernel.register("window/CameraInterface", CameraInterface)

