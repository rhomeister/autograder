import autograder

import git, os, shutil, sys, argparse
import tempfile
import shutil

from console_logger import ConsoleLogger
from checks.team_list_check import TeamListCheck
from checks.git_contribution_check import GitContributionCheck
from checks.required_files_present_check import RequiredFilesPresentCheck
from test_runner import TestRunner

from context import Context

import traceback

def main():
    parser = argparse.ArgumentParser(description='Autograde programming assignments.')
    parser.add_argument('url', metavar='URL', nargs='?',
                                help='the URL of the git repository',
                                default=os.getcwd())
    parser.add_argument('--testcasedir', help='the directory with testcases',
                                default='testcases')
    parser.add_argument('--runscript', help='the script run the program',
                                default='run')

    args = parser.parse_args()
    url = args.url
    testcasedir = args.testcasedir
    runscript = args.runscript
    Runner(url, testcasedir, runscript)

class Runner:
    def __init__(self, repo_url, testcasedir, runscript):
        try:
            self.repo_url = repo_url
            logger = ConsoleLogger()
            self.context = Context(logger, testcasedir, runscript)
            self.context.repo_dir = self.git_clone()
            self.check()
            self.test()
        except Exception as e:
            print traceback.format_exc()
            raise
        finally:
            self.cleanup()
            self.print_output()

            exit_code = 0 if self.context.error_count == 0 else 1
            exit(exit_code)

    # run test cases
    def test(self):
        print "---- TESTING PROGRAM ----"
        runner = TestRunner(self.context)
        runner.run()
        self.context.tests_failed = runner.error_count
        self.context.tests_run = runner.test_count
        self.context.tests_passed = runner.success_count

    def check(self):
        print "---- CHECKING SUBMISSION FILES ----"
        CHECKS = [TeamListCheck,
                  RequiredFilesPresentCheck,
                  GitContributionCheck]

        for check_class in CHECKS:
            check = check_class(self.context)
            check.run()
            self.context.error_count += check.error_count
            self.context.warning_count += check.warning_count

    def git_clone(self):
        repo_dir = tempfile.mkdtemp()

        print "---- CLONING ----"
        repo = git.Repo.init(repo_dir)
        origin = repo.create_remote('origin', self.repo_url)
        origin.fetch()
        origin.pull('master')
        self.context.logger.info('Cloned git repo into ' + repo_dir)
        return repo_dir

    def cleanup(self):
        print "---- CLEANING UP ----"
        shutil.rmtree(self.context.repo_dir)
        self.context.logger.info('Deleting temporary directory ' + self.context.repo_dir)

    def print_output(self):
        print "---- DONE ----"
        log = self.context.logger.info
        log = log if self.context.warning_count == 0 else self.context.logger.warn
        log = log if self.context.error_count == 0 else self.context.logger.error

        log("{} error(s) and {} warning(s) found while checking submission files".format(
                self.context.error_count, self.context.warning_count))

        log = self.context.logger.info
        log = log if self.context.tests_failed == 0 else self.context.logger.error
        log = log if self.context.tests_run > 0 else self.context.logger.warn
        log("program passed {}/{} test cases ({} failed)".format(
                self.context.tests_passed,
                self.context.tests_run,
                self.context.tests_failed))

if __name__ == "__main__":
    main()
