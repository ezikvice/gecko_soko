import os
from concurrent.futures import ProcessPoolExecutor as _ProcessPoolExecutor

from pyglet.event import EventDispatcher as _EventDispatcher


# позаимствовал здесь:
# https://stackoverflow.com/questions/65716631/using-filedialog-askdirectory-with-tkinter-and-pyglet-freezes-the-application
# TODO: разобраться с этим всем
class _Dialog(_EventDispatcher):
    executor = _ProcessPoolExecutor(max_workers=1)

    @staticmethod
    def _open_dialog():
        raise NotImplementedError

    def open(self):
        future = self.executor.submit(self._open_dialog, self._dialog)
        future.add_done_callback(self._dispatch_event)

    def _dispatch_event(self, future):
        raise NotImplementedError


class FileOpenDialog(_Dialog):
    def __init__(self, title="Open File", initial_dir=os.path.curdir, filetypes="", multiple=False):
        from tkinter import filedialog

        self._dialog = filedialog.Open(title=title,
                                       initialdir=initial_dir,
                                       filetypes=filetypes,
                                       multiple=multiple
                                       )

    @staticmethod
    def _open_dialog(dialog):
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        return dialog.show()

    def _dispatch_event(self, future):
        self.dispatch_event('on_dialog_open', future.result())

    def on_dialog_open(self, filename):
        """Event for filename choice"""
        print("FILENAMES ON SAVE!", filename)
        pass


class FileSaveDialog(_Dialog):
    def __init__(self, title="Save As", initial_dir=os.path.curdir, initial_file="", filetypes="", default_ext=""):
        from tkinter import filedialog
        self._dialog = filedialog.SaveAs(title=title,
                                         initialdir=initial_dir,
                                         initialfile=initial_file,
                                         filetypes=filetypes,
                                         defaultextension=default_ext,
                                         )

    @staticmethod
    def _open_dialog(dialog):
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        return dialog.show()

    def _dispatch_event(self, future):
        self.dispatch_event('on_dialog_save', future.result())

    @staticmethod
    def on_dialog_save(self, filename):
        """Event for filename choice"""
        print("FILENAMES ON SAVE!", filename)
        pass


FileOpenDialog.register_event_type('on_dialog_open')
FileSaveDialog.register_event_type('on_dialog_save')

# if __name__ == '__main__':
    # save_as = FileSaveDialog(initial_file="test", filetypes=[("PNG", ".png"),("24-bit Bitmap", ".bmp")])
    # save_as.open()

    # @save_as.event
    # def on_dialog_save(filename):
    #    print("FILENAMES ON SAVE!", filename)




    # open_dialog = FileOpenDialog(filetypes=[("PNG", ".png"), ("24-bit Bitmap", ".bmp")], multiple=True)
    # open_dialog.open()
    #
    #
    # @open_dialog.event
    # def on_dialog_open(filename):
    #     print("FILENAMES ON OPEN!", filename)