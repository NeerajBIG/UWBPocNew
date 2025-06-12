import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import zipfile
from utilities.readProperties import ReadConfig
import shutil

class Test_CreateReportZip:
    basePath = ReadConfig.basePath()
    print("Base Path is " + basePath)
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
    ReportFolderName = ReadConfig.getReportFolderName()
    # ScreenshotsFolderName = ReadConfig.getScreenshotFolderName()
    # DataAndReportFolderName = ReadConfig.getDataAndReportFolderName()

    def test_zipfolderReport(self):
        try:
           shutil.make_archive(self.basePath + "/" + self.ReportFolderName, 'zip',self.basePath+"/Reports")
        except:
            pass

    # def test_zipfolderScreenshots(self):
    #     print(self.ScreenshotsFolderName)
    #     try:
    #         shutil.make_archive(self.basePath + "/" + self.ScreenshotsFolderName, 'zip', self.basePath + "/Screenshots")
    #     except:
    #         pass
    #
    # def test_zipfolderDataAndReport(self):
    #     try:
    #         shutil.make_archive(self.basePath+"/"+self.DataAndReportFolderName, 'zip', ReadConfig.basePath()+"/TestData")
    #     except:
    #         pass