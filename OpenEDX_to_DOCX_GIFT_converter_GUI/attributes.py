class file_attributes():
    def __init__(self):
        self.file_name = "test.txt"
        self.file_format = "gift"
        self.test_name = "Test."


class problem_attributes():
    def __init__(self):
        #self.course_edit_method="Studio"
        self.display_name = "Вопрос"
        self.tolerance = "1%"
        self.allow_numbering = "false"


class default_problem_attributes(problem_attributes):
    def __init__(self):
        super().__init__()

    def copy(self, other, type = ""):
        other.display_name = self.display_name
        other.tolerance = self.tolerance
        other.allow_numbering = self.allow_numbering
