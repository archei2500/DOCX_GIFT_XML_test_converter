import xml_elements

class additional_answer(xml_elements.single_tag):
    def __init__(self, dash, answer):
        super().__init__(dash)
        self.name = "additional_answer"
        self.add_answer(answer)

    def add_answer(self, answer):
        self.add_property("answer", answer)

class correcthint(xml_elements.string_only_container):
    def __init__(self, dash, hint):
        super().__init__(dash, hint.replace("\n"," ").strip())
        self.name = "correcthint"

class formulaequationinput(xml_elements.single_tag):
    def __init__(self, dash):
        super().__init__(dash)
        self.name = "formulaequationinput"

    def add_trailing_text(self, text):
        self.add_property("trailing_text", text)

class responseparam(xml_elements.single_tag):
    def __init__(self, dash, value):
        super().__init__(dash)
        self.name = "responseparam"
        self.add_tolerance()
        self.add_default(value)

    def add_tolerance(self):
        self.add_property("type", "tolerance")

    def add_default(self, value):
        self.add_property("default", value)

    def set_tolerance(self, toler):
        self.properties["default"] = toler

class numericalresponse(xml_elements.intermediate_container):
    corr_feedback_added = False

    def __init__(self, dash, full_question):
        super().__init__(dash)
        self.name = "numericalresponse"
        self.corr_feedback_added = False
        next_truth = full_question.find("\n*")
        next = full_question.find("\nA:")
        if next == -1:
            next = len(full_question) + 1
        if next_truth == -1:
            next_truth = len(full_question) + 1
        start_of_answers = min(next_truth, next)
        if start_of_answers == len(full_question) + 1:
            start_of_answers = len(full_question)
        self.add_label(full_question[0 : start_of_answers])
        self.add_answers(full_question[start_of_answers : len(full_question)])
        self.add_formulaequationinput()
        self.add_responseparam()

    def add_answers(self, answers):
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
            if type_of_answer:
                self.add_answer(answers[start_of_answer : end_of_answer])
            ans_i += 1
            i = end_of_answer

    def add_answer(self, answer):
        def_feedback = answer.find("\nDefault Feedback:")
        def_feedback_text = ""
        if def_feedback > -1:
            def_feedback_text = answer[def_feedback + 18: ]
            answer = answer[: def_feedback]
        feedback_start = answer.find("\nFeedback:")
        if feedback_start == -1:
            feedback_start = len(answer)
        str = ((answer[0 : feedback_start]).replace("\n"," ")).strip()
        if not self.is_number(str):
            print("Warning! One of the correct answer options for the numeric problem is not a number")
        if self.properties.get("answer") == None:
            self.add_property("answer", str)
            if len(answer) - feedback_start > 10:
                self.add_correcthint(answer[feedback_start + 10 :])
                self.corr_feedback_added = True
        else:
            self.add_additional_answer(str)
            if self.corr_feedback_added == False and len(answer) - feedback_start > 10:
                self.add_correcthint(answer[feedback_start + 10 :])
                self.corr_feedback_added = True
        if def_feedback_text != "":
            self.add_solution(def_feedback_text)

    def is_number(self, str):
        try:
            float(str)
        except ValueError:
            return False
        try:
            int(str)
        except ValueError:
            return False
        return True

    def add_label(self, question):
        new_label = xml_elements.label(self.dash + 2, question)
        self.list.insert(0, new_label)

    def add_formulaequationinput(self):
        new_formulaequationinput = formulaequationinput(self.dash + 2)
        i = 0
        while (len(self.list) > i and (self.list[i].name == "label")):
            i += 1
        self.list.insert(i, new_formulaequationinput)

    def add_additional_answer(self, answer):
        new_additional_answer = additional_answer(self.dash + 2, answer)
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label", "formulaequationinput"])):
            i += 1
        self.list.insert(i, new_additional_answer)

    def add_correcthint(self, hint):
        new_correcthint = correcthint(self.dash + 2, hint)
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label", "formulaequationinput", "additional_answer"])):
            i += 1
        self.list.insert(i, new_correcthint)

    def add_responseparam(self):
        new_responseparam = responseparam(self.dash + 2, "1%")
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label", "formulaequationinput", "additional_answer", "correcthint"])):
            i += 1
        self.list.insert(i, new_responseparam)

    def add_solution(self, text):
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label", "formulaequationinput", "additional_answer", "correcthint", "responseparam"])):
            i += 1
        self.list.insert(i, xml_elements.solution(self.dash + 2, text))

    def set_tolerance(self, toler):
        for elem in self.list:
            if elem.name == "responseparam":
                elem.set_tolerance(toler)

    def set_trailing_text(self, text):
        for elem in self.list:
            if elem.name == "formulaequationinput":
                elem.add_trailing_text(text)