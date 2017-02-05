"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app --includes sip
"""

#Blah Blah

import os
import sys
import glob
from setuptools import setup
if sys.platform == 'darwin':
    import py2app
elif sys.platform == 'win32':
    import py2exe
sys.setrecursionlimit(100000)

def find_data_files(sources, targets, patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """

    ret = {}
    for i, source in enumerate(sources):
        target = targets[i]
        if glob.has_magic(source) or glob.has_magic(target):
            raise ValueError("Magic not allowed in src, target")
        pattern = os.path.join(source, patterns[i])
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
    return sorted(ret.items())

VERSION = os.environ['DEEPN_VERSION']
BUNDLE_VERSION = VERSION.replace(".", "")

APP = ['gene_count_gui.py']
INCLUDES = ['PyQt4', 'glob', 'cPickle', 'time', 'sys', 'os', 'pydoc',
                                                'json', 'numbers', 'hashlib', 'decimal', 'pyqtgraph']
OPTIONS = {'argv_emulation': True,
           'iconfile' : 'icon/Icon2.icns',
           'plist': {'CFBundleGetInfoString': 'Gene Count',
                     'CFBundleIdentifier': 'edu.uiowa.robertpiper.deepn.gene_count',
                     'CFBundleShortVersionString': VERSION,
                     'CFBundleName': 'Gene Count',
                     'CFBundleVersion': BUNDLE_VERSION,
                     'NSHumanReadableCopyright': '(c) 2016 Venkatramanan Krishnamani, Robert C. Piper, Mark Stammnes'},
           'includes': INCLUDES,
           'excludes': ['PyQt4.QtDesigner', 'PyQt4.QtNetwork', 'PyQt4.QtOpenGL', 'PyQt4.QtScript', 'PyQt4.QtSql', 'PyQt4.QtTest', 'PyQt4.QtWebKit', 'PyQt4.QtXml', 'PyQt4.phonon'],
           }
DATA_FILES = find_data_files(['functions', 'libraries', 'libraries/joblib', 'ui', 'dictionaries', '.', 'ui/Windows'],
                             ['functions', 'libraries', 'libraries/joblib', 'ui', 'dictionaries', '', 'ui/Windows'],
                             ['*.py', '*.py', '*.py', '*.ui', '*', '*.txt', '*.ui'])
if sys.platform == 'darwin':
    setup(
        app=APP,
        name='Gene Count',
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
        author='Venkatramanan Krishnamani, Robert C. Piper, Mark Stammnes',
        data_files=DATA_FILES,
    )
elif sys.platform == 'win32':
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
            if os.path.basename(pathname).lower() in ("msvcp71.dll", "dwmapi.dll", "'msvcp90.dll'"):
                    return 0
            return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL
    setup(
        console=APP,
        version=VERSION,
        description='Gene Count',
        author='Venkatramanan Krishnamani, Robert C. Piper, Mark Stammnes',
        # windows=[{"script":'gene_count_gui.py',
        #            "icon_resources": [(1, "icon/Icon2.ico")],
        #            "dest_base":"Gene Count"
        #         }],
        data_files=DATA_FILES,
        options={"py2exe": {'includes': INCLUDES,
                            "optimize": 2,
                            "compressed": 2,
                            "bundle_files": 1,
                            "dist_dir": "dist\Gene Count"
                            }}
    )