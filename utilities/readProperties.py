import configparser
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

class ReadConfig:
    path = os.path.dirname(os.path.abspath(__file__))
    path = path.rsplit('\\', 1)[0]
    path = path.replace('\\', '/')
    config = configparser.RawConfigParser()
    config.read(path+"/Configurations/config.ini")

    @staticmethod
    def getReportFolderName():
        FolderName = ReadConfig.config.get('common data','ReportFolderName')
        return FolderName

    @staticmethod
    def getScreenshotFolderName():
        FolderName = ReadConfig.config.get('common data', 'ScreenshotFolderName')
        return FolderName

    @staticmethod
    def getDataAndReportFolderName():
        FolderName = ReadConfig.config.get('common data', 'TestDataFolderName')
        return FolderName

    @staticmethod
    def basePath():
        return ReadConfig.path

    @staticmethod
    def getWaitTimeForEachElement():
        Time = ReadConfig.config.get('common data', 'WaitTimeForEachElement')
        return Time

    @staticmethod
    def getMainScreenshotFolderName():
        FolderName = ReadConfig.config.get('common data', 'MainScreenshotFolderName')
        return FolderName

    @staticmethod
    def getMainReportFolderName():
        FolderName = ReadConfig.config.get('common data', 'MainReportFolderName')
        return FolderName

    @staticmethod
    def getIngestionFilesFolderName():
        FolderName = ReadConfig.config.get('common data', 'IngestionFilesFolderName')
        return FolderName