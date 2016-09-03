import autograder
from base_check import BaseCheck
from analysis.team_parser import TeamParser
import os

class TeamListCheck(BaseCheck):
    def __init__(self, context):
        super(TeamListCheck, self).__init__(context)

    def run(self):
        team_file = os.path.join(self.context.repo_dir, 'team.txt')
        if not os.path.isfile(team_file):
            self.error("Required file 'team.txt' with names of team members not found")
            return

        team_parser = TeamParser(team_file)
        team_parser.parse()

        self.context.set_team(team_parser.members)

        team_size = len(team_parser.members)
        if team_size == 0:
            self.error("Found 0 team members in 'team.txt'")
        else:
            self.info('Found ' + str(team_size) + ' team member(s) in team.txt')

        for member in team_parser.members:
            self.info('Found team member: ' + member['name'])

