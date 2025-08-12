import os
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))


class testResult:
    dic = {}

    def testResultMeth(self, TestStep, StepResult, screenshotName, ExceptionText, TestPoints):
        self.dic[TestStep] = StepResult+"^-^"+screenshotName+"^-^"+ExceptionText+"^-^"+TestPoints
        return self.dic