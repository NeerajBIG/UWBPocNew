import os, sys
from email.mime.application import MIMEApplication
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from email.message import EmailMessage
import time
import smtplib
from testCases.configTest import setup
from utilities.readProperties import ReadConfig
from utilities import XLUtils
import glob
import shutil
import stat


class Test_HealthCheck:
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    path = basePath + "/TestData/DataAndReport.xlsx"

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


    ReportFolderName = ReadConfig.getIngestionFilesFolderName()
    # files = [ReportFolderName, ScreenshotFolderName, DataAndReportFolderName]
    files = [ReportFolderName]

    MainReportFolderName = ReadConfig.getMainReportFolderName()
    MainScreenshotFolderName = ReadConfig.getMainScreenshotFolderName()
    Mainfiles = [MainReportFolderName, MainScreenshotFolderName]

    path1 = basePath
    text = path1.split("/")
    for t in text:
        if t == ".jenkins":
            print("Running on Jenkins")
            path1 = os.path.dirname(basePath)
            print("path1 is " + path1)
            basePath = path1
        else:
            pass

    def test_HealthCheck(self, setup):
        email_sender = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_From")
        email_password = 'gwgc ioef ymbx yybo'
        email_receiver = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_To")
        subject = XLUtils.readDataConfig(self.path, self.sheetName_Config, "IngestionEmail_Subject")
        body = XLUtils.readDataConfig(self.path, self.sheetName_Config, "IngestionEmail_Body")

        em = EmailMessage()
        em['From'] = email_sender
        print(email_receiver)
        toaddr = email_receiver.split(",")
        em['To'] = ', '.join(toaddr)
        em['subject'] = subject + " - " + time.strftime("%m-%d-%Y")
        em.set_content(body)

        try:

            for f in self.files:
                os.chmod(self.basePath + "/" + f, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                with open(self.basePath + "/" + f , 'rb') as f1:
                    file_data = f1.read()
                em.add_attachment(file_data, maintype='text', subtype='plain', filename=f)

            # for filename in os.listdir(self.basePath + "/" + self.ReportFolderName):
            #     file_path = os.path.join(self.basePath + "/" + self.ReportFolderName, filename)
            #     if os.path.isfile(file_path):
            #         with open(file_path, "rb") as file:
            #             attachment = MIMEApplication(file.read(), Name=filename)
            #             em.attach(attachment)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, em['To'].split(","), em.as_string())
                time.sleep(5)
                print("Email sent ..................")

            # for f in self.files:
            #     os.remove(self.basePath + "/" + f + ".zip")

            # Mainfiles = self.Mainfiles
            # for f1 in Mainfiles:
            #     files = glob.glob(self.basePath + "/" + f1)
            #     for f2 in files:
            #         shutil.rmtree(f2)
            #         pass

            # Mainfiles1 = self.Mainfiles
            # for f2 in Mainfiles1:
            #     os.mkdir(self.basePath + "/" + f2)
            #     pass

        except Exception as e:
            print("Email not sent ..................")
            print(str(e))
            pass
