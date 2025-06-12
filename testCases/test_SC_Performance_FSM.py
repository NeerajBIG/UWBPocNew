import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from selenium.webdriver.common.by import By
from utilities.supportFxn import Support_Functions
import speedtest
import inspect
import time
from pageObjects.AllElementLocators import ElementLocators
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import XLUtils
from datetime import datetime
from fpdf import FPDF
from copy import deepcopy
from pyjavaproperties import Properties
import tzlocal

class Test_Performance_FSM():
    network = speedtest.Speedtest(secure=True)
    down = network.download() / 1000000
    up = network.upload() / 1000000

    ApplicationName = "Tricon FSM"
    logger = LogGen.loggen()
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"
    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
    sheetName_Data = "TestUserData"
    sheetName_Report = "Report"
    sheetName_Scenarios = "Scenarios"
    testStep = "Launching Application"
    error = ""

    #--Pdf Report configuration
    ReportHeader = "Performance Testing Report - " + ApplicationName
    ReportIntroduction = "The objective of performance testing is to evaluate how "+ApplicationName+" application performs under various conditions, such as different concurrent user loads, data load, and network. This type of testing aims to identify potential bottlenecks, performance issues, and system vulnerabilities that could affect user experience, reliability, or scalability. By simulating real-world traffic and usage scenarios, performance testing helps ensure that the system can handle the expected number of concurrent users, process transactions efficiently, and maintain stability under peak loads."
    ReportMethodology = "The test methodology used in this performance test focusing on page load time to measure how quickly a web page loads at different section under various conditions, including different network speeds and user traffic loads. By analyzing the page load times across different sections of the application, the testing aims to pinpoint areas of optimization, such as server response time, content delivery, and front-end performance, ensuring that the page loads efficiently and provides a seamless user experience."
    ReportKeyFindings = "Please observe the load time (Front End) marked in red color in following tables. An ideal page load time is between 0-3 seconds, 4 seconds is also considered to be an acceptable score. Anything above 4 seconds should be investigated and improved."
    LoadTimeThreshold = 4
    output_pdf = "Pdf3-TriconFSM-Output_Report.pdf"

    p = Properties()
    p.load(open(basePath+'/testCases/FSMProp.properties'))
    p.list()
    ThreadCount = p['threadcount']
    WOCount = p['workordercount']
    cloudstorage = p['clouddatastorgae']

    def test_Performance_FSM(self, setup):

        best = self.network.get_best_server()
        print(f"Found: {best['host']} located in {best['country']}")
        print("Download Speed: {:.2f} Mbps".format(self.down))
        print("Upload Speed: {:.2f} Mbps".format(self.up))
        down = "Download Speed: {:.2f} Mbps".format(self.down)
        up = "Upload Speed: {:.2f} Mbps".format(self.up)
        # down = "Test"
        # up = "Test"

        print(tzlocal.get_localzone_name())
        WOList = []

        #-Initializing PDF
        pdf = FPDF()
        pdf.add_page()

        scenario_ID = "SC_017"
        scenarioDataList = XLUtils.readDataScenarios(self.dataSheetPath, self.sheetName_Scenarios, scenario_ID)
        StartTime = datetime.now()
        log = "######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
            1] + " started at " + str(StartTime) + " ########"
        print(log)
        Enable = scenarioDataList[2]

        countLoop = 1

        # -Setting report header images on left and right side of the page
        pdf.image('C:/Users/neera/PycharmProjects/TriconFSM/utilities/BitsInGlassLogo.png', 5, 5,
                   33)  # (path, x, y, width)
        pdf.image('C:/Users/neera/PycharmProjects/TriconFSM/utilities/TriconResidentialLogo.png', 173, 5,
                   33, 10)  # (path, x, y, width)

        # -Setting report header text in the center of the page
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 15, txt=self.ReportHeader, ln=True, align='C')

        RightSectionSize = 7
        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Report Timestamp: "+str(StartTime.strftime("%m-%d-%Y, %H:%M:%S")) +" "+tzlocal.get_localzone_name(), ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(190, 5, txt="Testing URL: " + self.baseURL, ln=True, align='R')
        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Testing Environment: " + self.Env, ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Current Network Speed: " + str(up) +" "+ str(down), ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Virtual User Count <= " + str(self.ThreadCount), ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Work Orders Count >= " + str(self.WOCount), ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Cloud Data Storage: " + str(self.cloudstorage), ln=True, align='R')

        # -Setting report Objective
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Test Objective", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, self.ReportIntroduction, 0, 'L')

        # -Setting report Methodology
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Test Methodology", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, self.ReportMethodology, 0, 'L')

        # -Setting report Key Findings
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Key Findings", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, self.ReportKeyFindings, 0, 'L')

        if Enable is True:
            try:
                # ==================================== Common Steps 1 ====================================

                # ---------Initiating WebDriver and Launching Application
                self.driver = setup
                self.driver.get(self.baseURL)
                StepLog = "Test Step : " + self.testStep
                self.logger.info(StepLog)
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
                    self.logger.info(StepLog)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Entering Password
                self.testStep = "Entering Password"
                password = self.password
                try:
                    self.lp.setPassword(password)
                    print("password " + password)
                    StepLog = "######## Password entered : " + "##########"
                    self.logger.info(StepLog)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Clicking Login button
                self.testStep = "Clicking Login button"
                try:
                    self.lp.clickLogin()
                    StepLog = "######## Login button clicked"
                    self.logger.info(StepLog)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------------------------------Resetting Current Password if required-----------------------------------
                try:
                    #print("Inside try resetting password")
                    aa = self.driver.find_element(By.XPATH, "//div[text()='Security policies require that you change your password.']").text
                    print("aa: " + aa)
                    if aa == "Security policies require that you change your password.":
                        self.testStep = "Resetting Current Password"
                        password = self.password
                        try:
                            self.lp.setOldPassword(password)
                            uniqueText = "rules@"+str(StartTime.strftime("%m%d%Y"))
                            print("New Password set as: " + uniqueText)
                            self.lp.setNewPassword1(uniqueText)
                            self.lp.setNewPassword2(uniqueText)
                            StepLog = "######## Changed Password entered"
                            self.logger.info(StepLog)
                        except Exception as ee1:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                    # ---------Clicking Change password button
                    self.testStep = "Clicking Change password button"
                    try:
                        self.lp.clickButton_ChangePassword()
                        StepLog = "######## Change password button clicked"
                        self.logger.info(StepLog)
                    except:
                        self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        raise Exception

                except Exception as ee:
                    #print("Inside except resetting password")
                    pass

                # ---------------------------------Setting report Section - Dashboard-----------------------------------
                StartTime = datetime.now()
                pdf.multi_cell(0, 5, '\n')
                SectionName = "Dashboard"
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)

                # -Setting report Header Section Values
                header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                data1=[]
                data1array = []

                for i in range(1, countLoop + 1):
                    data1array.clear()
                    data1array.append(SectionName)
                    data1array.append(str(i))
                    if i > 1:
                        StartTime = datetime.now()
                    iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                    self.driver.switch_to.frame(iframe)

                    # ---------Verifying page title
                    self.testStep = "Searching element: " + SectionName + " " + str(i)
                    for i1 in range(1, 10):
                        print("i1: " + str(i1))
                        try:
                            # ---------Clicking Send To Vendor WO OK button
                            self.lp.Clicktab_WarrantyWO()
                            EndTime = datetime.now()
                            time_difference = EndTime - StartTime
                            XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                    scenarioDataList[1], self.testStep, "None", StartTime, EndTime)

                            navigationStart = self.driver.execute_script(
                                "return window.performance.timing.navigationStart")
                            responseStart = self.driver.execute_script("return window.performance.timing.responseStart")
                            domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                            backendPerformance_calc = responseStart - navigationStart
                            frontendPerformance_calc = domComplete - responseStart
                            data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                            data1array.append(str(round(float(backendPerformance_calc),2)/1000))
                            data1.append(deepcopy(data1array))
                            break
                        except Exception as e1:
                            pass
                    self.driver.refresh()

                pdf.set_font('Arial', 'B', 10)
                for idx, item in enumerate(header):
                    if idx == 0:
                        pdf.cell(75, 10, item, 1, 0, 'C')
                    elif idx == 1:
                        pdf.cell(22, 10, item, 1, 0, 'C')
                    else:
                        pdf.cell(47, 10, item, 1, 0, 'C')
                pdf.ln()
                # Table Body
                pdf.set_font('Arial', '', 10)
                for row in data1:
                    for idx2, item in enumerate(row):
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 10)
                        if idx2 == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')

                        elif idx2 == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        elif idx2 == 2:
                            if float(item) > self.LoadTimeThreshold:
                                pdf.set_text_color(255, 0, 0)
                                pdf.set_font('Arial', 'B', 10)
                            pdf.cell(47, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                # -------------------------------------------------------------------------------------------------------

                # ---------------------------------Setting report Section - Dispatcher Map-----------------------------------
                StartTime = datetime.now()
                pdf.multi_cell(0, 5, '\n')
                SectionName = "Dispatcher Map"
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)

                # -Setting report Header Section Values
                header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                data1 = []
                data1array = []

                for i in range(1, countLoop + 1):
                    data1array.clear()
                    data1array.append(SectionName)
                    data1array.append(str(i))
                    if i > 1:
                        StartTime = datetime.now()
                    iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                    self.driver.switch_to.frame(iframe)

                    # ---------Verifying page title
                    self.testStep = "Searching element: "+SectionName+" " + str(i)
                    for i1 in range(1, 10):
                        print("i1: " + str(i1))
                        try:
                            # ---------Clicking Send To Vendor WO OK button
                            self.lp.element_DispatcherMap()
                            EndTime = datetime.now()
                            time_difference = EndTime - StartTime
                            XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                    scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                            navigationStart = self.driver.execute_script(
                                "return window.performance.timing.navigationStart")
                            responseStart = self.driver.execute_script("return window.performance.timing.responseStart")
                            domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                            backendPerformance_calc = responseStart - navigationStart
                            frontendPerformance_calc = domComplete - responseStart
                            data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                            data1array.append(str(round(float(backendPerformance_calc), 2) / 1000))
                            data1.append(deepcopy(data1array))
                            break
                        except Exception as e1:
                            print("Exception: " + str(e1))
                            pass
                    self.driver.refresh()

                pdf.set_font('Arial', 'B', 10)
                for idx, item in enumerate(header):
                    if idx == 0:
                        pdf.cell(75, 10, item, 1, 0, 'C')
                    elif idx == 1:
                        pdf.cell(22, 10, item, 1, 0, 'C')
                    else:
                        pdf.cell(47, 10, item, 1, 0, 'C')
                pdf.ln()
                # Table Body
                pdf.set_font('Arial', '', 10)
                for row in data1:
                    for idx2, item in enumerate(row):
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 10)
                        if idx2 == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')

                        elif idx2 == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        elif idx2 == 2:
                            if float(item) > self.LoadTimeThreshold:
                                pdf.set_text_color(255, 0, 0)
                                pdf.set_font('Arial', 'B', 10)
                            pdf.cell(47, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                # -------------------------------------------------------------------------------------------------------

                # ---------------------------------Setting report Section - Workers List-----------------------------------
                StartTime = datetime.now()
                pdf.multi_cell(0, 5, '\n')
                SectionName = "Workers List"
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)

                # -Setting report Header Section Values
                header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                data1 = []
                data1array = []

                for i in range(1, countLoop + 1):
                    data1array.clear()
                    data1array.append(SectionName)
                    data1array.append(str(i))
                    if i > 1:
                        StartTime = datetime.now()
                    iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                    self.driver.switch_to.frame(iframe)

                    # ---------Verifying page title
                    self.testStep = "Searching element: "+SectionName+" " + str(i)
                    self.lp.clickradiobtn_ShowAllWorkers_xpath()
                    for i1 in range(1, 10):
                        print("i1: " + str(i1))
                        try:
                            # ---------Clicking Send To Vendor WO OK button
                            EndTime = datetime.now()
                            self.lp.element_Workers_Pagination()
                            time_difference = EndTime - StartTime
                            XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                    scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                            navigationStart = self.driver.execute_script(
                                "return window.performance.timing.navigationStart")
                            responseStart = self.driver.execute_script(
                                "return window.performance.timing.responseStart")
                            domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                            backendPerformance_calc = responseStart - navigationStart
                            frontendPerformance_calc = domComplete - responseStart
                            data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                            data1array.append(str(round(float(backendPerformance_calc), 2) / 1000))
                            data1.append(deepcopy(data1array))
                            break
                        except Exception as e1:
                            print("Exception: " + str(e1))
                            pass
                    self.driver.refresh()

                pdf.set_font('Arial', 'B', 10)
                for idx, item in enumerate(header):
                    if idx == 0:
                        pdf.cell(75, 10, item, 1, 0, 'C')
                    elif idx == 1:
                        pdf.cell(22, 10, item, 1, 0, 'C')
                    else:
                        pdf.cell(47, 10, item, 1, 0, 'C')
                pdf.ln()
                # Table Body
                pdf.set_font('Arial', '', 10)
                for row in data1:
                    for idx2, item in enumerate(row):
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 10)
                        if idx2 == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')

                        elif idx2 == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        elif idx2 == 2:
                            if float(item) > self.LoadTimeThreshold:
                                pdf.set_text_color(255, 0, 0)
                                pdf.set_font('Arial', 'B', 10)
                            pdf.cell(47, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                # -------------------------------------------------------------------------------------------------------

                # ---------------------------------Setting report Section - Searching Work Order-----------------------------------
                StartTime = datetime.now()
                pdf.multi_cell(0, 5, '\n')
                SectionName = "Searching Work Order"
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)

                # -Setting report Header Section Values
                header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                data1 = []
                data1array = []

                for i in range(1, countLoop + 1):
                    data1array.clear()
                    data1array.append(SectionName)
                    data1array.append(str(i))
                    if i > 1:
                        StartTime = datetime.now()
                    iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                    self.driver.switch_to.frame(iframe)

                    # ---------Verifying page title
                    self.testStep = "Searching element: "+SectionName+" " + str(i)
                    self.driver.find_element(By.XPATH, ElementLocators.search_xpath).clear()
                    self.driver.find_element(By.XPATH, ElementLocators.search_xpath).send_keys("W")
                    time.sleep(1)
                    Support_Functions.performEnter(self.driver, setup)
                    for i1 in range(1, 10):
                        print("i1: " + str(i1))
                        try:
                            EndTime = datetime.now()
                            self.lp.element_First_WOGlobalSearch()
                            time_difference = EndTime - StartTime
                            XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                    scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                            navigationStart = self.driver.execute_script(
                                "return window.performance.timing.navigationStart")
                            responseStart = self.driver.execute_script(
                                "return window.performance.timing.responseStart")
                            domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                            backendPerformance_calc = responseStart - navigationStart
                            frontendPerformance_calc = domComplete - responseStart
                            data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                            data1array.append(str(round(float(backendPerformance_calc), 2) / 1000))
                            data1.append(deepcopy(data1array))
                            break
                        except Exception as e1:
                            print("Exception: " + str(e1))
                            pass
                    self.driver.refresh()

                pdf.set_font('Arial', 'B', 10)
                for idx, item in enumerate(header):
                    if idx == 0:
                        pdf.cell(75, 10, item, 1, 0, 'C')
                    elif idx == 1:
                        pdf.cell(22, 10, item, 1, 0, 'C')
                    else:
                        pdf.cell(47, 10, item, 1, 0, 'C')
                pdf.ln()
                # Table Body
                pdf.set_font('Arial', '', 10)
                for row in data1:
                    for idx2, item in enumerate(row):
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 10)
                        if idx2 == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')

                        elif idx2 == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        elif idx2 == 2:
                            if float(item) > self.LoadTimeThreshold:
                                pdf.set_text_color(255, 0, 0)
                                pdf.set_font('Arial', 'B', 10)
                            pdf.cell(47, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                # -------------------------------------------------------------------------------------------------------

                # ---------------------------------Setting report Section - Searching & Opening Work Order-----------------------------------
                StartTime = datetime.now()
                pdf.multi_cell(0, 5, '\n')
                SectionName = "Searching & Opening Work Order (together)"
                print("SectionName is " + SectionName)
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)

                # -Setting report Header Section Values
                header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                data1 = []
                data1array = []
                for i in range(1, countLoop + 1):
                    data1array.clear()
                    data1array.append(SectionName)
                    data1array.append(str(i))
                    if i > 1:
                        StartTime = datetime.now()
                    iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                    self.driver.switch_to.frame(iframe)

                    # ---------Verifying page title
                    self.testStep = "Searching element: " + SectionName + " " + str(i)
                    self.driver.find_element(By.XPATH, ElementLocators.search_xpath).clear()
                    self.driver.find_element(By.XPATH, ElementLocators.search_xpath).send_keys("W")
                    time.sleep(1)
                    Support_Functions.performEnter(self.driver, setup)
                    time.sleep(1)
                    self.lp.element_First_WOGlobalSearchClick()
                    for i1 in range(1, 10):
                        print("i1: " + str(i1))
                        try:
                            EndTime = datetime.now()
                            self.lp.fetchtext_WOStatus_xpath()
                            time_difference = EndTime - StartTime
                            XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                    scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                            navigationStart = self.driver.execute_script(
                                "return window.performance.timing.navigationStart")
                            responseStart = self.driver.execute_script(
                                "return window.performance.timing.responseStart")
                            domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                            backendPerformance_calc = responseStart - navigationStart
                            frontendPerformance_calc = domComplete - responseStart
                            data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                            data1array.append(str(round(float(backendPerformance_calc), 2) / 1000))
                            data1.append(deepcopy(data1array))
                            self.lp.clickicon_CloseWODetails()
                            break
                        except Exception as e1:
                            print("Exception: " + str(e1))
                            pass
                    self.driver.refresh()

                pdf.set_font('Arial', 'B', 10)
                for idx, item in enumerate(header):
                    if idx == 0:
                        pdf.cell(75, 10, item, 1, 0, 'C')
                    elif idx == 1:
                        pdf.cell(22, 10, item, 1, 0, 'C')
                    else:
                        pdf.cell(47, 10, item, 1, 0, 'C')
                pdf.ln()
                # Table Body
                pdf.set_font('Arial', '', 10)
                for row in data1:
                    for idx2, item in enumerate(row):
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 10)
                        if idx2 == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')

                        elif idx2 == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        elif idx2 == 2:
                            if float(item) > self.LoadTimeThreshold:
                                pdf.set_text_color(255, 0, 0)
                                pdf.set_font('Arial', 'B', 10)
                            pdf.cell(47, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                # -------------------------------------------------------------------------------------------------------

                # ---------------------------------Setting report Section - Create Work Order: Step 1-----------------------------------
                pdf.multi_cell(0, 5, '\n')
                SectionName = "Create Work Order: Step 1"
                print("SectionName is " + SectionName)
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)
                # -Setting report Header Section Values
                header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                data1 = []
                data1array = []
                self.lp.clickbutton_CreateWorkOrder().click()
                StartTime = datetime.now()
                for i in range(1, countLoop + 1):
                    data1array.clear()
                    data1array.append(SectionName)
                    data1array.append(str(i))
                    if i > 1:
                        self.lp.clickbutton_CreateWorkOrder().click()
                        StartTime = datetime.now()
                    # iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                    # self.driver.switch_to.frame(iframe)
                    self.driver.switch_to.default_content()
                    # ---------Verifying page title
                    self.testStep = "Searching element: " + SectionName + " " + str(i)
                    for i1 in range(1, 10):
                        print("i1: " + str(i1))
                        try:
                            self.lp.element_CityLabel()
                            EndTime = datetime.now()
                            time_difference = EndTime - StartTime
                            XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                    scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                            navigationStart = self.driver.execute_script(
                                "return window.performance.timing.navigationStart")
                            responseStart = self.driver.execute_script(
                                "return window.performance.timing.responseStart")
                            domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                            backendPerformance_calc = responseStart - navigationStart
                            frontendPerformance_calc = domComplete - responseStart
                            data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                            data1array.append(str(round(float(backendPerformance_calc), 2) / 1000))
                            data1.append(deepcopy(data1array))
                            self.lp.clickbutton_BackToDispatch()
                            break
                        except Exception as e1:
                            print("Exception: " + str(e1))
                            pass
                    self.driver.refresh()

                pdf.set_font('Arial', 'B', 10)
                for idx, item in enumerate(header):
                    if idx == 0:
                        pdf.cell(75, 10, item, 1, 0, 'C')
                    elif idx == 1:
                        pdf.cell(22, 10, item, 1, 0, 'C')
                    else:
                        pdf.cell(47, 10, item, 1, 0, 'C')
                pdf.ln()
                # Table Body
                pdf.set_font('Arial', '', 10)
                for row in data1:
                    for idx2, item in enumerate(row):
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 10)
                        if idx2 == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')

                        elif idx2 == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        elif idx2 == 2:
                            if float(item) > self.LoadTimeThreshold:
                                pdf.set_text_color(255, 0, 0)
                                pdf.set_font('Arial', 'B', 10)
                            pdf.cell(47, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                # -------------------------------------------------------------------------------------------------------

                if self.Env == "PROD":
                    print("Current Environment is: " + self.Env)
                else:
                    print("Current Environment is: " + self.Env)
                    StartTime = datetime.now()
                    #count = int(scenarioDataList[3])
                    count = 1
                    for i in range(1, count + 1):
                        # ---------Clicking Create Work Order Button
                        self.testStep = "Clicking Create Work Order Button"
                        try:
                            self.lp.clickbutton_CreateWorkOrder().click()
                            StepLog = "######## Create Work Order button clicked"
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Entering City
                        self.testStep = "Entering City"
                        city = scenarioDataList[4]
                        try:
                            self.lp.searchCity(city)
                            StepLog = "######## City searched : " + city
                            self.logger.info(StepLog)
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
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Selecting location
                        self.testStep = "Selecting location"
                        location = scenarioDataList[5]
                        try:
                            self.lp.selectAddress(location)
                            StepLog = "######## location selected : " + location
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Selecting property person
                        self.testStep = "Selecting property person"
                        person = scenarioDataList[6]
                        try:
                            self.lp.selectAddressPerson(person)
                            StepLog = "######## property person : " + person
                            self.logger.info(StepLog)
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
                            self.logger.info(StepLog)
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
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Clicking Next button
                        self.testStep = "Clicking Next button"
                        try:
                            self.lp.clickbutton_next_Category_xpath()
                            StepLog = "######## Next button clicked ########"
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception
                        # =====================================================================================

                        self.testStep = "Selecting Issue"
                        issue = scenarioDataList[8]
                        try:
                            self.lp.clickradiobtn_issue_xpath(issue)
                            self.logger.info("######## Issue selected : " + issue)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        self.testStep = "Clicking Next button"
                        try:
                            Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                            self.lp.clickbutton_next_Category_xpath()
                            self.logger.info("######## Next button clicked ########")
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        self.testStep = "Selecting Issue Description"
                        issueDescribe = scenarioDataList[9]
                        try:
                            self.lp.clickradiobtn_issueDescribe_xpath(issueDescribe)
                            self.logger.info("######## Issue Description selected : " + issueDescribe)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        self.testStep = "Clicking Next button"
                        try:
                            Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                            self.lp.clickbutton_next_Category_xpath()
                            self.logger.info("######## Next button clicked ########")
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        self.testStep = "Selecting Changed batteries radio selection"
                        changedBatteries = scenarioDataList[10]
                        try:
                            self.lp.clickradiobtn_Batteries_xpath(changedBatteries)
                            self.logger.info("######## Changed batteries selected : " + changedBatteries)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        self.testStep = "Clicking Next button"
                        try:
                            Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                            self.lp.clickbutton_next_Category_xpath()
                            self.logger.info("######## Next button clicked ########")
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ==================================== Common Steps 2 ====================================
                        # ---------Adding Additional comment
                        self.testStep = "Adding Additional comment"
                        comments = "Iteration: " + str(i) + " - " + scenarioDataList[11]
                        try:
                            self.lp.setAdditionalComments(comments)
                            StepLog = "######## Additional comment added : " + comments
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Clicking Next button
                        self.testStep = "Clicking Next button"
                        try:
                            Support_Functions.scrollToElement(self.driver, setup, self.lp.ele_NextButton())
                            self.lp.clickbutton_next_Category_xpath()
                            StepLog = "######## Next button clicked ########"
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Creating Work order
                        self.testStep = "Creating Work order"
                        self.logger.info("Work order created successfully")
                        EndTime = datetime.now()
                        XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                scenarioDataList[1], self.testStep, "None", StartTime, EndTime)

                        # # ---------Clicking Intake Summary And Scheduling button
                        # self.testStep = "Clicking Intake Summary And Scheduling button"
                        # schedule = scenarioDataList[12]
                        # try:
                        #     # Support_Functions.scrolldownByOne(self.driver, setup)
                        #     self.lp.clickBtn_IntakeSummaryAndScheduling_xpath(schedule)
                        #     StepLog = "######## Intake Summary And Scheduling Button clicked: " + schedule
                        #     self.logger.info(StepLog)
                        # except:
                        #     self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        #     raise Exception

                        # ---------Clicking Schedule button
                        self.testStep = "Clicking Schedule button"
                        schedule = scenarioDataList[13]
                        try:
                            Support_Functions.scrolldownByOne(self.driver, setup)
                            self.lp.clickBtn_WOSchedule_xpath(schedule)
                            StepLog = "######## Button clicked: " + schedule
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        time.sleep(3)
                        # # ---------Fetching Work Order Number on Scheduling page
                        # self.testStep = "Fetching work order number displayed on Scheduling page"
                        # try:
                        #     WO = self.lp.fetchtext_WONumberSchedulingPage_xpath()
                        #     WOList.append(WO)
                        #     StepLog = "######## WO Number on Scheduling page Fetched: +" + WO
                        #     self.logger.info(StepLog)
                        # except:
                        #     self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        #     raise Exception
                        #
                        # # ---------Fetching Work Order Status on Scheduling page
                        # self.testStep = "Fetching work order Status displayed on Scheduling page"
                        # try:
                        #     WOStatus = self.lp.fetchtext_WOStatusSchedulingPage_xpath()
                        #     StepLog = "######## WO Status on Scheduling page Fetched: +" + WOStatus
                        #     self.logger.info(StepLog)
                        # except:
                        #     self.error = "No web element found, ref: [ " + self.testStep + " ]"
                        #     raise Exception
                        # =====================================================================================

                        # ---------Clicking Leave Unassigned button
                        self.testStep = "Clicking Leave Unassigned button"
                        try:
                            self.lp.clickbutton_LeaveUnassignedSchedulingPage()
                            StepLog = "######## Leave Unassigned button clicked ########"
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception

                        # ---------Clicking Finish button
                        self.testStep = "Clicking Finish button"
                        try:
                            self.lp.clickButton_Finish()
                            StepLog = "######## Finish button clicked ########"
                            self.logger.info(StepLog)
                        except:
                            self.error = "No web element found, ref: [ " + self.testStep + " ]"
                            raise Exception
                    pass

                    # ---------------------------------Setting report Section - Work Order Creation-----------------------------------
                    pdf.multi_cell(0, 5, '\n')
                    SectionName = "Work Order Creation"
                    print("SectionName is " + SectionName)
                    pdf.set_font('Arial', 'B', 12)
                    pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)
                    # -Setting report Header Section Values
                    header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
                    data1 = []
                    data1array = []
                    for i in range(1, 2):
                        data1array.clear()
                        data1array.append(SectionName)
                        data1array.append(str(i))
                        iframe = self.driver.find_element(By.XPATH, "//iframe[@name='PegaGadget0Ifr']")
                        self.driver.switch_to.frame(iframe)
                        # ---------Verifying page title
                        self.testStep = "Searching element: " + SectionName + " " + str(i)
                        for i1 in range(1, 10):
                            print("i1: " + str(i1))
                            try:
                                self.lp.element_DispatcherMap()
                                EndTime = datetime.now()
                                time_difference = EndTime - StartTime
                                XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                                        scenarioDataList[1], self.testStep, "None", StartTime, EndTime)
                                navigationStart = self.driver.execute_script(
                                    "return window.performance.timing.navigationStart")
                                responseStart = self.driver.execute_script(
                                    "return window.performance.timing.responseStart")
                                domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
                                backendPerformance_calc = responseStart - navigationStart
                                frontendPerformance_calc = domComplete - responseStart
                                data1array.append(str(round(float(time_difference.total_seconds()), 2)))
                                data1array.append(str(round(float(backendPerformance_calc), 2) / 1000))
                                data1.append(deepcopy(data1array))
                                break
                            except Exception as e1:
                                print("Exception: " + str(e1))
                                pass

                    pdf.set_font('Arial', 'B', 10)
                    for idx, item in enumerate(header):
                        if idx == 0:
                            pdf.cell(75, 10, item, 1, 0, 'C')
                        elif idx == 1:
                            pdf.cell(22, 10, item, 1, 0, 'C')
                        else:
                            pdf.cell(47, 10, item, 1, 0, 'C')
                    pdf.ln()
                    # Table Body
                    pdf.set_font('Arial', '', 10)
                    for row in data1:
                        for idx2, item in enumerate(row):
                            pdf.set_text_color(0, 0, 0)
                            pdf.set_font('Arial', '', 10)
                            if idx2 == 0:
                                pdf.cell(75, 10, item, 1, 0, 'C')

                            elif idx2 == 1:
                                pdf.cell(22, 10, item, 1, 0, 'C')
                            elif idx2 == 2:
                                if float(item) > self.LoadTimeThreshold:
                                    pdf.set_text_color(255, 0, 0)
                                    pdf.set_font('Arial', 'B', 10)
                                pdf.cell(47, 10, item, 1, 0, 'C')
                            else:
                                pdf.cell(47, 10, item, 1, 0, 'C')
                        pdf.ln()
                    # -------------------------------------------------------------------------------------------------------

                EndTime = datetime.now()
                pdf.set_font('Arial', 'B', RightSectionSize)
                pdf.cell(0, 15, txt=" ", ln=True, align='L')
                pdf.cell(0, 15, txt="Report End Timestamp: " + str(
                    StartTime.strftime("%m-%d-%Y, %H:%M:%S")) + " " + tzlocal.get_localzone_name(), ln=True, align='L')
                pdf.cell(0, 5, txt="Note: ", ln=True, align='L')
                pdf.cell(0, 5, txt="1) Python version: 3.9", ln=True, align='L')
                pdf.cell(0, 5, txt="1) JMeter version: apache-jmeter-5.5", ln=True, align='L')
                pdf.cell(0, 5, txt="2) JMeter Thread Count: Virtual User Count as given above.", ln=True, align='L')
                pdf.cell(0, 5, txt="3) JMeter Ramp-up Period(in seconds): 1 second.", ln=True, align='L')
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 5, txt="To understand more about JMeter, click here", ln=True, align='L', link='https://jmeter.apache.org/usermanual/test_plan.html#thread_group')

                # ---------Ending the test scenario
                EndTime = datetime.now()
                StepLog = "######## " + scenarioDataList[0] + " Test scenario: " + scenarioDataList[
                    1] + " completed successfully and ended at " + str(EndTime) + " ########"
                print(StepLog)
                self.logger.info(StepLog)
                self.driver.close()

                #-Creating PDF output file
                pdf.output(self.basePath+"/Reports/"+self.output_pdf)
                print(f"PDF created successfully: {self.output_pdf}")


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
                self.logger.error(self.errorMessage)

                EndTime = datetime.now()
                XLUtils.writeDataReport(self.dataSheetPath, self.sheetName_Report, scenario_ID,
                                        scenarioDataList[1], self.testStep, self.errorMessage, StartTime, EndTime)

                self.driver.close()
                assert False
        else:
            print("Skipping Scenario Execution for: " + scenarioDataList[0])
