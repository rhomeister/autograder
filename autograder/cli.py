import autograder

import git, os, shutil, sys, argparse
import tempfile
import shutil
from IPython import embed

from team_parser import TeamParser
from git_contribution_analyzer import GitContributionAnalyzer

def main():
    parser = argparse.ArgumentParser(description='Autograde programming assignments.')
    parser.add_argument('url', metavar='URL', nargs='?',
                                help='the URL of the git repository',
                                default=os.getcwd())

    args = parser.parse_args()
    url = args.url
    Runner(url)


class Runner:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.repo_dir = self.git_clone()
        self.check()
        self.cleanup()
        print "---- DONE ----"

    def check(self):
        print "---- PERFORMING CHECKS ----"

        required_files = ['team.txt', 'report.pdf']

        for required_file in required_files:
            if os.path.isfile(os.path.join(self.repo_dir, required_file)):
                print "     Required file '" + required_file + "' found."
            else:
                print "     ERROR: Required file '" + required_file + "' not found. Submission is incomplete. Exiting"
                exit()

        team_parser = TeamParser(os.path.join(self.repo_dir, 'team.txt'))
        team_parser.parse()

        analyzer = GitContributionAnalyzer(self.repo_dir)

        contributor_names = analyzer.contributor_names()

        not_committed = [member['name'] for member in team_parser.members if member['name'] not in contributor_names]
        if len(not_committed) > 0:
            for name in not_committed:
                print "     ERROR: Did not find any commits by '" + name + "'. Everyone must code!"
            exit()

        if analyzer.is_fair():
            print "     Checked for Git contribution fairness. Seems OK"
        else:
            print "     WARNING: potentially unfair git contributions detected. Run 'gitinspector' for more details"


    def git_clone(self):
        repo_dir = tempfile.mkdtemp()

        print "---- CLONING ----"
        repo = git.Repo.init(repo_dir)
        origin = repo.create_remote('origin', self.repo_url)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)
        return repo_dir

    def cleanup(self):
        shutil.rmtree(self.repo_dir)

if __name__ == "__main__":
    main()
