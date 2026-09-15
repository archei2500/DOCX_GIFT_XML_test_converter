from PyQt5 import QtCore, QtGui, QtWidgets
import attributes
import QuestionChangingWindow as QCW

class QCWindow_shell(QtWidgets.QDialog, QCW.Ui_QCWindow):
    def __init__(self, attr, text):
        super().__init__()
        self.attr = attr
        self.setupUi(self)
        self.set_values(attr, text)
        self.set_bindings()

    def set_values(self, attr, text):
        self.question_text.setText(text)
        self.lineEdit_display_name_q.setText(attr.display_name)
        n = ["always", "never"].index(attr.show_correctness)
        self.comboBox_show_correctness_q.setCurrentIndex(n)
        n = ["never", "always", "answered", "attempted", "closed", "finished", "correct_or_past_due", "past_due"].index(attr.showanswer)
        self.comboBox_showanswer_q.setCurrentIndex(n)
        n = ["per_student", "always", "on_reset", "never"].index(attr.rerandomize)
        self.comboBox_rerandomize_q.setCurrentIndex(n)
        self.spinBox_max_attempts_q.setProperty("value", int(attr.max_attempts))
        self.doubleSpinBox_weight_q.setProperty("value", float(attr.weight))
        if attr.show_reset_button == "true":
            self.checkBox_show_reset_button_q.setChecked(True)
        else:
            self.checkBox_show_reset_button_q.setChecked(False)
        if attr.submission_wait_seconds != None:
            self.spinBox_submission_wait_seconds_q.setProperty("value", int(attr.submission_wait_seconds))
        else:
            self.spinBox_submission_wait_seconds_q.setProperty("value", 0)

    def set_bindings(self):
        self.confirm.clicked.connect(self.conf)

    def conf(self):
        display_name = self.lineEdit_display_name_q.text()
        show_correctness = self.comboBox_show_correctness_q.currentText()
        showanswer = self.comboBox_showanswer_q.currentText()
        rerandomize = self.comboBox_rerandomize_q.currentText()
        max_attempts = self.spinBox_max_attempts_q.value()
        weight = round(self.doubleSpinBox_weight_q.value(), 4)
        show_reset_button = self.checkBox_show_reset_button_q.isChecked()
        submission_wait_seconds = self.spinBox_submission_wait_seconds_q.value()

        #display_name
        if display_name != "":
            self.attr.display_name = display_name
        #show_correctness
        if show_correctness == "Всегда":
            self.attr.show_correctness = "always"
        elif show_correctness == "Никогда":
            self.attr.show_correctness = "never"
        elif show_correctness == "<не добавлять>":
            self.attr.show_correctness = None
        else:
            raise
            
        #showanswer
        if showanswer == "Никогда":
            self.attr.showanswer = "never"
        elif showanswer == "Всегда":
            self.attr.showanswer = "always"
        elif showanswer == "Дан ответ":
            self.attr.showanswer = "answered"
        elif showanswer == "Использована попытка":
            self.attr.showanswer = "attempted"
        elif showanswer == "Закрыт":
            self.attr.showanswer = "closed"
        elif showanswer == "Ответ верен или прошёл срок сдачи":
            self.attr.showanswer = "correct_or_past_due"
        elif showanswer == "Прошёл срок сдачи":
            self.attr.showanswer = "past_due"
        elif showanswer == "Выполнен":
            self.attr.showanswer = "finished"
        else:
            raise
        #rerandomize
        if rerandomize == "Никогда":
            self.attr.rerandomize = "never"
        elif rerandomize == "Для каждого студента":
            self.attr.rerandomize = "per_student"
        elif rerandomize == "При сбросе":
            self.attr.rerandomize = "on_reset"
        elif rerandomize == "Всегда":
            self.attr.rerandomize = "always"
        else:
            raise
        #max_attenpts
        if max_attempts == 0:
            self.attr.max_attempts = "null"
        else:
            self.attr.max_attempts = str(max_attempts)
        #weight
        self.attr.weight =  str(weight)
        #reset_button
        if show_reset_button:
            self.attr.show_reset_button = "True"
        else:
            self.attr.show_reset_button = "False"
        #submission_wait_seconds
        if submission_wait_seconds != 0:
            self.attr.submission_wait_seconds =  str(submission_wait_seconds)
        self.close()

    def get_attr(self):
        return self.attr

class QCWindow_toler(QCWindow_shell):

    def setupUi(self, MainWindow):
        super().setupUi(self)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("MainWindow", "Погрешность"))
        self.lineEdit.setText(_translate("MainWindow", "1%"))

    def set_bindings(self):
        super().set_bindings()
        val_toler = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,255}([.]{1,1}[0-9]{1,255}){0,1}%{0,1}"))
        self.lineEdit.setValidator(val_toler)
        self.lineEdit.textChanged[str].connect(self.toler_repaint)

    def set_values(self, attr, text):
        super().set_values(attr, text)
        self.lineEdit.setText(attr.tolerance)

    def toler_repaint(self):
        code = self.validate_toler(None)
        if code == 0:
            self.lineEdit.setStyleSheet("color: red;")
        elif code == 1:
            self.lineEdit.setStyleSheet("color: orange;")
        elif code == 2:
            self.lineEdit.setStyleSheet("color: black;")

    def validate_toler(self, something):
        regex = QtCore.QRegExp("[0-9]{1,255}([.]{1,1}[0-9]{1,255}){0,1}%{0,1}")
        tmp = QtGui.QRegExpValidator(regex, self.lineEdit)
        state, new_text, new_position = tmp.validate(self.lineEdit.text(), self.lineEdit.cursorPosition())
        return(state)

    def conf(self):
        tolerance = self.lineEdit.text()
        if self.validate_toler(None) == 2:
            self.attr.tolerance = tolerance
        else:
            print("Warning! The entered error value is invalid. Used standard - 1%")
            self.attr.tolerance = "1%"
        super().conf()
        self.close()

class QCWindow_math_expression(QCWindow_toler):

    def setupUi(self, MainWindow):
        super().setupUi(self)
        self.label_reg_type = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_reg_type.setObjectName("label_reg_type")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_reg_type)
        self.comboBox_reg_type = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_reg_type.setObjectName("comboBox_reg_type")
        self.comboBox_reg_type.addItem("")
        self.comboBox_reg_type.addItem("")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.comboBox_reg_type)
        self.label_trailing_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_trailing_text.setObjectName("label_trailing_text")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_trailing_text)
        self.lineEdit_trailing_text = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_trailing_text.setObjectName("lineEdit_trailing_text")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.lineEdit_trailing_text)
        _translate = QtCore.QCoreApplication.translate
        self.label_reg_type.setText(_translate("MainWindow", "Тип поля для ввода"))
        self.comboBox_reg_type.setItemText(0, _translate("MainWindow", "Чувств. к регистру"))
        self.comboBox_reg_type.setItemText(1, _translate("MainWindow", "Нечувств. к регистру"))
        self.label_trailing_text.setText(_translate("MainWindow", "Текст после поля ввода"))

    def set_values(self, attr, text):
        super().set_values(attr, text)
        try:
            n = ["cs", "ci"].index(attr.reg_type)
            self.comboBox_reg_type.setCurrentIndex(n)
        except ValueError:
            self.comboBox_reg_type.setCurrentIndex(0)
        if attr.trailing_text != None:
            self.lineEdit_trailing_text.setText(attr.trailing_text)
        else:
            self.lineEdit_trailing_text.setText("")


    def conf(self):
        reg_type = self.comboBox_reg_type.currentText()
        trailing_text = self.lineEdit_trailing_text.text()
        if reg_type == "Чувств. к регистру":
            self.attr.reg_type = "cs"
        elif reg_type == "Нечувств. к регистру":
            self.attr.reg_type = "ci"
        if trailing_text != "":
            self.attr.trailing_text = trailing_text
        super().conf()
        self.close()

class QCWindow_numeric(QCWindow_toler):

    def setupUi(self, MainWindow):
        super().setupUi(self)
        self.label_trailing_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_trailing_text.setObjectName("label_trailing_text")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_trailing_text)
        self.lineEdit_trailing_text = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_trailing_text.setObjectName("lineEdit_trailing_text")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lineEdit_trailing_text)
        _translate = QtCore.QCoreApplication.translate
        self.label_trailing_text.setText(_translate("MainWindow", "Текст после поля ввода"))

    def set_values(self, attr, text):
        super().set_values(attr, text)
        if attr.trailing_text != None:
            self.lineEdit_trailing_text.setText(attr.trailing_text)
        else:
            self.lineEdit_trailing_text.setText("")

    def conf(self):
        trailing_text = self.lineEdit_trailing_text.text()
        if trailing_text != "":
            self.attr.trailing_text = trailing_text
        super().conf()
        self.close()

class QCWindow_text_match(QCWindow_shell):
    def setupUi(self, MainWindow):
        super().setupUi(self)
        self.label_reg_type = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_reg_type.setObjectName("label_reg_type")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_reg_type)
        self.comboBox_reg_type = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_reg_type.setObjectName("comboBox_reg_type")
        self.comboBox_reg_type.addItem("")
        self.comboBox_reg_type.addItem("")
        self.comboBox_reg_type.addItem("")
        self.comboBox_reg_type.addItem("")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.comboBox_reg_type)
        self.label_trailing_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_trailing_text.setObjectName("label_trailing_text")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_trailing_text)
        self.lineEdit_trailing_text = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_trailing_text.setObjectName("lineEdit_trailing_text")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lineEdit_trailing_text)
        _translate = QtCore.QCoreApplication.translate
        self.label_reg_type.setText(_translate("MainWindow", "Тип поля для ввода"))
        self.comboBox_reg_type.setItemText(0, _translate("MainWindow", "Чувств. к регистру"))
        self.comboBox_reg_type.setItemText(1, _translate("MainWindow", "Нечувств. к регистру"))
        self.comboBox_reg_type.setItemText(2, _translate("MainWindow", "Для рег. выражений, чувств. к регистру"))
        self.comboBox_reg_type.setItemText(3, _translate("MainWindow", "Для рег. выражений, нечувств. к регистру"))
        self.label_trailing_text.setText(_translate("MainWindow", "Текст после поля ввода"))

    def set_values(self, attr, text):
        super().set_values(attr, text)
        try:
            n = ["cs", "ci", "regexp cs", "regexp ci"].index(attr.reg_type)
            self.comboBox_reg_type.setCurrentIndex(n)
        except ValueError:
            self.comboBox_reg_type.setCurrentIndex(0)
        if attr.trailing_text != None:
            self.lineEdit_trailing_text.setText(attr.trailing_text)
        else:
            self.lineEdit_trailing_text.setText("")

    def conf(self):
        reg_type = self.comboBox_reg_type.currentText()
        trailing_text = self.lineEdit_trailing_text.text()
        if reg_type == "Чувств. к регистру":
            self.attr.reg_type = "cs"
        elif reg_type == "Нечувств. к регистру":
            self.attr.reg_type = "ci"
        elif reg_type == "Для рег. выражений, чувств. к регистру":
            self.attr.reg_type = "regexp cs"
        elif reg_type == "Для рег. выражений, нечувств. к регистру":
            self.attr.reg_type = "regexp ci"
        if trailing_text != "":
            self.attr.trailing_text = trailing_text
        super().conf()
        self.close()



