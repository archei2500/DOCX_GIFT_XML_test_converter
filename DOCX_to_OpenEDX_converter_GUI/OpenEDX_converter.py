import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import docx_file_parsing
import drop_OLX
import MainWindow
import attributes
from datetime import datetime

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
        self.setObjectName("OpenEDX_converter")
        self.set_bindings()

    def set_bindings(self):
        self.dir_browse.clicked.connect(self.browse_dir)
        self.file_browse.clicked.connect(self.browse_file)
        self.convert.clicked.connect(self.start_convert)
        stream = EmittingStream()
        stream.signal.connect(self.add_to_TextBrowser)
        sys.stdout = stream
        #sys.stderr = stream
        val = QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9_]{0,255}"))
        val_toler = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,255}([.]{1,1}[0-9]{1,255}){0,1}%{0,1}"))
        self.lineEdit_library.setValidator(val)
        self.lineEdit_org.setValidator(val)
        self.lineEdit.setValidator(val_toler)
        #self.lineEdit.textChanged[str].connect(self.validate_toler)

    def validate_toler(self, somthing):
        regex = QtCore.QRegExp("[0-9]{1,255}([.]{1,1}[0-9]{1,255}){0,1}%{0,1}")
        tmp = QtGui.QRegExpValidator(regex, self.lineEdit)
        state, new_text, new_position = tmp.validate(self.lineEdit.text(), self.lineEdit.cursorPosition())
        return(state)


    def __del__(self):
        sys.stdout = sys.__stdout__

    def add_to_TextBrowser(self, text):
        #self.textBrowser.append(text) It works strangely
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def browse_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory != "":
            self.lineEdit_dir.setText(directory)

    def browse_file(self):
        file, filter = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", "", "(*.docx)")
        if file != "":
            self.lineEdit_file.setText(file)

    def start_convert(self):
        library_library = self.lineEdit_library.text()
        library_display_name = self.lineEdit_display_name.text()
        library_org = self.lineEdit_org.text()
        library_use_latex_compiler = self.checkBox_use_latex_compiler.isChecked()
        library_show_correctness = self.comboBox_show_correctness.currentText()
        library_showanswer = self.comboBox_showanswer.currentText()
        library_rerandomize = self.comboBox_rerandomize.currentText()
        library_show_reset_button = self.checkBox_show_reset_button.isChecked()
        library_max_attempts = self.spinBox_max_attempts.value()
        time = ""
        if self.checkBox_time.isChecked():
            time += str(datetime.now()).replace(" ", "_").replace(".", "-").replace(":", "-")
            library_library += "_" + time

        questions_display_name = self.lineEdit_display_name_q.text()
        questions_show_correctness = self.comboBox_show_correctness_q.currentText()
        questions_showanswer = self.comboBox_showanswer_q.currentText()
        questions_rerandomize = self.comboBox_rerandomize_q.currentText()
        questions_max_attempts = self.spinBox_max_attempts_q.value()
        questions_weight = round(self.doubleSpinBox_weight_q.value(), 4)
        questions_show_reset_button = self.checkBox_show_reset_button_q.isChecked()
        questions_tolerance = self.lineEdit.text()
        questions_submission_wait_seconds = self.spinBox_submission_wait_seconds_q.value()
        questions_individually = self.checkBox_individually.isChecked()
        questions_reg_type_m = self.comboBox_reg_type_m.currentText()
        questions_reg_type_t = self.comboBox_reg_type_t.currentText()
        questions_trailing_text_m = self.lineEdit_trailing_text_m.text()
        questions_trailing_text_n = self.lineEdit_trailing_text_n.text()
        questions_trailing_text_t = self.lineEdit_trailing_text_t.text()

        file = self.lineEdit_file.text()
        dir = self.lineEdit_dir.text()

        if os.path.exists(file) and os.path.exists(dir) and os.path.isfile(file) and os.path.isdir(dir):
            if file[-5 : ] != ".docx":
                print("This is not docx file.")
                return
        else:
            print("Path to file or directory incorrect.")
            return

        l_attr = attributes.library_attributes()
        q_attr = attributes.default_problem_attributes()

        #library
        if library_library != "":
            l_attr.library = library_library
        #display_name
        if library_display_name != "":
            l_attr.display_name = library_display_name
        #org
        if library_org != "":
            l_attr.org = library_org
        #use_latex_compiler
        if library_use_latex_compiler:
            l_attr.use_latex_compiler = "True"
        else:
            l_attr.use_latex_compiler = "False"
        #show_correctness
        if library_show_correctness == "Всегда":
            l_attr.show_correctness = "always"
        elif library_show_correctness == "Никогда":
            l_attr.show_correctness = "never"
        elif library_show_correctness == "<не добавлять>":
            l_attr.show_correctness = None
        else:
            raise
        #show_answer
        if library_showanswer == "Выполнен":
            l_attr.showanswer = "finished"
        elif library_showanswer == "Всегда":
            l_attr.showanswer = "always"
        elif library_showanswer == "Дан ответ":
            l_attr.showanswer = "answered"
        elif library_showanswer == "Использована попытка":
            l_attr.showanswer = "attempted"
        elif library_showanswer == "Закрыт":
            l_attr.showanswer = "closed"
        elif library_showanswer == "Ответ верен или прошёл срок сдачи":
            l_attr.showanswer = "correct_or_past_due"
        elif library_showanswer == "Прошёл срок сдачи":
            l_attr.showanswer = "past_due"
        elif library_showanswer == "Никогда":
            l_attr.showanswer = "never"
        elif library_showanswer == "<не добавлять>":
            l_attr.showanswer = None
        else:
            raise
        #rerandomize
        if library_rerandomize == "Никогда":
            l_attr.rerandomize = "never"
        elif library_rerandomize == "Для каждого студента":
            l_attr.rerandomize = "per_student"
        elif library_rerandomize == "Всегда":
            l_attr.rerandomize = "always"
        elif library_rerandomize == "При сбросе":
            l_attr.rerandomize = "on_reset"
        else:
            raise
        #show_reset_button
        if library_show_reset_button:
            l_attr.show_reset_button = "True"
        else:
            l_attr.show_reset_button = "False"
        #max_attempts
        if library_max_attempts == 0:
            l_attr.max_attempts = "null"
        else:
            l_attr.max_attempts = str(library_max_attempts)

        #display_name
        if questions_display_name != "":
            q_attr.display_name = questions_display_name
        #show_correctness
        if questions_show_correctness == "Всегда":
            q_attr.show_correctness = "always"
        elif questions_show_correctness == "Никогда":
            q_attr.show_correctness = "never"
        elif questions_show_correctness == "<не добавлять>":
            q_attr.show_correctness = None
        else:
            raise
            
        #showanswer
        if questions_showanswer == "Никогда":
            q_attr.showanswer = "never"
        elif questions_showanswer == "Всегда":
            q_attr.showanswer = "always"
        elif questions_showanswer == "Дан ответ":
            q_attr.showanswer = "answered"
        elif questions_showanswer == "Использована попытка":
            q_attr.showanswer = "attempted"
        elif questions_showanswer == "Закрыт":
            q_attr.showanswer = "closed"
        elif questions_showanswer == "Ответ верен или прошёл срок сдачи":
            q_attr.showanswer = "correct_or_past_due"
        elif questions_showanswer == "Прошёл срок сдачи":
            q_attr.showanswer = "past_due"
        elif questions_showanswer == "Выполнен":
            q_attr.showanswer = "finished"
        else:
            raise
        #rerandomize
        if questions_rerandomize == "Никогда":
            q_attr.rerandomize = "never"
        elif questions_rerandomize == "Для каждого студента":
            q_attr.rerandomize = "per_student"
        elif questions_rerandomize == "При сбросе":
            q_attr.rerandomize = "on_reset"
        elif questions_rerandomize == "Всегда":
            q_attr.rerandomize = "always"
        else:
            raise
        #max_attenpts
        if questions_max_attempts == 0:
            q_attr.max_attempts = "null"
        else:
            q_attr.max_attempts = str(questions_max_attempts)
        #weight
        q_attr.weight =  str(questions_weight)
        #reset_button
        if questions_show_reset_button:
            q_attr.show_reset_button = "true"
        else:
            q_attr.show_reset_button = "false"
        #tolerance
        if self.validate_toler(None) == 2:
            q_attr.tolerance = questions_tolerance
        else:
            print("Warning! The entered error value is invalid. Used standard - 1%")
            q_attr.tolerance = "1%"
        #submission_wait_seconds
        if questions_submission_wait_seconds != 0:
            q_attr.submission_wait_seconds =  str(questions_submission_wait_seconds)
        #reg_type
        if questions_reg_type_m == "Чувств. к регистру":
            q_attr.reg_type_m = "cs"
        elif questions_reg_type_m == "Нечувств. к регистру":
            q_attr.reg_type_m = "ci"
        if questions_reg_type_t == "Чувств. к регистру":
            q_attr.reg_type_t = "cs"
        elif questions_reg_type_t == "Нечувств. к регистру":
            q_attr.reg_type_t = "ci"
        elif questions_reg_type_t == "Для рег. выражений, чувств. к регистру":
            q_attr.reg_type_t = "regexp cs"
        elif questions_reg_type_t == "Для рег. выражений, нечувств. к регистру":
            q_attr.reg_type_t = "regexp ci"
        #trailing_text
        if questions_trailing_text_m != "":
            q_attr.trailing_tex_m = questions_trailing_text_m
        if questions_trailing_text_n != "":
            q_attr.trailing_tex_n = questions_trailing_text_n
        if questions_trailing_text_t != "":
            q_attr.trailing_tex_t = questions_trailing_text_t

        lib, problems, problems_names = docx_file_parsing.parse_file(file, l_attr, q_attr, questions_individually)
        drop_OLX.drop_files(dir, lib, problems, problems_names, library_library)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow_shell()
window.show()
app.exec_()
