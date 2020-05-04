# Python3 Class Example

class Captain():

    def __init__(self, name, surname=""):
        self.name = name
        if surname:
            self.surname = surname

    def get_name(self):
        name_string = self.name
        if hasattr(Captain, "surname"):
            name_string += " " + self.surname
        return name_string
