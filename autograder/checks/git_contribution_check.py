from base_check import BaseCheck
from git_contribution_analyzer import GitContributionAnalyzer

class GitContributionCheck(BaseCheck):
    def __init__(self, context):
        super(GitContributionCheck, self).__init__(context)

    def run(self):
        self.analyzer = GitContributionAnalyzer(self.context.repo_dir)

        not_committed = self.member_names_without_commits()
        if len(not_committed) > 0:
            for name in not_committed:
                self.error("Did not find any commits by '" + name + "'. Everyone must code!")
        else:
            self.info("All team members performed GIT commits. OK")

        if self.analyzer.is_fair():
            self.info("Checked for Git contribution fairness. Seems OK")
        else:
            self.warn("Potentially unfair git contributions detected. Run 'gitinspector' for more details")

    def member_names_without_commits(self):
        contributor_names = self.analyzer.contributor_names()
        return [member['name'] for member in self.context.team
                if member['name'] not in contributor_names]
