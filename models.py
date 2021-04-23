class Profile(dict):
    def __init__(self, name, job_title, location, company, contacts):
        self.name = name
        self.job_title = job_title
        self.location = location
        self.company = company
        self.contacts = contacts
        dict.__init__(self, name = name, job_title = job_title,
            location = location, company = company, contacts = contacts)

class Contact(dict):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        dict.__init__(self, name = name, value = value)