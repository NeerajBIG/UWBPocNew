import os
from selenium import webdriver

import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def setup():
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"

    Run_Mode = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Run_Mode")
    print("Run_Mode: ", Run_Mode)

    driver = None
    if Run_Mode == "Local":
        # service = Service()
        # options = webdriver.ChromeOptions()
        # driver = webdriver.Chrome(service=service, options=options)

        # Latest code to automatically download latest chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)


    elif Run_Mode == "Server":
        GridHUB_URL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "GridHUB_URL")
        print("GridHUB_URL: ", GridHUB_URL)
        selenium_grid_url = GridHUB_URL+"/wd/hub"
        driver = webdriver.Remote(options=webdriver.ChromeOptions(), command_executor=selenium_grid_url)

    driver.maximize_window()
    return driver

def pytest_configure(config):
    config._metadata['Project Name'] = 'Test Project'
    config._metadata['Module Name'] = 'Test Module'

@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)
