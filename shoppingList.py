import sys
from PySide6 import QtCore, QtWidgets as QtW, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog


class mainWindow(QtW.QWidget):
    def __init__(self):
        super().__init__()

        self.finalContent = None
        self.input_addToList = QtW.QLineEdit()
        self.input_addToList.setPlaceholderText("Enter your next need")
        self.addToList_button = QtW.QPushButton("Add your need to shopping list")
        self.import_button = QtW.QPushButton("Import shopping list from file")
        self.compare_button = QtW.QPushButton("compare both lists")
        self.listViewImport = QtW.QTextEdit()
        self.listViewImport.setPlaceholderText(
            "If you see this, you doesnt import any file"
        )
        self.givenList = QtW.QTextEdit()
        self.givenList.setPlaceholderText(
            "If you see this, your shopping list is empty"
        )
        self.clearList_button = QtW.QPushButton("Clear all lists")
        self.exportList_button = QtW.QPushButton("Export your current shopping list")

        self.mainlayout = QtW.QHBoxLayout(self)
        self.V1box_layout = QtW.QVBoxLayout()
        self.V2box_layout = QtW.QVBoxLayout()
        self.mainlayout.addLayout(self.V1box_layout)
        self.mainlayout.addLayout(self.V2box_layout)

        self.V1box_layout.addWidget(self.input_addToList)
        self.V1box_layout.addWidget(self.import_button)
        self.V1box_layout.addWidget(self.listViewImport)
        self.V1box_layout.addWidget(self.clearList_button)

        self.V2box_layout.addWidget(self.addToList_button)
        self.V2box_layout.addWidget(self.compare_button)
        self.V2box_layout.addWidget(self.givenList)
        self.V2box_layout.addWidget(self.exportList_button)

        self.addToList_button.clicked.connect(self.__addStrToList)
        self.clearList_button.clicked.connect(self.__clearList)
        self.import_button.clicked.connect(self.__open_file_dialog)
        self.compare_button.clicked.connect(self.__compare_lists)
        self.exportList_button.clicked.connect(self.__exportList)

    def __addStrToList(self):
        self.givenList.append(self.input_addToList.text())

    def __clearList(self):
        self.givenList.clear()
        self.listViewImport.clear()

    def __open_file_dialog(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Datei auswählen",
            "",
            "Alle Dateien (*);;Textdateien (*.txt)",
            options=options,
        )
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.listViewImport.clear()
                self.listViewImport.append(file_content)

    def __compare_lists(self):
        self.givenList_set = self.givenList.toPlainText()
        self.givenList_words = self.givenList_set.split()
        self.content_givenList = set(self.givenList_words)

        self.importList_set = self.listViewImport.toPlainText()
        self.importList_words = self.importList_set.split()
        self.content_importList = set(self.importList_words)

        self.finalContent = "\n".join(
            self.content_givenList.union(self.content_importList)
        )
        self.givenList.clear()
        self.givenList.append(self.finalContent)

    def __exportList(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "w") as file:
                file.write(str(self.finalContent))


if __name__ == "__main__":
    app = QtW.QApplication([])

    widget = mainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
