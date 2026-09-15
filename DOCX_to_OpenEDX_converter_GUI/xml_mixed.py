import xml_elements


class mixed(xml_elements.intermediate_container):
    def __init__(self, dash, full_question):
        super().__init__(dash)
        self.add_label(full_question)

    def add_label(self, question):
        self.name = "mixed"
        question = question[question.find(">") + 1: question.find("</problem>")].strip(' \n')
        new_text = xml_elements.text_container(self.dash + 2, question)
        self.list.append(new_text)
