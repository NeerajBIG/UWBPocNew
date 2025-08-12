import os
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import inspect
import time
from pageObjects.AllElementLocators import ElementLocators
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from datetime import datetime
from testCases.testResultData import testResult


class Test_HealthCheck:
    basePath = ReadConfig.basePath()
    path1 = basePath
    text = path1.split("/")
    for t in text:
        if t == ".jenkins":
            print("Running on Jenkins")
            path = os.path.dirname(basePath)
            print("path is " + path)
            basePath = path
            JenkinsJobName = os.getenv("JOB_NAME")
            basePath = basePath + "/" + JenkinsJobName
        else:
            pass

    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"

    sheetName_Report = "Report"
    sheetName_Config = "Config"
    sheetName_Data = "TestUserData"
    sheetName_Scenarios = "Scenarios"
    sheetName_WoData = "WorkOrderData"
    sheetName_Locators = "Locators"

    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
    ApplicationName = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "ProjectName")

    testStep = "Launching Application"
    error = ""

    def test_HealthCheck(self, setup):
        scenario_ID = "SC_001"
        scenarioDataList = XLUtils.readDataScenarios(self.dataSheetPath, self.sheetName_Scenarios, scenario_ID)
        StartTime = datetime.now()
        now = datetime.now()
        current_time = now.strftime("h%Hm%Ms%S")
        ScenarioName = scenarioDataList[1]
        ScenarioTitle = scenarioDataList[2]
        Enable = scenarioDataList[3]
        locator = "None"
        # ---------Initiating WebDriver and Launching Application
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = ElementLocators(self.driver)
        self.lp1 = testResult()

        # ---------Deleting all screenshots
        self.lp.deleteScreenshot()
        self.lp.deleteReports()

        if Enable is True:
            try:
                # ---------Entering Username
                self.testStep = "To ensure proper handling and acceptance of input within the username field."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                self.user = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                         "username_" + self.Env)
                self.password = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                             "password_" + self.Env)
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                             "textbox_username_id")
                    self.lp.inputData(locator, self.user)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception


                # ---------Entering Password
                self.testStep = "To ensure proper handling and acceptance of input within the password field."
                self.testPoints = """
                This is step 11
                This is step 22
                This is step 33
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "textbox_password_id")
                    self.lp.inputData(locator, self.password)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception


                # ---------Clicking Login button
                self.testStep = "Initiating the login sequence via the Login button."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_login_xpath")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_login_xpath")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception


                time.sleep(1)
                # ---------Clicking Home link text
                self.testStep = "Initiating navigation via the 'Home' text link."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_home")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_home")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception


                time.sleep(1)
                # ---------Clicking Cases link text
                self.testStep = "Interacting with the Cases link text"
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Cases")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_Cases")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : "+str(locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception


                time.sleep(1)
                # ---------Clicking Users link text
                self.testStep = "Selecting the Users link text"
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Users")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_Users")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking Monitoring link text
                self.testStep = "Clicking Monitoring hyperlink text"
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Monitoring")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_Monitoring")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking Notes link text
                self.testStep = "Clicking Notes link text"
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Notes")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_Notes")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                #----------Inside Case Numbers---------
                time.sleep(1)
                # ---------Clicking Home link text
                self.testStep = "Navigating back to Home"
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_home")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_home")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ----------Clicking Case Number (Unassigned)
                time.sleep(1)
                # ---------Clicking Case Number  link text
                self.testStep = "Selecting the 'Case Number' navigation link."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_CaseNumberUnassigned")
                    Data = scenarioDataList[4] + "']"
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_CaseNumberUnassigned")
                    self.lp.performClick(locator + Data, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking Summary tab
                self.testStep = "Clicking Summary tab to verify its content."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Summary")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Summary")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking Documents tab
                self.testStep = "Clicking Documents tab to verify its content."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Documents")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Documents")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking Communication tab
                self.testStep = "Clicking Communication tab to verify its content."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Communication")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Communication")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking Notes tab
                self.testStep = "Clicking Notes tab to verify its content."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Notes")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Notes")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                time.sleep(1)
                # ---------Clicking SmartIngestionAudit tab
                self.testStep = "Clicking SmartIngestionAudit tab to verify its content."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_SmartIngestionAudit")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_SmartIngestionAudit")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                #----------Sections inside Summary Tab
                time.sleep(1)
                # ---------Clicking Summary tab
                self.testStep = "Navigating back to Summary tab."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Summary")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Summary")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ---------Clicking Program Filing-Preparation Button
                self.testStep = "Interacting with the 'Program Filing-Preparation' control button."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_ProgramFilingPreparation")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_ProgramFilingPreparation")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ---------Clicking Upfront Analysis Button
                self.testStep = "Interacting with the 'Upfront Analysis' button."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_UpfrontAnalysis")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_UpfrontAnalysis")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ---------Clicking In-depth Analysis Button
                self.testStep = "Interacting with the 'In-depth Analysis' button."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_In-depthAnalysis")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_In-depthAnalysis")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ---------Clicking Negotiation & Quotation Button
                self.testStep = "Interacting with the 'Negotiation & Quotation' button."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Negotiation&Quotation")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Negotiation&Quotation")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ---------Clicking Authorization Refusal Button
                self.testStep = "Interacting with the 'Authorization Refusal' button."
                self.testPoints = """
                This is step 1.
                This is step 2.
                This is step 3.
                """
                lines = self.testPoints

                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_AuthorizationRefusal")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_AuthorizationRefusal")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException", lines)
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage, lines)
                    #raise Exception

                # ---------Ending the test scenario
                EndTime = datetime.now()
                StepLog = "######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
                    1] + " completed successfully and ended at " + str(EndTime) + " ########"
                print(StepLog)
                time.sleep(2)
                self.lp.createPDaF(ScenarioName+" - "+scenario_ID, ScenarioTitle)
                self.driver.close()

            except:
                print("Inside Exception-----2")
                self.lp.createPDaF(ScenarioName+" - "+scenario_ID, ScenarioTitle)
                self.driver.close()
                assert False

        else:

            print("Skipping Scenario Execution for: " + scenarioDataList[0])
