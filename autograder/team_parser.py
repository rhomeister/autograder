class TeamParser:
    def __init__(self, file):
        self.file = file

    def parse(self):
        lines = []
        self.members = []

        with open(self.file) as f:
            lines = f.readlines()

        for line in lines:
            name = line.split(',')[0].strip()
            self.members.append({'name': name})

        return self.members

