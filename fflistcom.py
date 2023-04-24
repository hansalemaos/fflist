from nutikacompile import compile_with_nuitka

wholecommand = compile_with_nuitka(
    pyfile=r"C:\ProgramData\anaconda3\envs\nu\fflist.pyw",
    icon=r"C:\ProgramData\anaconda3\envs\nu\iconfilesearch.ico",
    disable_console=True,
    file_version="1.0.0.1",
    onefile=True,
    outputdir="c:\\fflist2",
    addfiles=[
r"C:\ProgramData\anaconda3\envs\nu\iconfilesearch.ico",
r"C:\ProgramData\anaconda3\envs\nu\uffs.com",
    ],
    delete_onefile_temp=False,  # creates a permanent cache folder
    needs_admin=True,
    arguments2add="--msvc=14.3 --noinclude-numba-mode=nofollow --plugin-enable=tk-inter --jobs=3",
)
