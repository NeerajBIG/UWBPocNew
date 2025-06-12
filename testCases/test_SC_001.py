import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import inspect
import time
from pageObjects.AllElementLocators import ElementLocators
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from datetime import datetime
from utilities.supportFxn import Support_Functions


class Test_CreateWorkOrder:
    #logger = LogGen.loggen()
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"
    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
    sheetName_Data = "TestUserData"
    sheetName_Report = "Report"
    sheetName_Scenarios = "Scenarios"
    sheetName_WoData = "WorkOrderData"
    testStep = "Launching Application"
    error = ""

    def test_CreateWorkOrder_Thermostat_Count(self, setup):
        scenario_ID = "SC_001"
        scenarioDataList = XLUtils.readDataScenarios(self.dataSheetPath, self.sheetName_Scenarios, scenario_ID)
        StartTime = datetime.now()
        # self.logger.info("######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
        #     1] + " started at " + str(StartTime) + " ########")
        Enable = scenarioDataList[2]
        WorkOrderDetailsFound = {}
        WOList = []
        test = XLUtils.readWorkOrderData(self.dataSheetPath, self.sheetName_WoData, "Env_ToRun")
        count = int(scenarioDataList[3])
        print(f"xCount: {count}")
        if Enable is True:
            try:
                # ==================================== Common Steps 1 ====================================
                # ---------Initiating WebDriver and Launching Application
                self.driver = setup
                self.driver.get(self.baseURL)
                StepLog = "Test Step : " + self.testStep
                # #self.logger.info(StepLog)
                self.lp = ElementLocators(self.driver)
                self.user = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                         "username_" + self.Env)
                self.password = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                             "password_" + self.Env)
                # ---------Entering Username
                self.testStep = "Entering Username"
                user = self.user
                try:
                    self.lp.setUserName(self.user)
                    StepLog = "######## Username entered : " + user
                    # #self.logger.info(StepLog)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Entering Password
                self.testStep = "Entering Password"
                password = self.password
                try:
                    self.lp.setPassword(password)
                    StepLog = "######## Password entered : " + "##########"
                    # #self.logger.info(StepLog)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Login button
                self.testStep = "Clicking Login button"
                try:
                    self.lp.clickLogin()
                    StepLog = "######## Login button clicked"
                    #self.logger.info(StepLog)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Verifying page title
                self.testStep = "User logged in successfully, verifying page title"
                try:
                    act_title = self.lp.pageTitle()
                    StepLog = "######## Login button clicked, verifying page title"
                    #self.logger.info(StepLog)
                    if act_title == "Dispatcher portal":
                        EndTime = datetime.now()
                        XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                    else:
                        self.error = "$-unmatched page title, Login Failed-$"
                        raise Exception
                except:
                    raise Exception

                count = int(scenarioDataList[3])
                for i in range(1, count+1):
                    #print(f"Iteration: {i}")

                    # ---------Clicking Create Work Order Button
                    self.testStep = "Clicking Create Work Order Button"
                    try:
                        self.lp.clickbutton_CreateWorkOrder().click()
                        StepLog = "######## Create Work Order button clicked"
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Entering City
                    self.testStep = "Entering City"
                    city = scenarioDataList[4]
                    try:
                        self.lp.searchCity(city)
                        StepLog = "######## City searched : " + city
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Entering Address
                    self.testStep = "Entering Address"
                    address = scenarioDataList[5]
                    try:
                        self.lp.searchAddress(address)
                        time.sleep(1)
                        self.lp.clickbutton_SearchCity()
                        StepLog = "######## Address searched : " + address
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Selecting location
                    self.testStep = "Selecting location"
                    location = scenarioDataList[5]
                    try:
                        self.lp.selectAddress(location)
                        StepLog = "######## location selected : " + location
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Selecting property person
                    self.testStep = "Selecting property person"
                    person = scenarioDataList[6]
                    try:
                        self.lp.selectAddressPerson(person)
                        StepLog = "######## property person : " + person
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Clicking Create New Work Order(s) button
                    self.testStep = "Clicking Create New Work Order(s) button"
                    try:
                        Support_Functions.scrolldownByOne(self.driver, setup)
                        Support_Functions.scrolldownByOne(self.driver, setup)
                        Support_Functions.scrolldownByOne(self.driver, setup)
                        time.sleep(3)
                        self.lp.clickbutton_CreateNewWorkOrder()
                        StepLog = "######## Create New Work Order(s) button clicked ########"
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Selecting Category
                    self.testStep = "Selecting Category"
                    category = scenarioDataList[7]
                    try:
                        Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_SelectCategory())
                        self.lp.selectCategory(category)
                        StepLog = "######## Category selected : " + category
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Clicking Next button
                    self.testStep = "Clicking Next button"
                    try:
                        self.lp.clickbutton_next_Category_xpath()
                        StepLog = "######## Next button clicked ########"
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception
                    # =====================================================================================

                    self.testStep = "Selecting Issue"
                    issue = scenarioDataList[8]
                    try:
                        self.lp.clickradiobtn_issue_xpath(issue)
                        #self.logger.info("######## Issue selected : " + issue)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    self.testStep = "Clicking Next button"
                    try:
                        Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                        self.lp.clickbutton_next_Category_xpath()
                        #self.logger.info("######## Next button clicked ########")
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    self.testStep = "Selecting Issue Description"
                    issueDescribe = scenarioDataList[9]
                    try:
                        self.lp.clickradiobtn_issueDescribe_xpath(issueDescribe)
                        #self.logger.info("######## Issue Description selected : " + issueDescribe)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    self.testStep = "Clicking Next button"
                    try:
                        Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                        self.lp.clickbutton_next_Category_xpath()
                        #self.logger.info("######## Next button clicked ########")
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    self.testStep = "Selecting Changed batteries radio selection"
                    changedBatteries = scenarioDataList[10]
                    try:
                        self.lp.clickradiobtn_Batteries_xpath(changedBatteries)
                        #self.logger.info("######## Changed batteries selected : " + changedBatteries)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    self.testStep = "Clicking Next button"
                    try:
                        Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                        self.lp.clickbutton_next_Category_xpath()
                        #self.logger.info("######## Next button clicked ########")
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ==================================== Common Steps 2 ====================================
                    # ---------Adding Additional comment
                    self.testStep = "Adding Additional comment"
                    comments = "Iteration: "+str(i) + " - " + scenarioDataList[11]
                    try:
                        self.lp.setAdditionalComments(comments)
                        StepLog = "######## Additional comment added : " + comments
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Clicking Next button
                    self.testStep = "Clicking Next button"
                    try:
                        Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                        self.lp.clickbutton_next_Category_xpath()
                        StepLog = "######## Next button clicked ########"
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Creating Work order
                    self.testStep = "Creating Work order"
                    #self.logger.info("Work order created successfully")
                    EndTime = datetime.now()
                    XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                            scenarioDataList[1], self.testStep, "None", StartTime, EndTime)

                    # ---------Clicking Intake Summary And Scheduling button
                    self.testStep = "Clicking Intake Summary And Scheduling button"
                    schedule = scenarioDataList[12]
                    try:
                        #Support_Functions.scrolldownByOne(self.driver, setup)
                        self.lp.clickBtn_IntakeSummaryAndScheduling_xpath(schedule)
                        StepLog = "######## Intake Summary And Scheduling Button clicked: " + schedule
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Clicking Schedule button
                    self.testStep = "Clicking Schedule button"
                    schedule = scenarioDataList[13]
                    try:
                        Support_Functions.scrolldownByOne(self.driver, setup)
                        self.lp.clickBtn_WOSchedule_xpath(schedule)
                        StepLog = "######## Button clicked: " + schedule
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    time.sleep(3)
                    # ---------Fetching Work Order Number on Scheduling page
                    self.testStep = "Fetching work order number displayed on Scheduling page"
                    try:
                        WO = self.lp.fetchtext_WONumberSchedulingPage_xpath()
                        WOList.append(WO)
                        StepLog = "######## WO Number on Scheduling page Fetched: +" + WO
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                    # ---------Fetching Work Order Status on Scheduling page
                    self.testStep = "Fetching work order Status displayed on Scheduling page"
                    try:
                        WOStatus = self.lp.fetchtext_WOStatusSchedulingPage_xpath()
                        StepLog = "######## WO Status on Scheduling page Fetched: +" + WOStatus
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception
                    # =====================================================================================

                    # ---------Clicking Leave Unassigned button
                    self.testStep = "Clicking Leave Unassigned button"
                    try:
                        Support_Functions.scrolldownByOne(self.driver, setup)
                        Support_Functions.scrolldownByOne(self.driver, setup)
                        self.lp.clickbutton_LeaveUnassignedSchedulingPage()
                        StepLog = "######## Leave Unassigned button clicked ########"
                        #self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                # ---------Ending the test scenario
                WorkOrderDetailsFound["Created_Work_Orders"] = WOList
                print(WorkOrderDetailsFound)
                EndTime = datetime.now()
                StepLog = "######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
                    1] + " completed successfully and ended at " + str(EndTime) + " ########"
                print(StepLog)
                #self.logger.info(StepLog)


            except Exception as e:
                screenshotFile = type(self).__name__ + "[" + inspect.stack()[0][3] + "].png"
                path = self.basePath
                text = path.split("/")
                for t in text:
                    if t == ".jenkins":
                        print("Running on Jenkins")
                        path = os.path.dirname(self.basePath)
                        print("path is " + path)
                    else:
                        pass
                self.driver.save_screenshot(path + "/Screenshots/" + screenshotFile)
                self.errorMessage = "######## Test case failed due to " + self.error + ". Screenshot file: " + screenshotFile + " is present in screenshots folder attached"
                #self.logger.error(self.errorMessage)

                EndTime = datetime.now()
                XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                        scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)

                self.driver.close()
                assert False

        else:
            print("Skipping Scenario Execution for: " + scenarioDataList[0])
