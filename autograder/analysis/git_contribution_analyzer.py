import subprocess
import xml.etree.ElementTree as ET

# Class for analyzing the contributions of each collaborator of a git
# repository. This uses gitinspector to do the actual work
class GitContributionAnalyzer:
    def __init__(self, directory):
        self.directory = directory
        self.contributors = []
        self.analyze()

    def analyze(self):
        p = subprocess.Popen(['gitinspector', self.directory, '-F', 'xml'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = p.communicate()

        root = ET.fromstring(out)

        if root.find('changes').find('authors') is None:
            return

        for author in root.find('changes').find('authors').iter('author'):
            self.contributors.append(Contribution(author))

        return self.contributors

    def contributor_names(self):
        return [contributor.name for contributor in self.contributors]

    def contributor_fractions(self):
        return [contributor.fraction for contributor in self.contributors]

    # returns true if the standard error of the contribution fractions is
    # below a certain level
    def is_fair(self):
        return FairnessMetric.is_fair(self.contributor_fractions())

class FairnessMetric:
    @staticmethod
    def is_fair(fractions):
        if len(fractions) == 1:
            return True
        else:
            return FairnessMetric.fairness_metric(fractions) > 0.7

    @staticmethod
    def fairness_metric(fractions):
        return 1.0
        # count = len(fractions)
        # std = numpy.std(fractions)
        # denom = (count - 1) ** 0.5
        # stderr = std / denom

        # mean = numpy.mean(fractions)
        # worst_std = (((1 - mean) ** 2 + mean ** 2 * (count - 1)) / count) ** 0.5
        # worst_stderr = worst_std / denom
        # return (1 - stderr / worst_stderr) ** 2


class Contribution:
    def __init__(self, author_node):
        self.author_node = author_node
        self.name = self.get_attribute('name')
        self.commits = self.get_attribute('commits')
        self.insertions = self.get_attribute('insertions')
        self.percentage = float(self.get_attribute('percentage-of-changes'))
        self.fraction = self.percentage / 100.0

    def get_attribute(self, attribute_name):
        return self.author_node.find(attribute_name).text
