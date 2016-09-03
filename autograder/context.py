class Context(object):
    def __init__(self, repo_dir, logger):
        self.repo_dir = repo_dir
        self.logger = logger
        self.team = []

    def set_team(self, team):
        self.team = team
