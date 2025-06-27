import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import time
from datetime import datetime
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from pageObjects.AllElementLocators import ElementLocators
from testCases.testResultData import testResult
import imaplib
import email


class Test_ReadEmail:
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

    def test_ReadEmail(self, setup):

        scenario_ID = "SC_002"
        scenarioDataList = XLUtils.readDataScenarios(self.dataSheetPath, self.sheetName_Scenarios, scenario_ID)
        StartTime = datetime.now()
        now = datetime.now()
        current_time = now.strftime("h%Hm%Ms%S")
        ScenarioName = scenarioDataList[1]
        ScenarioTitle = scenarioDataList[2]
        Enable = scenarioDataList[3]
        locator = "None"
        AssignReassignFlag = 0

        # ---------Initiating WebDriver and Launching Application
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = ElementLocators(self.driver)
        self.lp1 = testResult()

        # ---------Deleting all screenshots
        self.lp.deleteScreenshot()

        if Enable is True:
            try:
                self.user = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                         "username_" + self.Env)
                self.password = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                             "password_" + self.Env)
                # ---------Entering Username
                self.testStep = "To verify data input to username field"
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
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                # ---------Entering Password
                self.testStep = "To verify data input to password field"
                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "textbox_password_id")
                    self.lp.inputData(locator, self.password)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                # ---------Clicking Login button
                self.testStep = "Clicking Login button"
                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_login_xpath")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath, self.sheetName_Locators,
                                                                                   "button_login_xpath")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                # ----------Inside Case Numbers---------
                time.sleep(1)
                # ---------Clicking Home link text
                self.testStep = "Clicking Home link text"
                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_home")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "LinkText_home")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                # ----------Clicking Case Number (Unassigned)
                time.sleep(1)
                # ---------Clicking Case Number  link text
                self.testStep = "Clicking Case Number  link text"
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
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                time.sleep(1)
                # ---------Clicking Assign Underwriter button
                self.testStep = "Clicking Assign Underwriter button"
                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_AssignUnderwrite")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_AssignUnderwrite")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                    time.sleep(1)
                    # ---------Clicking Reassign Underwriter button
                    self.testStep = "Clicking Reassign Underwriter button"
                    screenshotName = self.testStep.replace(" ", "")
                    try:
                        locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                               "button_ReassignUnderwrite")
                        locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                       self.sheetName_Locators,
                                                                                       "button_ReassignUnderwrite")
                        self.lp.performClick(locator, locatorConfirmation)
                        self.lp.takeScreenshot(screenshotName)
                        self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                        AssignReassignFlag = 1
                    except:
                        self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                            locator)
                        EndTime = datetime.now()
                        self.errorMessage = "Test case failed due to " + self.error
                        XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                        self.lp.takeScreenshot(screenshotName)
                        self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                        # raise Exception

                time.sleep(1)
                # ---------Clicking Underwriter Team dropdown
                self.testStep = "Clicking Underwriter Team dropdown"
                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "dropdown_SelectUnderwriterTeam")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "dropdown_SelectUnderwriterTeam")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.dropdownByOne(setup)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                userUnderwriter = "None"
                if AssignReassignFlag == 0:
                    time.sleep(1)
                    # ---------Entering Underwriter in textbox
                    self.testStep = "Entering Underwriter in textbox"
                    screenshotName = self.testStep.replace(" ", "")
                    userUnderwriter = ReadConfig.getUnderwriterEmail1()
                    try:
                        locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                               "textbox_Underwriter")
                        self.lp.inputData(locator, userUnderwriter)
                        self.lp.dropdownByOne(setup)
                        self.lp.takeScreenshot(screenshotName)
                        self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                    except:
                        self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                            locator)
                        EndTime = datetime.now()
                        self.errorMessage = "Test case failed due to " + self.error
                        XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                        self.lp.takeScreenshot(screenshotName)
                        self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                        # raise Exception

                time.sleep(1)
                # ---------Clicking Assign button
                self.testStep = "Clicking Assign button"
                screenshotName = self.testStep.replace(" ", "")
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Assign")
                    locatorConfirmation = XLUtils.readDataTestUserDataConfirmation(self.dataSheetPath,
                                                                                   self.sheetName_Locators,
                                                                                   "button_Assign")
                    self.lp.performClick(locator, locatorConfirmation)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                except:
                    self.error = "No web element found for test step - : [ " + self.testStep + " ].  Element locator used - : " + str(
                        locator)
                    EndTime = datetime.now()
                    self.errorMessage = "Test case failed due to " + self.error
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)
                    self.lp.takeScreenshot(screenshotName)
                    self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                    # raise Exception

                time.sleep(5)
                # ---------Reading assignment email sent to Underwriter
                self.testStep = "Reading assignment email sent to Underwriter"
                imap_url = 'imap.gmail.com'
                password = ReadConfig.getUnderwriterPassword1()

                try:
                    my_mail = imaplib.IMAP4_SSL(imap_url)
                    my_mail.login(userUnderwriter, password)
                    my_mail.select('inbox')  # Connect to the inbox.

                    key = 'SUBJECT "Program Assignment"'
                    _, data = my_mail.search(None, key)

                    mail_id_list = data[0].split()
                    msgs = []
                    for num in mail_id_list:
                        typ, data = my_mail.fetch(num, '(RFC822)')
                        msgs.append(data)
                        my_mail.store(num, "+FLAGS", "\\Deleted")

                    if len(msgs) != 0:
                        print("Email found: " + str(len(msgs)))
                        for msg in msgs[::-1]:
                            for response_part in msg:
                                if type(response_part) is tuple:
                                    my_msg = email.message_from_bytes(response_part[1])
                                    print("---------------------------------------------")
                                    print("subject:", my_msg['subject'])
                                    print("from:", my_msg['from'])
                                    print("body:")
                                    for part in my_msg.walk():
                                        print(part.get_content_type())
                                        if part.get_content_type() == 'text/html':
                                            print(part.get_payload())

                        screenshotName = "None"
                        self.lp1.testResultMeth(self.testStep, "Passed", screenshotName, "NoException")
                    else:
                        self.error = "No email found for test step - : [ " + self.testStep + " ]"
                        EndTime = datetime.now()
                        self.errorMessage = "Test case failed due to " + self.error
                        XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                scenarioDataList[1], self.testStep, self.errorMessage, StartTime,
                                                EndTime)
                        screenshotName = "None"
                        self.lp1.testResultMeth(self.testStep, "Failed", screenshotName, self.errorMessage)
                except Exception as e:

                    print("Connection failed")
                    raise

                # ---------Ending the test scenario
                EndTime = datetime.now()
                StepLog = "######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
                    1] + " completed successfully and ended at " + str(EndTime) + " ########"
                print(StepLog)
                time.sleep(2)
                self.lp.createPDaF(ScenarioName + " - " + scenario_ID, ScenarioTitle)
                self.driver.close()
            except:
                print("Inside Exception-----2")
                self.lp.createPDaF(ScenarioName+" - "+scenario_ID, ScenarioTitle)
                self.driver.close()
                assert False

        else:

            print("Skipping Scenario Execution for: " + scenarioDataList[0])