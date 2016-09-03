from base_check import BaseCheck
import os

class RequiredFilesPresentCheck(BaseCheck):
    def __init__(self, context):
        super(RequiredFilesPresentCheck, self).__init__(context)

    def run(self):
        required_files = ['report.pdf']
        for required_file in required_files:
            self.check_presence(required_file)

    def check_presence(self, required_file):
        file = os.path.join(self.context.repo_dir, required_file)
        if os.path.isfile(file):
            self.info("Required file '{}' found.".format(required_file))
        else:
            self.error("Required file '{}' not found.".format(required_file))
