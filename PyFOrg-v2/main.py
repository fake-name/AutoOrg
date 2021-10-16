
import sys
from PySide2.QtWidgets import QApplication
import gui_events


def go():

	app = QApplication([])
	window = gui_events.PyFOrg()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	go()

