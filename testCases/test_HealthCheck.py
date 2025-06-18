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
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"
    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
    sheetName_Data = "TestUserData"
    sheetName_Report = "Report"
    sheetName_Scenarios = "Scenarios"
    sheetName_WoData = "WorkOrderData"
    sheetName_Locators = "Locators"

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

        if Enable is True:
            try:
                # ==================================== Common Steps 1 ====================================

                # ---------Initiating WebDriver and Launching Application
                self.driver = setup
                self.driver.get(self.baseURL)
                self.lp = ElementLocators(self.driver)
                self.user = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                         "username_" + self.Env)
                self.password = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                             "password_" + self.Env)

                self.lp1 = testResult()

                # ---------Entering Username
                self.testStep = "To verify data input to username field"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                             "textbox_username_id")
                    self.lp.inputData(locator, self.user)
                    self.lp1.testResultMeth(self.testStep, "Passed")
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    self.lp1.testResultMeth(self.testStep, "Failed")
                    raise Exception

                # ---------Entering Password
                self.testStep = "To verify data input to password field"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "textbox_password_id")
                    self.lp.inputData(locator, self.password)
                    self.lp1.testResultMeth(self.testStep, "Failed")
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    self.lp1.testResultMeth( self.testStep, "Failed")
                    raise Exception

                self.driver.close()
                # ---------Clicking Login button
                self.testStep = "Clicking Login button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_login_xpath")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Home link text
                self.testStep = "Clicking Home link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_home")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Cases link text
                self.testStep = "Clicking Cases link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Cases")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Users link text
                self.testStep = "Clicking Users link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Users")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Monitoring link text
                self.testStep = "Clicking Monitoring link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Monitoring")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Notes link text
                self.testStep = "Clicking Notes link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_Notes")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                #----------Inside Case Numbers---------
                time.sleep(1)
                # ---------Clicking Home link text
                self.testStep = "Clicking Home link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_home")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ----------Clicking Case Number (Unassigned)
                time.sleep(1)
                # ---------Clicking Case Number  link text
                self.testStep = "Clicking Case Number  link text"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_CaseNumberUnassigned")
                    Data = scenarioDataList[3] + "']"
                    self.lp.performClick(locator + Data)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Summary tab
                self.testStep = "Clicking Summary tab"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Summary")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Documents tab
                self.testStep = "Clicking Documents tab"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Documents")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Communication tab
                self.testStep = "Clicking Communication tab"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Communication")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking Notes tab
                self.testStep = "Clicking Notes tab"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Notes")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                time.sleep(1)
                # ---------Clicking SmartIngestionAudit tab
                self.testStep = "Clicking SmartIngestionAudit tab"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_SmartIngestionAudit")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                #----------Sections inside Summary Tab
                time.sleep(1)
                # ---------Clicking Summary tab
                self.testStep = "Clicking Summary tab"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Summary")
                    print(locator)
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Program Filing / Preparation Button
                self.testStep = "Clicking Program Filing / Preparation Button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_ProgramFilingPreparation")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Upfront Analysis Button
                self.testStep = "Clicking Upfront Analysis Button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_UpfrontAnalysis")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking In-depth Analysis Button
                self.testStep = "Clicking In-depth Analysis Button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_In-depthAnalysis")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Negotiation & Quotation Button
                self.testStep = "Clicking Negotiation & Quotation Button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_Negotiation&Quotation")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Authorization Refusal Button
                self.testStep = "Clicking Authorization Refusal Button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_AuthorizationRefusal")
                    self.lp.performClick(locator)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Ending the test scenario
                EndTime = datetime.now()
                StepLog = "######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
                    1] + " completed successfully and ended at " + str(EndTime) + " ########"
                print(StepLog)
                time.sleep(5)


                self.lp.createPDaF(ScenarioName+" - "+scenario_ID, ScenarioTitle)
            except Exception as e:
                print("Inside Exception-----1")
                screenshotFile = type(self).__name__ + "[" + inspect.stack()[0][3] + "-" + current_time + "].png"
                path = self.basePath
                text = path.split("/")
                for t in text:
                    if t == ".jenkins":
                        print("Running on Jenkins")
                        path = os.path.dirname(self.basePath)
                        print("path is " + path)
                        JenkinsJobName = os.getenv("JOB_NAME")
                        path = path + "/" + JenkinsJobName
                    else:
                        pass
                #self.driver.save_screenshot(path + "/Screenshots/" + screenshotFile)
                self.errorMessage = "######## Test case failed due to " + self.error + ". Screenshot file: " + screenshotFile + " is present in screenshots folder attached"
                EndTime = datetime.now()
                XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                        scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)

                print("Inside Exception-----2")
                self.lp.createPDaF(ScenarioName+" - "+scenario_ID, ScenarioTitle)
                self.driver.close()
                assert False

        else:

            print("Skipping Scenario Execution for: " + scenarioDataList[0])
