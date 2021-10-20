
import sys
from PySide2.QtWidgets import QApplication
from pyforg import gui_events
import version


def go():

	app = QApplication([])
	window = gui_events.PyFOrg()
	window.setWindowTitle("AutoOrg - v%s" % version.VERSION)
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	go()

