from hackyargparser import add_sysargv
import os
from tkinter import *
import pandas as pd
from pandastable import Table
from uffspd import list_all_files

from shellextools import (
    format_folder_drive_path_backslash,
    add_multi_commands_to_drive_and_folder, get_my_icon, get_monitors_resolution, get_filepath
)
import sys

from tkinteruserinput import get_user_input


class TestApp(Frame):
    def __init__(self, df, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.resolution = get_monitors_resolution()[0]
        self.monitor_w = self.resolution['width']
        self.monitor_h = self.resolution['height']
        self.main.geometry(f'{self.monitor_w - 100}x{self.monitor_h - 100}')
        self.main.title('Search results')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        self.table = pt = Table(f, dataframe=df.copy(),
                                showtoolbar=True, showstatusbar=True)
        self.table.autoResizeColumns()
        pt.show()


myicon = get_my_icon("iconfilesearch.ico")


@add_sysargv
def main(path: str = "", action: str = ""):
    path = format_folder_drive_path_backslash(path)
    uffspath = get_filepath(r"uffs.com")
    dfa = pd.DataFrame(columns=['aa_path', 'aa_name', 'aa_path_only', 'aa_size', 'aa_size_on_disk',
                                'aa_created', 'aa_last_written', 'aa_last_accessed', 'aa_descendents',
                                'aa_read_only', 'aa_archive', 'aa_system', 'aa_hidden', 'aa_offline',
                                'aa_not_content_indexed_file', 'aa_no_scrub_file', 'aa_integrity',
                                'aa_pinned', 'aa_unpinned', 'aa_directory_flag', 'aa_compressed',
                                'aa_encrypted', 'aa_sparse', 'aa_reparse', 'aa_attributes'])
    if action == 'listcertainfiles':
        user_input = get_user_input(
            linesinputbox=20,
            size="900x450",
            title="File types",
            textabovebox="File types - separated with some kind of white space",
            submitbutton="Submit",
            regexcheck=r".*",
            showerror=("Error", "This is not a file type!"),
            showinfo=None,
            showwarning=None,
            icon=myicon,
        )
        allowed_extensions = ['.' + g.lower().strip('. ') for x in user_input.split() if (g := x.strip())]

        dfa = list_all_files(
            path2search=path,
            file_extensions=allowed_extensions,
            uffs_com_path=uffspath,
        )
    if action == 'listallfiles':
        dfa = list_all_files(
            path2search=path,
            file_extensions=None,
            uffs_com_path=uffspath,
        )
    try:
        dfa.aa_created = pd.to_datetime(dfa.aa_created.astype('string'))
        dfa.aa_last_written = pd.to_datetime(dfa.aa_last_written.astype('string'))
        dfa.aa_last_accessed = pd.to_datetime(dfa.aa_last_accessed.astype('string'))
    except Exception:
        pass
    dfa.columns = [x[3:] for x in dfa.columns]
    app = TestApp(dfa)
    return app


if __name__ == "__main__":
    if len(sys.argv) == 1:
        futurnameofcompiledexe = "fflist.exe"
        multicommands = [
            {
                "mainmenuitem": "list files",
                "submenu": "List all files",
                "folderinprogramdata": "RCTools",
                "add2drive": True,
                "add2folder": True,
                "additional_arguments": "--action listallfiles",
            },

            {
                "mainmenuitem": "list files",
                "submenu": "List file types",
                "folderinprogramdata": "RCTools",
                "add2drive": True,
                "add2folder": True,
                "additional_arguments": "--action listcertainfiles",
            },

        ]
        add_multi_commands_to_drive_and_folder(
            futurnameofcompiledexe,
            multicommands,
        )
    else:
        try:
            app = main()
            app.mainloop()
            try:
                sys.exit(0)
            finally:
                os._exit(0)

        except Exception as fe:
            print(fe)
            try:
                sys.exit(1)
            finally:
                os._exit(1)
