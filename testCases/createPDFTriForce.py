import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from utilities.readProperties import ReadConfig
from datetime import datetime
from fpdf import FPDF
import tzlocal
from utilities import XLUtils
from pyjavaproperties import Properties
import speedtest

class createPDFcl:
    ApplicationName = "TriForce"
    basePath = ReadConfig.basePath()
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"
    Env = XLUtils.readDataConfigTriForce(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfigTriForce(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")

    p = Properties()
    p.load(open(basePath + '/testCases/TriForceProp.properties'))
    p.list()
    ThreadCount = p['threadcount']
    PropertiesCount = p['propertiescount']
    cloudstorage = p['clouddatastorgae']

    # --Pdf Report configuration
    ReportHeader = "Performance Testing Report - " + ApplicationName
    ReportIntroduction = "The objective of performance testing is to evaluate how " + ApplicationName + " application performs under various conditions, such as different concurrent user loads, data load, and network. It aims to identify potential bottlenecks, performance issues, and system vulnerabilities that could affect user experience, reliability, or scalability. By simulating real-world traffic and usage scenarios, performance testing helps ensure that the system can handle the expected number of concurrent users, process transactions efficiently, and maintain stability under peak loads."
    ReportMethodology = "The test methodology used in this performance test focusing on page load time to measure how quickly a web page loads at different section under various conditions, including different network speeds and user traffic loads. By analyzing the page load times across different sections of the application, the testing aims to pinpoint areas of optimization, such as server response time, content delivery, and front-end performance, ensuring that the page loads efficiently and provides a seamless user experience."
    ReportKeyFindings = "Please observe the load time (Front End) marked in red color in following tables. An ideal page load time is between 0-3 seconds, 4 seconds is also considered to be an acceptable score. Anything above 4 seconds should be investigated and improved."
    LoadTimeThreshold = 4
    output_pdf = ApplicationName + "-Output_Report.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    RightSectionSize = 7
    LeftSectionSize = 7

    def headerPDF(self):
        StartTime = datetime.now()

        network = speedtest.Speedtest(secure=True)
        down = network.download() / 1000000
        up = network.upload() / 1000000

        best = network.get_best_server()
        print(f"Found: {best['host']} located in {best['country']}")
        print("Download Speed: {:.2f} Mbps".format(down))
        print("Upload Speed: {:.2f} Mbps".format(up))
        down = "Download Speed: {:.2f} Mbps".format(down)
        up = "Upload Speed: {:.2f} Mbps".format(up)
        # down = "Test"
        # up = "Test"

        self.pdf.image('C:/Users/neera/PycharmProjects/TriconFSM/utilities/BitsInGlassLogo.png', 5, 5,
                       33)  # (path, x, y, width)
        self.pdf.image('C:/Users/neera/PycharmProjects/TriconFSM/utilities/TriconResidentialLogo.png', 173, 5,
                       33, 10)  # (path, x, y, width)

        # -Setting report header text in the center of the page
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(200, 15, txt=self.ReportHeader, ln=True, align='C')

        RightSectionSize = self.RightSectionSize
        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.cell(190, 5, txt="Report Timestamp: " + str(
            StartTime.strftime("%m-%d-%Y, %H:%M:%S")) + " " + tzlocal.get_localzone_name(), ln=True, align='R')

        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.set_text_color(0, 0, 255)
        self.pdf.cell(190, 5, txt="Testing URL: " + self.baseURL, ln=True, align='R')
        self.pdf.set_text_color(0, 0, 0)

        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.cell(190, 5, txt="Testing Environment: " + self.Env, ln=True, align='R')

        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.cell(190, 5, txt="Current Network Speed: " + str(up) + " " + str(down), ln=True, align='R')

        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.cell(190, 5, txt="Virtual User Count: " + str(self.ThreadCount), ln=True, align='R')

        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.cell(190, 5, txt="Current Properties Count = " + str(self.PropertiesCount), ln=True, align='R')

        self.pdf.set_font('Arial', 'B', RightSectionSize)
        self.pdf.cell(190, 5, txt="Cloud Data Storage: " + str(self.cloudstorage), ln=True, align='R')

        # -Setting report Objective
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, "Test Objective", ln=True, align='L')
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 5, self.ReportIntroduction, 0, 'L')

        # -Setting report Methodology
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, "Test Methodology", ln=True, align='L')
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 5, self.ReportMethodology, 0, 'L')

        # -Setting report Key Findings
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, "Key Findings", ln=True, align='L')
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 5, self.ReportKeyFindings, 0, 'L')

    def createPDF(self, section_name, data_value, data_array, link_value):
        RightSectionSize = self.RightSectionSize
        # ---------------------------------Setting report Section - Tasks-----------------------------------
        self.pdf.multi_cell(0, 5, '\n')
        SectionName = section_name
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.multi_cell(0, 10, "Performance metrics for: " + SectionName)

        # -Setting report Header Section Values
        header = ['Test Step', 'Attempt #', 'Front End Load Time (s)', 'Server Load Time (s)']
        data = data_value
        link = link_value
        print(" ")
        if data is not "None":
            self.pdf.set_font('Arial', '', 6)
            self.pdf.set_text_color(0, 0, 255)
            if link is not "None":
                self.pdf.cell(0, 5, data, link=link)
                self.pdf.multi_cell(0, 5, "")
            else:
                self.pdf.multi_cell(0, 5, data)
            self.pdf.set_text_color(0, 0, 0)
            data = None

        self.pdf.set_font('Arial', 'B', 10)
        for idx, item in enumerate(header):
            if idx == 0:
                self.pdf.cell(75, 10, item, 1, 0, 'C')
            elif idx == 1:
                self.pdf.cell(22, 10, item, 1, 0, 'C')
            else:
                self.pdf.cell(47, 10, item, 1, 0, 'C')
        self.pdf.ln()
        # Table Body
        self.pdf.set_font('Arial', '', 10)
        data1 = data_array
        for row in data1:
            for idx2, item in enumerate(row):
                self.pdf.set_text_color(0, 0, 0)
                self.pdf.set_font('Arial', '', 10)
                if idx2 == 0:
                    self.pdf.cell(75, 10, item, 1, 0, 'C')
                elif idx2 == 1:
                    self.pdf.cell(22, 10, item, 1, 0, 'C')
                elif idx2 == 2:
                    print("item value is " + item)
                    if float(item) > self.LoadTimeThreshold:
                        self.pdf.set_text_color(255, 0, 0)
                        self.pdf.set_font('Arial', 'B', 10)
                    self.pdf.cell(47, 10, item, 1, 0, 'C')
                else:
                    self.pdf.cell(47, 10, item, 1, 0, 'C')
            self.pdf.ln()

    def footerPDF(self):
        LeftSectionSize = self.LeftSectionSize
        self.pdf.set_font('Arial', 'B', LeftSectionSize)
        self.pdf.cell(0, 15, txt=" ", ln=True, align='L')
        self.pdf.cell(0, 5, txt="Note: ", ln=True, align='L')
        self.pdf.cell(0, 5, txt="1) Python version: 3.9", ln=True, align='L')
        self.pdf.cell(0, 5, txt="2) JMeter version: apache-jmeter-5.5", ln=True, align='L')
        self.pdf.cell(0, 5, txt="3) JMeter Thread Count: Virtual User Count as given above", ln=True, align='L')
        self.pdf.cell(0, 5, txt="4) JMeter Ramp-up Period(in seconds): 1", ln=True, align='L')
        self.pdf.set_text_color(0, 0, 255)
        self.pdf.cell(0, 5, txt="To understand more about JMeter, click here", ln=True, align='L',
                      link='https://jmeter.apache.org/')

    def EndPDF(self):
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
        # -Creating PDF output file
        self.pdf.output(self.basePath + "/Reports/" + self.output_pdf)
        print(f"PDF created successfully: {self.output_pdf}")
