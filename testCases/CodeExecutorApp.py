from github import Github
import time
import streamlit as st
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from utilities import XLUtils
from utilities.readProperties import ReadConfig
import smtplib
from email.mime.text import MIMEText
from streamlit.components.v1 import html


class aaa:
    ProjectName = "Tricon"
    basePath = ReadConfig.basePath()
    #st.text("basePath is: " + basePath)
    text = basePath.split("/")
    for t in text:
        if t == "mount":
            path = basePath.rsplit('/', 1)[0]
            basePath = path
        else:
            pass
    dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"
    sheetName_Config = "Config"

    Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
    baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
    EmailRecipients = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "EmailReport_To")

    sheetName_Data = "TestUserData"
    sheetName_Report = "Report"
    sheetName_Scenarios = "Scenarios"
    testStep = "Launching Application"

    st.set_page_config(layout="wide")
    st.html("""
        <a href="https://bitsinglass.com/">
        <img src="https://raw.githubusercontent.com/NeerajBIG/ExtraDataBitsinglass/main/BitsInGlassLogo.png" width="150" height="50" ALIGN="CENTER">
        </a>
        """)
    st.header(ProjectName + " Automation code executor")

    #------------------------------------------
    if st.checkbox('Start Over'):
        if st.checkbox('Run Tricon PEGA Regression Test'):
            st.text("Current Environment to run the test cases is: " + Env)
            st.text("Environment URL: " + baseURL)
            #st.text("Email Recipients list: " + EmailRecipients)

            agree = st.checkbox(
                "Any concern such as excluding yourself from the list or want to be a recipient of the test results ? Send a request below")
            if agree == True:
                st.write(
                    "Choose the option below for the request and describe your concern in the body section. You will be contacted shortly.")
                email_sender = "neeraj1wayitsol@gmail.com"
                email_receiver = "neerajpebmaca@gmail.com"

                option = st.selectbox('How can we help?', (
                'Select an option', 'Add email to the recipient list', 'Removing email from recipient list',
                'Other Concerns'))
                st.write('You selected:', option)
                if option == 'Other Concerns':
                    st.write("** Please describe your concern in the body section. We will get back to you shortly.")
                elif option == 'Add email to the recipient list':
                    st.write("** Please mention the email address to include in the body section.")
                elif option == 'Removing email from recipient list':
                    st.write("** Please mention the email address to remove in the body section.")
                subject = option
                body = st.text_area('Body')
                if body == "" or option == 'Select an option':
                    st.warning("Please describe your concern in the body section.")
                else:
                    if st.button("Send Request"):
                        try:
                            msg = MIMEText(body)
                            msg['From'] = email_sender
                            msg['To'] = email_receiver
                            msg['Subject'] = ProjectName + ": Request for " + subject
                            email_password = 'gwgc ioef ymbx yybo'

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(email_sender, email_password)
                            server.sendmail(email_sender, email_receiver, msg.as_string())
                            server.quit()

                            st.success('Email sent successfully! 🚀')

                        except Exception as e:
                            st.error(f"Email not sent, error occurred. Please send an email externally : {e}")

            #st.text(EmailRecipients)
            person = st.text_input('Validate your email address before running scripts.')
            text = EmailRecipients.split(",")
            for index, t in enumerate(text):
                if t.strip() == person.strip():
                    st.write('Cheers! Your email address verified successfully.')
                    st.html("""
                            <H4>Please select an option below to run the test case</H4>
                            """
                            )

                    scenario_ID = "SC_001"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    count = int(scenarioDataList[3])
                    st.text(scenario_ID + ": " + ScenarioTitle + ". Current count is " + str(count))
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_002"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_003"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass
                        pass

                    scenario_ID = "SC_004"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_005"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_006"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_007"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_008"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_009"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_010"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                <script type="text/javascript">
                                    window.open('%s', '_blank').focus();
                                </script>
                            """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_011"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                    <script type="text/javascript">
                                        window.open('%s', '_blank').focus();
                                    </script>
                                """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_012"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                        <script type="text/javascript">
                                            window.open('%s', '_blank').focus();
                                        </script>
                                    """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_013"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                        <script type="text/javascript">
                                            window.open('%s', '_blank').focus();
                                        </script>
                                    """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_014"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                        <script type="text/javascript">
                                            window.open('%s', '_blank').focus();
                                        </script>
                                    """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_015"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                        <script type="text/javascript">
                                            window.open('%s', '_blank').focus();
                                        </script>
                                    """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                    scenario_ID = "SC_016"
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=Test_' + scenario_ID + '&token=bitsinglasstestjobs'
                    scenarioDataList = XLUtils.readDataScenarios(dataSheetPath, sheetName_Scenarios, scenario_ID)
                    ScenarioTitle = scenarioDataList[1]
                    st.text(scenario_ID + ": " + ScenarioTitle)
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = """
                                        <script type="text/javascript">
                                            window.open('%s', '_blank').focus();
                                        </script>
                                    """ % (url)
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass


                else:
                    if index == len(text) - 1:
                        if person != "":
                            st.warning(
                                'Sorry, you are not in the recipient list. Please send request by clicking on the above checkbox to be included in the recipient list. We will get back to you shortly when your email is added to the list.')
                        else:
                            st.warning('Please enter your email address to validate.')

            st.html("""
                    <Br>You will receive an email with test results after the code execution is complete.</Br>
                    <Br>For any questions please contact at <a href="mailto:neeraj.kumar@bitsinglass.com"></Br>
                    neeraj.kumar@bitsinglass.com</a>.

                    <B></B>
                    <B></B>
                    <HR>
                    </BODY>
                    """
                    )

        elif st.checkbox('Run Tricon Appian Load Test'):

            Modules = ["FullTestReadOnly"]
            SelectedModule = st.selectbox("Select Module", Modules)

            Count = st.slider("Select Virtual Users count", 1, 1000)
            st.text("Virtual Users count is: " + str(Count))

            LoopCount = st.slider("Select Loop Count", 1, 100)
            st.text("Loop count is: " + str(LoopCount))

            option = st.selectbox('Please choose the application environment', ('QA', 'Staging', 'Preprod', 'Prod'))
            st.write('You selected:', option)

            token = st.text_input("Enter the access token")
            if token == "":
                st.text("Token field is empty. Please enter the token to run the test cases.")
            else:
                try:
                    g = Github(token)
                    repo = 'NeerajBIG/TriconFSM'
                    repo = g.get_repo(repo)
                    path = "testCases/TriForceProp.properties"

                    #---------QA environment properties----------------
                    data = "QAUsername=Pushp.PO"
                    data = data + '\n' + "QAPassword=testrules@987"
                    data = data + '\n' + "QAUrl=tahtest.appiancloud.com"

                    # ---------Staging environment properties----------------
                    data = data + '\n' + "StagingUsername=Pushp.PO1"
                    data = data + '\n' + "StagingPassword=testrules@9871"
                    data = data + '\n' + "StagingUrl=tahdev.appiancloud.com"

                    data = data + '\n' + "threadcount=" + str(Count)
                    data = data + '\n' + "loopcount=" + str(LoopCount)
                    data = data + '\n' + "Project=" + ProjectName
                    data = data + '\n' + "Environment=" + option
                    data = data + '\n' + "Application=" + ProjectName + "Appian"

                    repo.update_file(path=path, message="Updated JMeter Property file", content=data, branch="master",
                                     sha=repo.get_contents("testCases/TriForceProp.properties").sha)
                    time.sleep(2)

                    scenario_ID = SelectedModule
                    url = 'https://7965-13-54-100-122.ngrok-free.app/buildByToken/build?job=' + scenario_ID + '&token=bitsinglasstestjobs'
                    if 'button' not in st.session_state:
                        st.session_state.button = False

                    def open_page(url):
                        st.session_state.button = not st.session_state.button
                        open_script = ("""<script type="text/javascript">window.open('%s', '').focus();
                        </script>
                        """
                                       % (url))
                        html(open_script)

                    st.button('Run Test Case: ' + scenario_ID, on_click=open_page, args=(url,))
                    if st.session_state.button:
                        time.sleep(2)
                        st.session_state.button = False
                        st.rerun()
                    else:
                        pass

                except Exception as e:
                    st.error("Token is invalid. Please enter a valid token to run the test cases.")
                    #st.text(str(e))
            t = "None"
            if st.checkbox('List Buttons for all Graphs'):
                for t in Modules:
                    #st.text(str(t))
                    pass
                if t == Modules[0]:
                    st.link_button(Modules[0],
                               "https://4162-13-54-100-122.ngrok-free.app/d/qzGpZBdVz/jmeter-performance-testing-dashboard?orgId=1&from=1728154957480&to=1728156757480&var-bucket=Tricon&var-application=TriconAppian&var-measurement=Tricon-QA&var-Environment=QA&var-transaction=Navigating+to+all+Sections", )

    if st.button("Reload Page", type="primary"):
        st.rerun()
