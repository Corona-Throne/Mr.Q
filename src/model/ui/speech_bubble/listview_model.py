from copy import deepcopy

from PyQt5.QtCore import QAbstractListModel, Qt

class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []
        self.backup = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text, color):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.recover_messages()
            self.messages.append((who, text, color, True))
            self.backup.append((who, text, color, False))
            # Trigger refresh.
            self.layoutChanged.emit()

    def recover_messages(self):
        self.messages = deepcopy(self.backup)