# -*- mode: python -*-

import os.path

# Soooo horrible.
import sys

version = "UNKNOWN"
with open("version.py", "r") as fp:
	for line in fp.readlines():
		if line.strip().startswith("VERSION"):
			version = line.split("=")[-1].strip().replace('"', "")

print("App Version: ", version)
block_cipher = None


a = Analysis(['main.py'],
			pathex=['C:/code/pyFOrg/PyFOrg-v2'],
			binaries=None,
			datas=None,
			hiddenimports=[
				],
			hookspath=None,
			runtime_hooks=None,
			excludes = [
				"numpy.core._dotblas.pyd",
				"scipy.linalg._fblas.pyd",
				"scipy.linalg._flapack.pyd",
				"scipy.linalg._flinalg.pyd",
				"scipy.sparse.linalg.dsolve._superlu",
				"scipy.sparse.linalg.eigen.arpack._arpack",
				"scipy.integrate.vode",
				"scipy.integrate.lsoda",
				"scipy.integrate",
				"tcl",
				"_tkinter",
				"tkinter",
				"_tkinter",
				"Tkinter"
				"matplotlib",
				'matplotlib.backends._backend_agg',
				'matplotlib._png',
				'scipy.ndimage._ni_label',
				'matplotlib._image',
				'matplotlib._path',
				'matplotlib._tri',
				'matplotlib.ttconv',
				'pyzmq',
				'zmq',
				'ipython',
				'IPython',
				'requests',
				'lib2to3',
				'matplotlib',
				'qt4',
				'pyqt4',
				'_ssl',
				'_sqlite3',
				'_curses',
				'PIL',
				'tornado',
				'wx',
			],
			cipher=block_cipher)


excludes = [
	'sqlite3.dll',
	'tcl85.dll',
	'tk85.dll',
	'_tkinter',
	"tcl86t.dll",
	"tk86t.dll",
]

fuzzy_excludes = [
	# 'mkl',
	# 'libopenblas',
	'opengl32sw',
]

# I'm not using matplotlib
for entry in a.datas[:]:
	if os.path.dirname(entry[1]).startswith("C:/Python38/Lib/site-packages/matplotlib"):
		a.datas.remove(entry)

# Or anything in the "excludes" list
for item in a.binaries[:]:
	item_name = item[0]
	if item_name in excludes:
		a.binaries.remove(item)
	elif any([item_name.startswith(tmp) for tmp in fuzzy_excludes]):
		a.binaries.remove(item)


# Make sure the DLLs are present.
for _, fpath, _ in a.binaries:
	assert os.path.exists(fpath), "Missing binary file %s!" % fpath

ONEFILE = True
# ONEFILE = False

pyz = PYZ(a.pure, a.zipped_data)

if ONEFILE:
	exe = EXE(pyz,
				a.scripts,
				a.binaries,
				a.zipfiles,
				a.datas,
				# exclude_binaries=True,
				name    = 'PyFOrg - {ver}.exe'.format(ver=version),
				debug   = False,
				strip   = None,
				upx     = False,
				console = True,
				)

else:
	exe = EXE(pyz,
			  a.scripts,
			  exclude_binaries=True,
				name    = 'PyFOrg - {ver}.exe'.format(ver=version),
			  strip=None,
			  upx=False,
			  debug=1,
			  console=True )

	coll = COLLECT(exe,
				   a.binaries,
				   a.zipfiles,
				   a.datas,
				   strip=None,
				   upx=False,
				   name='PyFOrg')
