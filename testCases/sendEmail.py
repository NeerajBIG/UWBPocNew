import os, sys
import shutil
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import time
from email.message import EmailMessage
import smtplib
import glob
from utilities import XLUtils
from utilities.readProperties import ReadConfig

class Test_SendEmail:
    basePath = ReadConfig.basePath()
    path = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"
    ReportFolderName = XLUtils.readDataConfig(path, sheetName_Config, "EmailReport_FolderName")
    # ScreenshotFolderName = ReadConfig.getScreenshotFolderName()
    # DataAndReportFolderName = ReadConfig.getDataAndReportFolderName()
    #files = [ReportFolderName, ScreenshotFolderName, DataAndReportFolderName]
    files = [ReportFolderName]

    # MainReportFolderName = ReadConfig.getMainReportFolderName()
    # MainScreenshotFolderName = ReadConfig.getMainScreenshotFolderName()
    # Mainfiles = [MainReportFolderName, MainScreenshotFolderName]

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

    def test_sendemail(self):
        email_sender = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_From")
        email_password = 'gwgc ioef ymbx yybo'
        email_receiver = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_To")
        subject = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_Subject")
        body = XLUtils.readDataConfig(self.path, self.sheetName_Config, "EmailReport_Body")

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
                    with open(self.basePath + "/" + self.ReportFolderName + "/" + filename, 'rb') as f1:
                        file_data = f1.read()
                    em.add_attachment(file_data, maintype='text', subtype='plain', filename=filename)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, em['To'].split(","), em.as_string())
                time.sleep(2)

                print("Email sent ..................")

        except Exception as e:
            print("Email not sent ..................")
            print(str(e))
            pass
