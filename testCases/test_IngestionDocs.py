import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from email.message import EmailMessage
import time
import smtplib
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from pageObjects.AllElementLocators import ElementLocators


class Test_HealthCheck:
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    path = dataSheetPath

    sheetName_Config = "Config"
    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")

    sheetName_Data = "TestUserData"
    ReportFolderName = ReadConfig.getIngestionFilesFolderName()
    sheetName_Locators = "Locators"

    path1 = basePath
    text = path1.split("/")
    for t in text:
        if t == ".jenkins":
            print("Running on Jenkins")
            path1 = os.path.dirname(basePath)
            print("path1 is " + path1)
            basePath = path1 + "/UWB_test_Ingestion"
        else:
            pass

    def test_HealthCheck(self, setup):
        email_sender = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_From")
        email_password = 'gwgc ioef ymbx yybo'
        email_receiver = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_To")
        subject = XLUtils.readDataConfig(self.path, self.sheetName_Config, "IngestionEmail_Subject")
        body = XLUtils.readDataConfig(self.path, self.sheetName_Config, "IngestionEmail_Body") + self.basePath

        em = EmailMessage()
        em['From'] = email_sender
        print(email_receiver)
        toaddr = email_receiver.split(",")
        em['To'] = ', '.join(toaddr)
        em['subject'] = subject + " - " + time.strftime("%m-%d-%Y")
        em.set_content(body)

        try:
            for (root, dirs, file) in os.walk(self.basePath + "/" + self.ReportFolderName):
                for filename in file:
                    print(filename)
                    with open(self.basePath + "/" + self.ReportFolderName + "/" +filename , 'rb') as f1:
                        file_data = f1.read()
                    em.add_attachment(file_data, maintype='text', subtype='plain', filename=filename)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, em['To'].split(","), em.as_string())
                time.sleep(2)
                print("Email sent ..................")

                #-------Reading data ingestion on Appian frontend application
                # ---------Initiating WebDriver and Launching Application
                self.driver = setup
                self.driver.get(self.baseURL)
                self.lp = ElementLocators(self.driver)
                self.user = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                         "username_" + self.Env)
                self.password = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Data,
                                                             "password_" + self.Env)
                # ---------Entering Username
                self.testStep = "Entering Username"
                try:
                    locator = XLUtils.readDataTestUserData(self.dataSheetPath, self.sheetName_Locators,
                                                           "textbox_username_id")
                    self.lp.inputData(locator, self.user)
                except:
                    self.error = "No web element found, ref: [ " + self.testStep + " ]"
                    raise Exception

                # ---------Entering Password
                self.testStep = "Entering Password"
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

                time.sleep(4)
                for t in range(1,2):
                    print("t is: "+str(t))
                    self.driver.refresh()
                    time.sleep(2)


        except Exception as e:
            print("Email not sent ..................")
            print(str(e))
            pass
