class Context(object):
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.team = []

    def set_team(self, team):
        self.team = team
