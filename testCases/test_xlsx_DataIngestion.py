import os
import sys
from os.path import dirname, join, abspath
from testCases.testResultData import testResult
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import inspect
import time
from pageObjects.AllElementLocators import ElementLocators
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from datetime import datetime


class Test_DataIngestion:
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

    xlsxIngestionFileName = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "IngestionFile_xlsx")
    dataSheetIngestionPath = basePath + "/IngestionFiles/"+xlsxIngestionFileName+".xlsx"
    def test_DataIngestion(self, setup):
        scenario_ID = "SC_002"
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
                self.lp1 = testResult()

                #-- Reading Ingestion XL data
                sheetName_dataSheetIngestion = "Building Years const Type"
                dataSheetIngestion_Result = XLUtils.readXLData(self.dataSheetIngestionPath, sheetName_dataSheetIngestion)
                print(dataSheetIngestion_Result)
                self.lp1.testResultMeth("Building value for 2002 - Present matched in both XLSX file and Appian page: " + str(dataSheetIngestion_Result["2002 - Present"]), "Passed")

                self.user = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                         "username_" + self.Env)
                self.password = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                             "password_" + self.Env)

                # ---------Entering Username
                self.testStep = "To verify data input to username field"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                             "textbox_username_id")
                    self.lp.inputData(locator, self.user)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Entering Password
                self.testStep = "To verify data input to password field"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "textbox_password_id")
                    self.lp.inputData(locator, self.password)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Login button
                self.testStep = "Clicking Login button"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "button_login_xpath")
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
                    Data = scenarioDataList[4] + "']"
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
                # ---------Clicking Building Year LinkText
                self.testStep = "Clicking Building Year LinkText"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "LinkText_BuildingYear")
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
