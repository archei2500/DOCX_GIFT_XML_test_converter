import xml_elements

class problem_in_library(xml_elements.single_tag):
    #name = ""
    #properties = {}
    #dash = 0

    def __init__(self, dash=0):
        super().__init__(dash)
        self.name = "problem"

    def add_url(self, url_value):
         self.add_property("url_name", url_value)

class library(xml_elements.intermediate_container):
    #name = ""
    #properties = {}
    #dash = 0
    #list = list()

    def __init__(self, dash=0):
        super().__init__(dash)
        self.name = "library"

    def add_opening(self, text):
        res_str = "<" + self.name
        for key in self.properties:
            res_str += " " + key + "=\"" + (self.properties).get(key) + "\""
        text.append(' ' * self.dash + res_str + ">")

    def add_problem(self, problem_url):
        new_problem = problem_in_library(self.dash + 2)
        new_problem.add_url(problem_url)
        self.list.append(new_problem)

    def add_display_name(self, value):
        self.add_property("display_name", value)

    def add_org(self, value):
        self.add_property("org", value)

    def add_library(self, value):
        self.add_property("library", value)

    def add_inner_attributes(self):
        url = "http://code.edx.org/xblock/option"
        names = ["advanced_modules","matlab_api_key","xqa_key","format","giturl","source_file","default_tab","name","chrome"]
        inner_attrebute = xml_elements.string_only_container(self.dash + 2, "[]")
        inner_attrebute.name = "ns0:" + names[0]
        inner_attrebute.add_property("xmlns:ns0", url)
        self.list.append(inner_attrebute)
        for i in range(1, 9):
            inner_attrebute = xml_elements.single_tag(self.dash + 2)
            inner_attrebute.name = "ns" + str(i) + ":" + names[i]
            inner_attrebute.add_property("xmlns:ns" + str(i), url)
            inner_attrebute.add_property("none", "true")
            self.list.append(inner_attrebute)




