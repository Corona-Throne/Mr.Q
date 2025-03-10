from PyQt5 import QtWidgets

from src.controller import MrQ_window

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MrQ_window()
    window.showFullScreen()
    sys.exit(app.exec_())