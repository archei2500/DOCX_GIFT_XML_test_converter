import xml_elements

class choicehint(xml_elements.string_only_container):

    def __init__(self, dash, hint):
        str = (hint.replace("\n"," ")).strip()
        super().__init__(dash, str)
        self.name = "choicehint"

    def add_selected(self, value):
        value_str = "false"
        if value:
            value_str = "true"
        self.add_property("selected", value_str)

class choice(xml_elements.fully_functional_container):

    def __init__(self, dash, answer):
        feedback_start = answer.find("\nFeedback:")
        if feedback_start == -1:
            feedback_start = len(answer)
        str = ((answer[0 : feedback_start]).replace("\n"," ")).strip()
        super().__init__(dash, str)
        self.name = "choice"
        if len(answer) - feedback_start > 10:
            self.add_choicehint(answer[feedback_start + 10: len(answer)])

    def add_correct(self, type_of_answer):
        type_str = "false"
        if type_of_answer:
            type_str = "true"
        self.add_property("correct", type_str)

    def add_choicehint(self, hint):
        new_choicehint = choicehint(self.dash + 2, hint)
        new_choicehint.add_selected(True)
        self.list.append(new_choicehint)

class checkboxgroup(xml_elements.intermediate_container):

    def __init__(self, dash, answers):
        super().__init__(dash)
        self.name = "checkboxgroup"
        i = 0
        ans_i = 0
        while(i != -1 and i + 4 < len(answers)):
            if answers[i : i + 3] == "\n" + xml_elements.ALPHABET[ans_i] + ':':
                type_of_answer = False
                start_of_answer = i + 3
            elif answers[i : i + 4] == "\n*" + xml_elements.ALPHABET[ans_i] + ':':
                type_of_answer = True
                start_of_answer = i + 4
            else:
                raise xml_elements.IncorrectSyntax("Incorrect syntax of the answer entry")
            next = answers.find("\n" + xml_elements.ALPHABET[ans_i+1] + ":", start_of_answer + 2)
            next_truth = answers.find("\n*", start_of_answer + 2)
            if next == -1:
                next = len(answers) + 1
            if next_truth == -1:
                next_truth = len(answers) + 1
            end_of_answer = min(next_truth, next)
            if end_of_answer == len(answers) + 1:
                end_of_answer = len(answers)
            self.add_choice(answers[start_of_answer : end_of_answer], type_of_answer)
            ans_i += 1
            i = end_of_answer

    def add_choice(self, answer, type_of_answer):
        new_choice = choice(self.dash + 2, answer)
        new_choice.add_correct(type_of_answer)
        self.list.append(new_choice)

class choiceresponse(xml_elements.intermediate_container):
    def __init__(self, dash, full_question):
        super().__init__(dash)
        self.name = "choiceresponse"
        next = full_question.find("\n*")
        next_truth = full_question.find("\nA:")
        if next == -1:
            next = len(full_question) + 1
        if next_truth == -1:
            next_truth = len(full_question) + 1
        start_of_answers = min(next_truth, next)
        if start_of_answers == len(full_question) + 1:
            start_of_answers = len(full_question)
        self.add_label(full_question[0 : start_of_answers])
        self.add_checkboxgroup(full_question[start_of_answers : len(full_question)])

    def add_label(self, question):
        new_label = xml_elements.label(self.dash + 2, question)
        self.list.append(new_label)

    def add_checkboxgroup(self, answers):
        new_checkboxgroup = checkboxgroup(self.dash + 2, answers)
        self.list.append(new_checkboxgroup)

    #def add_shuffle(self):
    #    self.add_property("shuffle", "true")

    def add_partial_credit(self):
        self.add_property("partial_credit", "EDC")




