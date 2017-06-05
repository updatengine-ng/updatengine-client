#############################################################################
# Convert python code to Windows exe
#  > python setup.py build
# 
# Original script by tyrtamos :
#   http://python.jpvweb.com/mesrecettespython/doku.php?id=cx_freeze
#############################################################################

import sys, os
from cx_Freeze import setup, Executable

#############################################################################
# preparation des options

# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path

# options d'inclusion/exclusion des modules
includes = ["lxml._elementpath"]  # nommer les modules non trouves par cx_freeze
excludes = []
packages = []  # nommer les packages utilises

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = ['updatengine.ico', 'LICENSE.txt']

if sys.platform == "win32":
    pass
    # includefiles += [...] : ajouter les recopies specifiques a Windows
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques a Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# niveau d'optimisation pour la compilation en bytecodes
optimize = 2

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True

# construction du dictionnaire des options
options = {
    "path": path,
    "includes": includes,
    "excludes": excludes,
    "packages": packages,
    "include_files": includefiles,
    "bin_path_includes": binpathincludes,
    "create_shared_zip": False,  # <= ne pas generer de fichier zip
    "include_in_shared_zip": False,  # <= ne pas generer de fichier zip
    "compressed": False,  # <= ne pas generer de fichier zip
    "optimize": optimize,
    "silent": silent
}

# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

#############################################################################
# preparation des cibles

base = None
# if sys.platform == "win32":
    # base = "Win32GUI"  # pour application graphique sous Windows
    # base = "Console" # pour application en console sous Windows

# icone = None
if sys.platform == "win32":
    icone = "updatengine.ico"

uecli = Executable(
    script = "updatengine-client.py",
    base = base,
    compress = False,  # <= ne pas generer de fichier zip
    copyDependentFiles = True,
    appendScriptToExe = True,
    appendScriptToLibrary = False,  # <= ne pas generer de fichier zip
    icon = icone,
)

#############################################################################
# creation du setup

setup(
    name = "UpdatEngine client",
    #version = "2.4.9",
    description = "UpdatEngine client",
    author="UpdatEngine",
    options={"build_exe": options},
    executables=[uecli],
)
