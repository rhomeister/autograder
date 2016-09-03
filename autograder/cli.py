import autograder

import git, os, shutil, sys, argparse
import tempfile
import shutil
from colorama import init, Fore

from team_parser import TeamParser
from git_contribution_analyzer import GitContributionAnalyzer

from checks.team_list_check import TeamListCheck
from checks.git_contribution_check import GitContributionCheck
from checks.required_files_present_check import RequiredFilesPresentCheck

from context import Context

def main():
    parser = argparse.ArgumentParser(description='Autograde programming assignments.')
    parser.add_argument('url', metavar='URL', nargs='?',
                                help='the URL of the git repository',
                                default=os.getcwd())

    args = parser.parse_args()
    url = args.url
    init()
    Runner(url)

class Runner:
    def __init__(self, repo_url):
        self.warning_count = self.error_count = 0
        self.repo_url = repo_url
        self.repo_dir = self.git_clone()
        self.check()
        self.cleanup()

        self.print_output()

        exit_code = 0 if self.error_count == 0 else 1
        exit(exit_code)

    def check(self):
        print "---- PERFORMING CHECKS ----"

        CHECKS = [TeamListCheck,
                  RequiredFilesPresentCheck,
                  GitContributionCheck]

        context = Context(self.repo_dir)

        for check_class in CHECKS:
            check = check_class(context)
            check.run()
            self.error_count += check.error_count
            self.warning_count += check.warning_count


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

    def print_output(self):
        print "---- DONE ----"
        color = Fore.GREEN
        color = color if self.warning_count == 0 else Fore.YELLOW
        color = color if self.error_count == 0 else Fore.RED

        print "{}{} error(s) and {} warning(s) found".format(
                color, self.error_count, self.warning_count)

if __name__ == "__main__":
    main()
