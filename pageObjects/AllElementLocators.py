import os, sys
from os.path import dirname, join, abspath
#import tzlocal
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from datetime import datetime
import inspect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from testCases.configTest import setup
from utilities import XLUtils
from utilities.readProperties import ReadConfig
import time
import matplotlib.pyplot as plt
from fpdf import FPDF
from testCases.testResultData import testResult


class ElementLocators:
    Time = ReadConfig.getWaitTimeForEachElement()
    halt = 1
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"
    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")

    def __init__(self, driver):
        self.driver = driver

    def inputData(self, xp, data):
        xpath = xp
        try:
            if WebDriverWait(self.driver, self.Time).until(
                    EC.presence_of_element_located(
                        (By.ID, xpath))):
                self.driver.find_element(By.ID, xpath).clear()
                self.driver.find_element(By.ID, xpath).send_keys(data)
        except Exception as ee:
            print("Test scenario failed at step: " + inspect.stack()[0][3])
            print("Element locator used: " + xpath)
            raise Exception

    def performClick(self, xp):
        xpath = str(xp)
        try:
            if WebDriverWait(self.driver, self.Time).until(
                    EC.presence_of_element_located(
                        (By.XPATH, xpath))):
                time.sleep(1)
                clickObj = self.driver.find_element(By.XPATH, xpath)
                self.driver.execute_script("arguments[0].click();", clickObj)
        except Exception as ee:
            print("Test scenario failed at step: " + inspect.stack()[0][3])
            print("Element locator used: " + str(xpath))
            raise Exception

    def dropdownByOne(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()
        time.sleep(1)
        action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    def keyUpByOne(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.ARROW_UP).key_up(Keys.ARROW_UP).perform()
        time.sleep(1)
        action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    def dropdownByOneWithoutEnter(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()
        time.sleep(1)

    def scrolldownByOne(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.PAGE_DOWN).perform()
        action.key_up(Keys.PAGE_DOWN).perform()
        time.sleep(1)

    def scrollupByOne(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.PAGE_UP).perform()
        action.key_up(Keys.PAGE_UP).perform()
        time.sleep(1)

    def scrollToElement(self, setup, element):
        self.driver = setup
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def performEnter(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.ENTER).perform()
        action.key_up(Keys.ENTER).perform()
        time.sleep(1)

    def performTab(self, setup):
        self.driver = setup
        action = ActionChains(self.driver)
        action.key_down(Keys.TAB).perform()
        action.key_up(Keys.TAB).perform()
        time.sleep(1)

    def createImage(self, xdata, ydata, data):
        basePath = ReadConfig.basePath()
        path = basePath
        text = path.split("/")
        for t in text:
            if t == ".jenkins":
                print("Running on Jenkins")
                path = os.path.dirname(basePath)
                print("path is " + path)
            else:
                pass
        image_path = path + "/Reports/" + data + ".png"
        plt.figure()
        plt.plot(xdata, ydata, marker='o')
        plt.title('Load Time Report for ' + data)
        plt.xlabel('Iteration')
        plt.ylabel('Load Time (in seconds)')
        plt.legend(['Max Time value: ' + str(round(max(ydata), 2)) + ' s'], loc='upper right')
        plt.grid(True)
        plt.savefig(image_path)
        plt.close()

    def createPDaF(self, ScenarioName, ScenarioTitle, ):
        basePath = ReadConfig.basePath()
        dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
        sheetName_Config = "Config"
        Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
        baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
        ApplicationName = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "ProjectName")

        # --Pdf Report configuration
        ReportHeader = "Testing Report - " + ScenarioName
        ReportIntroduction = ScenarioTitle
        ReportMethodology = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "ReportMethodology")
        output_pdf = ApplicationName.replace(" ", "") + "_"+ScenarioName+"-Output_Report"

        path = basePath
        text = path.split("/")
        for t in text:
            if t == ".jenkins":
                print("Running on Jenkins")
                path = os.path.dirname(basePath)
                print("path is " + path)
                basePath = path
            else:
                pass
        output_file_name = output_pdf
        pdf_path = basePath + "/Reports/" + output_file_name + ".pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        RightSectionSize = 7
        LeftSectionSize = 7

        StartTime = datetime.now()

        # network = speedtest.Speedtest(secure=True)
        # down = network.download() / 1000000
        # up = network.upload() / 1000000
        # best = network.get_best_server()
        # print(f"Found: {best['host']} located in {best['country']}")
        # print("Download Speed: {:.2f} Mbps".format(down))
        # print("Upload Speed: {:.2f} Mbps".format(up))
        # down = "Download Speed: {:.2f} Mbps".format(down)
        # up = "Upload Speed: {:.2f} Mbps".format(up)

        down = "Test"
        up = "Test"

        # --Left side image
        pdf.image('C:/Users/neera/PycharmProjects/UWB2/utilities/BitsInGlassLogo.png', 5, 5,
                       33)  # (path, x, y, width)
        # --Right side image
        # self.pdf.image('C:/Users/neera/PycharmProjects/UWB2/utilities/BitsInGlassLogo.png', 173, 5,
        #                33, 10)  # (path, x, y, width)

        # --Top right side section
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 15, txt=ReportHeader, ln=True, align='C')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Report Timestamp: " + str(
            StartTime.strftime("%m-%d-%Y, %H:%M:%S")) , ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(190, 5, txt="Testing URL: " + baseURL, ln=True, align='R')
        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Testing Environment: " + Env, ln=True, align='R')

        pdf.set_font('Arial', 'B', RightSectionSize)
        pdf.cell(190, 5, txt="Current Network Speed: " + str(up) + " " + str(down), ln=True, align='R')

        # -Setting report Introduction
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Test Introduction", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, ReportIntroduction, 0, 'L')

        # -Setting report Methodology
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Test Methodology", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, ReportMethodology, 0, 'L')

        # -Setting report Summary
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Test Summary", ln=True, align='L')
        pdf.set_font('Arial', '', 10)

        lp1 = testResult()

        finalDic = lp1.testResultMeth("None", "None")

        # for key, value in finalDic:
        dicKeys = list(finalDic.keys())[:200]

        for i in range (1, len(dicKeys)+1):
            pdf.set_text_color(0, 0, 0)
            if str(dicKeys[i-1]) != "None":
                pdf.multi_cell(0, 5, "* "+ str(dicKeys[i-1]), 0, 'L')
                if str(finalDic[dicKeys[i - 1]]) == "Passed":
                    pdf.set_text_color(0, 128, 0)
                elif str(finalDic[dicKeys[i - 1]]) == "Failed":
                    pdf.set_text_color(255, 0, 0)
                pdf.multi_cell(0, 5, " Result: " + str(finalDic[dicKeys[i - 1]]), 0,
                           'L')
                pdf.multi_cell(0, 5, " ", 0, 'L')

        # --Bottom left side section
        pdf.set_font('Arial', 'B', LeftSectionSize)
        pdf.cell(0, 15, txt=" ", ln=True, align='L')
        pdf.cell(0, 5, txt="Note: ", ln=True, align='L')
        pdf.cell(0, 5, txt="1) Python version: 3.11", ln=True, align='L')
        pdf.cell(0, 5, txt="2) Jenkins version: 2.514", ln=True, align='L')
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 5, txt="To understand more about jenkins, click here", ln=True, align='L',
                      link='https://www.jenkins.io/')

        pdf.output(pdf_path)
        print(f"PDF created successfully")
