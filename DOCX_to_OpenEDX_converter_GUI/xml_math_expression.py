import xml_elements

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

class formularesponse(xml_elements.intermediate_container):
    corr_feedback_added = False

    def __init__(self, dash, full_question):
        super().__init__(dash)
        self.name = "formularesponse"
        def_feedback = full_question.find("\nDefault Feedback:")
        def_feedback_text = ""
        if def_feedback > -1:
            def_feedback_text = full_question[def_feedback + 18: ]
            full_question = full_question[: def_feedback]
            self.add_solution(def_feedback_text)
        next_truth = full_question.find("\n*")
        next = full_question.find("\nA:")
        if next == -1:
            next = len(full_question) + 1
        if next_truth == -1:
            next_truth = len(full_question) + 1
        start_of_answers = min(next_truth, next)
        if start_of_answers == len(full_question) + 1:
            start_of_answers = len(full_question)
        if full_question[next_truth : next_truth + 2] == '\n*' and full_question[next_truth + 3] == ':' and xml_elements.ALPHABET.find(full_question[next_truth + 2]) != -1:
                type_of_answer = False
                start_of_answer = next_truth + 4
                ans_i = xml_elements.ALPHABET.find(full_question[next_truth + 2])
        else:
            raise xml_elements.IncorrectSyntax("Incorrect syntax of the answer entry")
        end_of_answer = full_question.find("\n", start_of_answer + 2)
        if end_of_answer == -1:
            end_of_answer = len(full_question)
        self.add_label(full_question[0 : start_of_answers])
        self.add_answer(full_question[start_of_answer : end_of_answer])
        self.add_formulaequationinput()
        self.add_responseparam()

    def add_label(self, question):
        new_label = xml_elements.label(self.dash + 2, question)
        self.list.insert(0, new_label)

    def add_answer(self, expr):
        standart = []
        standart[: 13] = ["sqrt", "log", "ln", "exp", "abs", "sin", "arcsin", "sinh", "arcsinh", "cos", "arccos", "cosh", "arccosh"]
        standart[13 : 24] = ["tan", "arctan", "tanh", "arctanh", "sec", "arcsec", "sech", "arcsech", "csc", "arccsc", "csch"]
        standart[24 : ] = ["arccsch", "cot", "arccot", "coth", "arccoth", "fact", "factorial"]
        expr_syntax = ["(", ")", "+", "-", "/", "*", "^", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", " "]
        expr = expr.replace("\n"," ").strip()
        i = 0;
        variables = []
        current_leter = ""
        while i < len(expr):
            if (expr[i] in expr_syntax):
                if len(current_leter) != 0:
                    if expr[i] == "(":
                        if not (current_leter in standart):
                            print("Warning! Unknown function in math expression: ", current_leter)
                        current_leter = ""
                    else:
                        if current_leter in standart:
                            print("Warning! The variable name is the same as the standard function: ", current_leter)
                        variables.append(current_leter)
                        current_leter = ""
            else:
                current_leter += expr[i]
            i += 1
        self.add_property("type", "cs")
        self.add_samples(variables)
        self.add_property("answer", expr)

    def add_samples(self, variables):
        res_str = ""
        for var in variables:
            res_str += var + ','
        res_str = res_str[ : -1] + '@'
        for i in range(len(variables)):
            res_str += "0.1,"
        res_str = res_str[ : -1] + ':'
        for i in range(len(variables)):
            res_str += "10,"
        res_str = res_str[ : -1] + '#'
        res_str += "10"
        self.add_property("samples", res_str)

    def add_formulaequationinput(self):
        new_formulaequationinput = formulaequationinput(self.dash + 2)
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label"])):
            i += 1
        self.list.insert(i, new_formulaequationinput)

    def add_responseparam(self):
        new_responseparam = responseparam(self.dash + 2, "1%")
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label", "formulaequationinput"])):
            i += 1
        self.list.insert(i, new_responseparam)

    def add_solution(self, text):
        i = 0
        while (len(self.list) > i and (self.list[i].name in ["label", "formulaequationinput", "responseparam"])):
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

    def set_reg_type(self, type):
        self.properties["type"] = type
        



