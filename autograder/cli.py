import autograder

import git, os, shutil, sys, argparse
import tempfile
import shutil

from console_logger import ConsoleLogger
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
    Runner(url)

class Runner:
    def __init__(self, repo_url):
        self.warning_count = self.error_count = 0
        self.repo_url = repo_url
        self.logger = ConsoleLogger()
        self.repo_dir = self.git_clone()
        self.check()
        self.cleanup()

        self.print_output()

        exit_code = 0 if self.error_count == 0 else 1
        exit(exit_code)

    def check(self):
        print "---- PERFORMING CHECKS ----"
        context = Context(self.repo_dir, self.logger)

        CHECKS = [TeamListCheck,
                  RequiredFilesPresentCheck,
                  GitContributionCheck]

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
        log = self.logger.info
        log = log if self.warning_count == 0 else self.logger.warn
        log = log if self.error_count == 0 else self.logger.error

        log("{} error(s) and {} warning(s) found".format(
                self.error_count, self.warning_count))

if __name__ == "__main__":
    main()
