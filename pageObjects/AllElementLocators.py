import os, sys
from os.path import dirname, join, abspath
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
            # start_time = time.time()
            # loopCounter = 5
            # for item in range (0, loopCounter):
            #     if time.time() - start_time > 5:
            #         print("Loop timed out")
            #         break
            #     try:
            #         self.driver.find_element(By.XPATH, "//div[@class='SailContainerWeb---sailcontents appian-context-browser-chrome appian-context-os-windows appian-context-ux-responsive' and @id='sitesBody']").is_displayed()
            #         print("********************Loader exist******************")
            #         break
            #     except Exception as ee1:
            #         print("Not present" + str(ee1))
            #     print(item)
            #     time.sleep(0.5)
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

    def createPDF(self, ele_name, descrp, file_name):
        pdf = FPDF()
        textHeight = 5
        posX = 10
        posY = 10
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        basePath = ReadConfig.basePath()
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
        output_file_name = file_name
        pdf_path = basePath + "/Reports/" + output_file_name + ".pdf"

        pdf.set_font('Arial', 'B', 12)
        #---------Adding Title to the PDF
        pdf.cell(0, posX, 'Tricon - Load Time Report - Env: ' + self.Env + ' Generated on ' + str(
            datetime.now().strftime("%m/%d/%Y T%H:%M")), 0, 1, 'C')
        var = 0

        imageHeight = 0
        count = len(ele_name)
        for i in range(count):
            lineMultiple = len(descrp[i]) // 128
            if i == 0:
                var = var + 10
            else:
                if (i % 2) == 0:
                    pdf.add_page()
                    var = 10
                else:
                    var = imageHeight + var + 10

            #image_path = basePath + "/Reports/" + ele_name[i] + ".png"
            image_path = "C:/Users/neera/PycharmProjects/TriconFSM/utilities/BitsInGlassLogo.png"

            pdf.set_xy(posX, posY + var)
            #---------Adding Content above the graph in the PDF
            body = str(i + 1) + ") " + descrp[i]
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, textHeight, body)

            var = var + 10
            if lineMultiple > 1:
                var = var + (lineMultiple * 5)
            pdf.set_xy(posX, posY + var)
            #---------Adding Graph image to the PDF
            image_width = 120
            page_width = pdf.w - 2 * pdf.l_margin
            center_x = (page_width - image_width) / 2
            pdf.image(image_path, x=center_x + 7, y=posY + var, w=image_width)
            imageHeight = 90

        pdf.output(pdf_path)
