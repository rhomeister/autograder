class Context(object):
    def __init__(self, logger, testcasedir, runscript):
        self.warning_count = self.error_count = 0
        self.logger = logger
        self.team = []
        self.testcasedir = testcasedir
        self.runscript = runscript

    def set_team(self, team):
        self.team = team
