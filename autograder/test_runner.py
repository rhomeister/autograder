import glob, os
import subprocess
from difflib import context_diff

class TestRunner(object):
    def __init__(self, context):
        self.context = context
        self.error_count = 0
        self.test_count = 0
        self.success_count = 0

    def run(self):
        os.getcwd()
        os.chdir(self.context.repo_dir)

        search = os.path.join(self.context.testcasedir, '*.in')
        problem_files = glob.glob(search)

        if len(problem_files) == 0:
            self.warn("No problem files found. Does directory '" +
                    self.context.testcasedir + "' exist?")
            return

        file = self.context.runscript
        if not os.path.isfile(file):
            self.error("Could not find file '{}' to run the program.".format(file))
            return

        for problem_file in problem_files:
            self.test_count += 1
            output = self.get_output(problem_file)
            expected_output = self.get_expected_output(problem_file)
            if self.compare(problem_file, output, expected_output):
                self.success_count += 1
            else:
                self.error_count += 1

    def compare(self, problem_file, output, expected_output):
        expected_output = self.strip_whitespace(expected_output)
        diff_iterator = context_diff(output, expected_output,
            fromfile='program output', tofile='expected')
        diff = ""

        for char in diff_iterator:
            diff += char

        if len(diff) == 0:
            self.info("Testing '" + problem_file + "'. Result: output CORRECT")
            return True
        else:
            self.error("Testing '" + problem_file + "'. Result: output DIFFERENT")
            self.error("    Expected:")
            for line in expected_output.split('\n'):
                self.error("    " + line)
            self.error("    Actual:")
            for line in output.split('\n'):
                self.error("    " + line)
            return False

    def info(self, message):
        self.context.logger.info(message)

    def warn(self, message):
        self.context.logger.warn(message)

    def error(self, message):
        self.context.logger.error(message)


    def get_expected_output(self, problem_file):
        expected_output_file = problem_file[:-2] + 'out'
        with open(expected_output_file, 'r') as file:
            return file.read()

    def get_output(self, problem_file):
        runscript = os.path.join(self.context.repo_dir, self.context.runscript)
        out = ''
        err = ''
        try:
            with open(problem_file, 'r') as input:
                p = subprocess.Popen(runscript,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = input)
                out, err = p.communicate()
                p.wait()
                if len(err) > 0:
                    self.warn('Stderr is outputting text:')
                    for line in err.split('\n'):
                        self.warn(line)
        except Exception as e:
            self.error('Caught unexpected error: ' + str(e))

        return self.strip_whitespace(out)

    def strip_whitespace(self, string):
        # remove trailing whitespace
        return "\n".join([line.rstrip() for line in string.split("\n") if
            len(line) > 0])
