from PyQt5 import QtWidgets

class GifPlayer:

    def __init__(self, widget: QtWidgets.QWidget) -> None:
        self.movie = widget.movie()
        self.movie.start()
        self.movie.setPaused(True)

    def play(self):
        self.movie.start()

    def stop(self):
        self.movie.setPaused(True)