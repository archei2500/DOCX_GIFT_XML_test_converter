#Abstractions:
class single_tag:
    'Abstract single-tag element'
    name = ""
    properties = {}
    dash = 0

    def __init__(self, dash):
        self.name = "abstract"
        self.properties = {}
        self.dash = dash

    def add_to_text(self, text):
        self.add_opening(text)

    def add_opening(self, text):
        res_str = "<" + self.name
        for key in self.properties:
            res_str += " " + key + "=\"" + (self.properties).get(key) + "\""
        text.append(' ' * self.dash + res_str + "/>")

    def add_property(self, property, value):
        self.properties[property] = value

class abstract_container(single_tag):
    'Abstract container'

    def add_to_text(self, text):
        self.add_opening(text)
        self.add_ending(text)

    def add_ending(self, text):
        res_str = "</" + self.name + ">"
        text.append(' ' * self.dash + res_str)

    def add_opening(self, text):
        res_str = "<" + self.name
        for key in self.properties:
            res_str += " " + key + "=\"" + (self.properties).get(key) + "\""
        text.append(' ' * self.dash + res_str + ">")

    def add_property(self, property, value):
        self.properties[property] = value

class string_only_container(abstract_container):
    'Container with string'
    name = ""
    properties = {}
    dash = 0
    str = ""

    def __init__(self, dash, str):
        self.str = str
        super().__init__(dash)

    def add_opening(self, text):
        res_str = "<" + self.name
        for key in self.properties:
            res_str += " " + key + "=\"" + (self.properties).get(key) + "\""
        text.append(' ' * self.dash + res_str + ">" + (self.str).replace('\n', ''))


class text_container(abstract_container):
    'Container with text'
    name = ""
    properties = {}
    dash = 0
    text = ""

    def __init__(self, dash, str):
        self.str = str
        super().__init__(dash)

    def add_opening(self, text):
        # res_str = "<" + self.name
        res_str = ""
        for key in self.properties:
            res_str += " " + key + "=\"" + (self.properties).get(key) + "\""
        text.append(' ' * self.dash + res_str + self.str.replace('\n', '\n' + ' ' * self.dash))
        # text.append(' ' * self.dash + res_str + ">" + self.str)

    def add_to_text(self, text):
        self.add_opening(text)


class intermediate_container(abstract_container):
    'Container with other containers'
    name = ""
    properties = {}
    dash = 0
    list = list()

    def __init__(self, dash):
        self.list = list()
        super().__init__(dash)

    def add_to_text(self, text):
        self.add_opening(text)
        for elem in self.list:
            elem.add_to_text(text)
        self.add_ending(text)

class fully_functional_container(string_only_container, intermediate_container):
    'Container with string and other containers'
    name = ""
    properties = {}
    dash = 0
    str = ""
    list = list()

    def __init__(self, dash, str):
        self.list = list()
        super().__init__(dash, str)

    def add_to_text(self, text):
        self.add_opening(text)
        for elem in self.list:
            elem.add_to_text(text)
        self.add_ending(text)

#Implementations

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class IncorrectSyntax(Exception):
    pass

class problem(intermediate_container):

    def __init__(self, dash=0):
        super().__init__(dash)
        self.name = "problem"

    def add_content(self, content):
        self.list.append(content)

class label(string_only_container):

    def __init__(self, dash, str):
        super().__init__(dash, (str.replace("\n"," ")).strip())
        self.name = "label"

class p(string_only_container):
    def __init__(self, dash, str):
        super().__init__(dash, (str.replace("\n"," ")).strip())
        self.name = "p"

class div(intermediate_container):

    def __init__(self, dash=0, text=""):
        super().__init__(dash)
        self.name = "div"
        self.add_p(text)
        self.add_class("detailed-solution")

    def add_class(self, value):
        self.add_property("class", value)

    def add_p(self, text):
        self.list.append(p(self.dash + 2, text))

class solution(intermediate_container):

    def __init__(self, dash=0, text=""):
        super().__init__(dash)
        self.name = "solution"
        self.add_div(text)

    def add_div(self, text):
        self.list.append(div(self.dash + 2, text))