import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import file_parsing
import MainWindow
import attributes


class EmittingStream(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def write(self, text):
        self.signal.emit(text)


class MainWindow_shell(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName("Questions_converter_inverse")
        self.set_bindings()

    def set_bindings(self):
        self.dir_browse.clicked.connect(self.browse_dir)
        self.dir2_browse.clicked.connect(self.browse_dir2)
        self.convert.clicked.connect(self.start_convert)
        stream = EmittingStream()
        stream.signal.connect(self.add_to_TextBrowser)
        sys.stdout = stream
        val = QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9_.]{0,255}"))
        val_toler = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,255}([.]{1,1}[0-9]{1,255}){0,1}%{0,1}"))
        self.lineEdit_res_name.setValidator(val)
        self.lineEdit.setValidator(val_toler)
        self.lineEdit.textChanged[str].connect(self.validate_toler)

    def validate_toler(self, somthing):
        regex = QtCore.QRegExp("[0-9]{1,255}([.]{1,1}[0-9]{1,255}){0,1}%{0,1}")
        tmp = QtGui.QRegExpValidator(regex, self.lineEdit)
        state, new_text, new_position = tmp.validate(self.lineEdit.text(), self.lineEdit.cursorPosition())
        return state

    def __del__(self):
        sys.stdout = sys.__stdout__

    def add_to_TextBrowser(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def browse_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory != "":
            self.lineEdit_dir.setText(directory)

    def browse_dir2(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory != "":
            self.lineEdit_file.setText(directory)


    def start_convert(self):
        file_format = self.comboBox_format.currentText()
        res_file_name = self.lineEdit_res_name.text()
        test_name = self.lineEdit_test_name.text()
        questions_display_name = self.lineEdit_display_name_q.text()
        allow_numbering = self.checkBox_allow_numbering.isChecked()
        questions_tolerance = self.lineEdit.text()

        dir = self.lineEdit_dir.text()
        file_dir = self.lineEdit_file.text()

        if not(os.path.exists(file_dir) and os.path.exists(dir) and os.path.isdir(file_dir) and os.path.isdir(dir)):
            print("Path to one or both of the directories incorrect.")
            return
        # проверка структуры директории
        if not(os.path.exists(dir + "/policies") and os.path.isdir(dir + "/policies") and
               os.path.exists(dir + "/problem") and os.path.isdir(dir + "/problem") and
               os.path.isfile(dir + "/library.xml")):
            print("The library directory you specified does not have the required hierarchy of files and folders.")
            return

        q_attr = attributes.default_problem_attributes()
        f_attr = attributes.file_attributes()

        # file format
        if file_format == "GIFT":
            f_attr.file_format = "gift"
        else:
            f_attr.file_format = "docx"
        # result file name
        if res_file_name != "":
            if file_format == "GIFT":
                if res_file_name.rfind(".") != -1:
                    if res_file_name.rfind(".") == len(res_file_name) - 1:
                        res_file_name += "txt"
                else:
                    res_file_name += ".txt"
            else:
                if res_file_name[-5:] != ".docx":
                    res_file_name += ".docx"
            f_attr.file_name = res_file_name
        if test_name != "":
            f_attr.test_name = test_name

        # display_name
        if questions_display_name != "":
            q_attr.display_name = questions_display_name
        q_attr.allow_numbering = "true" if allow_numbering else "false"

        # tolerance
        if self.validate_toler(None) == 2:
            q_attr.tolerance = questions_tolerance
        else:
            print("Warning! The entered error value is invalid. Used standard - 1%")
            q_attr.tolerance = "1%"

        if file_format == "GIFT":
            file_parsing.parse_xml_to_gift(dir, file_dir, f_attr, q_attr)
        else:
            file_parsing.parse_xml_to_docx(dir, file_dir, f_attr)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow_shell()
window.show()
app.exec_()
