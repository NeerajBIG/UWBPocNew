import datetime
import sys
import time
from os.path import dirname, join, abspath
import wget
from openai import OpenAI

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from github import Github
import streamlit as st
import streamlit as st1
import sys
from os.path import dirname, join, abspath
from pageObjects.AllElementLocators import ElementLocators
from testCases.configTest import setup

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from LLMfunctions import *
import urllib.parse
from streamlit_pdf_viewer import pdf_viewer
import requests
import json


class aaa:
    global df1
    try:
        basePath = ReadConfig.basePath()
        path1 = basePath
        text = path1.split("/")

        basePathGit = ""
        jenkinsCheck = 0
        for t in text:
            if t == ".jenkins":
                print("Running on Jenkins")
                path = os.path.dirname(basePath)
                print("path is " + path)
                basePath = path
                JenkinsJobName = os.getenv("JOB_NAME")
                basePath = basePath + "/" + JenkinsJobName

                basePathGit = basePath.rsplit('/', 1)[0]
                basePathGit = basePathGit + "/ReportsGitTok"
                basePathOpenAI = basePathGit + "/OpenAIToken"

                jenkinsCheck = 1
            else:
                pass

        if jenkinsCheck == 0:
            basePathGit = ReadConfig.basePath()

            basePathGit = basePathGit + "/Configurations"
            basePathOpenAI = basePathGit + "/Configurations"

        with open(basePathGit + "/GitToken.txt", "r") as file:
            content = file.read()
            GITToken = content
        GitToken = GITToken

        with open(basePathGit + "/OpenAIToken.txt", "r") as file:
            content = file.read()
            OpenAIToken = content
        OpenAIToken = OpenAIToken

        dataSheetPath = basePath + "/TestData/DataAndReport.xlsx"

        sheetName_Report = "Report"
        sheetName_Config = "Config"
        sheetName_Data = "TestUserData"
        sheetName_Scenarios = "Scenarios"
        sheetName_WoData = "WorkOrderData"
        sheetName_Locators = "Locators"

        Env = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_ToRun")
        baseURL = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "Env_" + Env + "_URL")
        ApplicationName = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "ProjectName")
        ProjectName = ApplicationName
        EmailRecipients = XLUtils.readDataConfig(dataSheetPath, sheetName_Config, "EmailReport_To")

        ResponseCarryForward = ""

        st.set_page_config(
            page_title=ApplicationName,
            layout="wide"
        )
        st.html("""
            <a href="https://bitsinglass.com/">
            <img src="https://raw.githubusercontent.com/NeerajBIG/ExtraDataBitsinglass/main/BitsInGlassLogo.png" width="150" height="50" ALIGN="CENTER">
            </a>
            """)
        st.header(ProjectName + " Automation code executor")

        #------------------------------------------
        if st.toggle('Run Code Executor / AI Assistant'):
            if st.checkbox('Run ' + ProjectName + ' Regression Test'):
                st.text("Current Environment selected to run the test cases is: " + Env)
                st.text("Environment URL: " + baseURL)
                #st.text("Email Recipients list: " + EmailRecipients)

                person = st.text_input(
                    'To run the test script, please authorize yourself by validate your email address')
                text = EmailRecipients.split(",")
                authorizationChecker = 0
                for index, t in enumerate(text):
                    if t.strip() == person.strip():
                        st.write('Cheers! Your email address verified successfully.')
                        st.write('Please select an option below to run the test case.')
                        authorizationChecker = 1
                        break
                    else:
                        if index == len(text) - 1:
                            if person != "":
                                st.warning(
                                    'Authorization failed. Please send a request and share your email address to be authorized. We will get back to you shortly once your email is added to the list.')
                            else:
                                st.warning('Please enter your email address to validate.')

                if authorizationChecker == 1:
                    scenario_ID = "SC_001"
                    jenkinsBaseUrl = 'http://localhost:8080/buildByToken/build?job='
                    job = 'UWB_HealthCheck'
                    url = jenkinsBaseUrl + job + '&token=bitsinglasstestjobs'

                    AllScenarios = XLUtils.getAllScenarios(dataSheetPath, sheetName_Scenarios)
                    ScenarioDic = {}
                    ScenarioDic1 = {}
                    for index1, t1 in enumerate(AllScenarios.keys()):
                        if "SC" in t1:
                            ButtonName = AllScenarios[t1]
                            ButtonDescription = AllScenarios[ButtonName]

                            url = jenkinsBaseUrl + ApplicationName + "_" + t1 + '&token=bitsinglasstestjobs'

                            ScenarioDic[ButtonName] = ButtonDescription
                            ScenarioDic1[ButtonDescription] = url

                    col = st.columns(len(ScenarioDic.keys()))
                    for index2, t2 in enumerate(ScenarioDic.keys()):
                        urlKey = ScenarioDic[t2]
                        url = ScenarioDic1[urlKey]

                        with st.container(border=True):
                            st.link_button(t2, url)
                            st.write(ScenarioDic[t2])

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

            if st.checkbox('Run ' + ProjectName + ' API Test'):
                API_URL = st.text_input("Enter API end point url")
                # clients = OpenAI(
                #     api_key="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")

                methodType = st.selectbox(
                    "Please select API Method type",
                    ("GET", "POST", "PUT", "PATCH"),
                )

                if methodType == "POST":
                    Client_ID = st.text_input("Enter Client ID")
                    Client_Secret = st.text_input("Enter Client Secret")

                    st.error("Work in Progress....")

                elif methodType == "PUT":
                    st.error("Sorry! This method is not supported.")

                elif methodType == "PATCH":
                    st.error("Sorry! This method is not supported.")

                elif methodType == "GET":
                    st.markdown("""
                        <style>
                        .stButton > button {
                            background-color: #088F8F;
                            color: black;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    if st.button("Run API Test", type="secondary"):

                        if API_URL != "":
                            endpoint = f"{API_URL}"
                            st.text("1111")

                            progress_text = "Hitting API and getting response.."
                            my_bar = st.progress(0, text=progress_text)

                            response = ""
                            for percent_complete in range(100):
                                time.sleep(0.01)
                                my_bar.progress(percent_complete + 1, text=progress_text)

                                if percent_complete > 5:
                                    response = requests.get(endpoint)
                                    if len(response.text) > 0:
                                        st.text(str(len(response.text)))
                                        # time.sleep(1)
                                        my_bar.empty()
                                        break

                            if len(response.text) > 0:
                                # Assertions
                                assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
                                data = response.json()
                                st.text(f"GET request successful for {endpoint}")
                                st.text(f"Response data: {json.dumps(data, indent=2)}")

                            else:
                                st.text("Hitting API and getting response..")
                                pass
                        else:
                            st.error("Base URL cannot be empty")

            elif st.checkbox('Get previous test results'):

                option = st.selectbox('Please choose the application environment', ('QA', 'Staging', 'Preprod', 'Prod'))
                st.write('You selected:', option)

                token = st.text_input("Enter the access token")
                if token == "":
                    st.text(
                        "Token field is empty. Please enter the authorized token to get the test cases list to run.")
                else:
                    try:
                        g = Github(token)
                        repoPath = 'NeerajBIG/ExtraDataBitsinglass'
                        repo = g.get_repo(repoPath)

                        path = "UWB_Reports"
                        # repo.update_file(path=path, message="Updated JMeter Property file", content=data, branch="master",
                        #                  sha=repo.get_contents("testCases/TriForceProp.properties").sha)

                        folderContent = repo.get_contents(path)
                        st.text("")
                        st.text("")
                        st.text("")
                        st.text("Total report files count: " + str(len(folderContent)))

                        # for item in folderContent:
                        #     st.text(item)

                        ReportDates = []
                        ReportNames = []
                        ReportLinksDic = {}
                        for c in folderContent:
                            if ".pdf" in c.name:
                                with st.container(border=True):
                                    ReportDate = c.name.split("_")
                                    ReportDates.append(ReportDate[3])
                                    ReportNames.append(c.name)
                                    ReportLinksDic[c.name] = c.download_url

                        today = datetime.date.today()
                        startD = st.date_input("Choose Report Range Start Date", value=today)
                        endD = st.date_input("Choose Report Range End Date", value=today)

                        start_date = str(startD)
                        end_date = str(endD)

                        ReportAllData = {'Date': ReportDates, 'Value': ReportNames}
                        df = pd.DataFrame(ReportAllData)

                        df['Date'] = pd.to_datetime(df['Date'])
                        filtered_df_range = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

                        #st.text(str(len(filtered_df_range)))

                        if len(filtered_df_range) > 0:
                            df1 = pd.DataFrame(filtered_df_range)
                            first_row = df1.iloc[0]

                        st.text("")
                        st.text("")
                        st.text("")
                        st.text("Total filtered reports count: " + str(len(filtered_df_range)))

                        ExceptionCheck = 0
                        try:
                            print(str(filtered_df_range['Value'][0]))
                        except:
                            ExceptionCheck = 1

                        # st.text(ExceptionCheck)
                        if ExceptionCheck == 1:
                            if pd.to_datetime(start_date) > pd.to_datetime(end_date):
                                st.error("Start Date cannot be greater than end date")
                            else:
                                if len(filtered_df_range) == 0:
                                    st.error("Sorry, no result found")
                                else:
                                    index_FilteredItems = df1[df1['Value'] == filtered_df_range['Value']].index.tolist()
                                    #st.text(index_FilteredItems)

                                    for d in range(index_FilteredItems[0], index_FilteredItems[-1] + 1):
                                        try:
                                            with  st.container(border=True):
                                                file_URL = ReportLinksDic[str(filtered_df_range['Value'][d])]
                                                file_Name = str(filtered_df_range['Value'][d])
                                                text_for_button = 'Click on the button to download the report'

                                                col1, col2 = st.columns([1, 1])
                                                with col1:
                                                    st.link_button(label=file_Name, url=file_URL)
                                                with col2:
                                                    st.text(text_for_button)

                                                if st.checkbox('Display Test Report', key=d):
                                                    try:
                                                        st.set_page_config(layout="wide", page_title=ApplicationName)
                                                        col1, col2 = st.columns([0.4, 0.5], gap="small")

                                                        with col1:
                                                            #st.header("Upload Test Reports PDF File")
                                                            # uploaded_file = st.file_uploader("Please upload your test report pdf document:", type="pdf")

                                                            file_URL = urllib.parse.unquote(file_URL)
                                                            url = file_URL
                                                            wget.download(url,
                                                                          basePath + '/Reports/temp-' + file_Name)
                                                            path = basePath + '/Reports/temp-' + file_Name

                                                            with open(path, 'rb') as pdf_file:
                                                                abc = pdf_file
                                                                pdf_content = pdf_file.read()
                                                                uploaded_file = pdf_content

                                                                root, extension = os.path.splitext(path)

                                                        if uploaded_file is not None:
                                                            FileType = extension
                                                            if FileType == ".pdf":
                                                                with col2:
                                                                    pdf_viewer(input=pdf_content, width=600,
                                                                               height=1000)

                                                                documents = get_pdf_text(uploaded_file)
                                                                st.session_state.vector_store = create_vectorstore_from_texts(
                                                                    documents,
                                                                    api_key=OpenAIToken,
                                                                    file_name=file_Name)
                                                                # Generate answer
                                                                with col1:
                                                                    if st.button("Summarize File", key=file_Name):
                                                                        with st.spinner("Generating answer"):
                                                                            answer = query_document(
                                                                                vectorstore=st.session_state.vector_store,
                                                                                query="Read content of the document. Do not include your suggestion and analysis.",
                                                                                api_key=OpenAIToken)
                                                                            placeholder = st.write(answer)
                                                                os.remove(path)
                                                            else:
                                                                st.rerun()

                                                    except Exception as e11:
                                                        st.error("Exception type 1")
                                                        st.error(str(e11))
                                                        if "got []" in str(e11):
                                                            st.error("File has no text to extract")
                                                            st.error(str(e11))

                                        except Exception as e12:
                                            st.error("Exception type 2")
                                            st.text(str(e12))

                        else:
                            index_FilteredItems = df1[df1['Value'] == filtered_df_range['Value']].index.tolist()
                            #st.text(index_FilteredItems)

                            for d in range(index_FilteredItems[0], index_FilteredItems[-1] + 1):
                                with  st.container(border=True):
                                    file_URL = ReportLinksDic[str(filtered_df_range['Value'][d])]
                                    file_Name = str(filtered_df_range['Value'][d])

                                    text_for_button = 'Click on the button to download the report'
                                    col1, col2 = st.columns([1, 1])
                                    with col1:
                                        st.link_button(label=file_Name, url=file_URL)
                                    with col2:
                                        st.text(text_for_button)

                                    if st.checkbox('Display Test Report', key=d):
                                        try:
                                            st.set_page_config(layout="wide", page_title=ApplicationName)
                                            col1, col2 = st.columns([0.4, 0.5], gap="small")

                                            with col1:
                                                # st.header("Upload Test Reports PDF File")
                                                # uploaded_file = st.file_uploader("Please upload your test report pdf document:", type="pdf")

                                                file_URL = urllib.parse.unquote(file_URL)
                                                url = file_URL
                                                wget.download(url,
                                                              basePath + '/Reports/temp-' + file_Name)
                                                path = basePath + '/Reports/temp-' + file_Name

                                                with open(path, 'rb') as pdf_file:
                                                    abc = pdf_file
                                                    pdf_content = pdf_file.read()
                                                    uploaded_file = pdf_content

                                                    root, extension = os.path.splitext(path)

                                            if uploaded_file is not None:
                                                FileType = extension
                                                if FileType == ".pdf":
                                                    with col2:
                                                        # base64_data = base64.b64encode(pdf_content)
                                                        # base64_string = base64_data.decode('utf-8')
                                                        # pdf_display = F'<iframe src="data:application/pdf;base64,{base64_string}" width="600" height="1000" type="application/pdf"></iframe>'
                                                        # st.markdown(pdf_display, unsafe_allow_html=True)
                                                        pdf_viewer(input=pdf_content, width=600, height=1000)

                                                    documents = get_pdf_text(uploaded_file)
                                                    st.session_state.vector_store = create_vectorstore_from_texts(
                                                        documents,
                                                        api_key=OpenAIToken,
                                                        file_name=file_Name)
                                                    # Generate answer
                                                    with col1:
                                                        if st.button("Summarize File", key=file_Name):
                                                            with st.spinner("Generating answer"):
                                                                answer = query_document(
                                                                    vectorstore=st.session_state.vector_store,
                                                                    query="Read content of the document. Do not include your suggestion and analysis.",
                                                                    api_key=OpenAIToken)
                                                                placeholder = st.write(answer)

                                                    os.remove(path)
                                                else:
                                                    st.rerun()
                                        except Exception as e11:

                                            st.error(str(e11))
                                            if "got []" in str(e11):
                                                st.error("File has no text to extract")
                                                st.error(str(e11))

                    except Exception as e:
                        st.error("Token is invalid. Please enter a valid token to be authorized to run the test cases.")
                        st.text(str(e))

            else:
                agree = st.checkbox(
                    "Any concern? such as 1) Excluding yourself from the list of recipients or 2) Want to be a recipient for the test results? 3) Other Concern. Send a request below")
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
                        st.write(
                            "** Please describe your concern in the body section. We will get back to you shortly.")
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
                                driver = setup
                                lp = ElementLocators(driver)
                                email_sender = ReadConfig.getReportEmailSender()
                                email_password = ReadConfig.getReportPasswordSender()
                                email_receiver = XLUtils.readDataConfig(dataSheetPath, sheetName_Config,
                                                                        "EmailReport_To")
                                ReportFolderName = "None"
                                lp.shareReports(email_sender, email_password, email_receiver, subject, body,
                                                ReportFolderName)
                            except Exception as e:
                                st.error(f"Email not sent, error occurred. Please send an email externally : {e}")

            st.markdown("""
                <style>
                .stButton > button {
                    background-color: #AFE1AF;  /* Change to your desired color */
                    color: black;                /* Change text color */
                }
                </style>
                """, unsafe_allow_html=True)
            if st.button("Reload Page", type="primary"):
                st.rerun()

            st.text("")
            st.text("")
            original_title = '<p style="font-family:Courier; color:Orange; font-size: 10px;">Powered by Streamlit: 1.46.1 , OpenAI: 1.91.0</p>'
            st.markdown(original_title, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 6])
            with col1:
                st.html("""
                        <a href="https://streamlit.io/">
                        <img src="https://raw.githubusercontent.com/NeerajBIG/ExtraDataBitsinglass/main/streamlit.png" width="75" height="35" ALIGN="CENTER">
                        </a>
                        """
                        )
            with col2:
                st.html("""
                        <a href="https://openai.com/">
                        <img src="https://raw.githubusercontent.com/NeerajBIG/ExtraDataBitsinglass/main/openai.png" width="120" height="35" ALIGN="LEFT">
                        </a>
                        """
                        )
        else:
            st1.title("AI Assistant!")
            from datetime import datetime

            client = OpenAI(
                api_key="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")

            # Setting messages in the session
            if "messages" not in st1.session_state:
                st1.session_state.messages = []

            for message in st1.session_state["messages"]:
                with st1.chat_message(message["role"]):
                    st1.markdown(message["content"])

            # initialize model
            full_response = ""
            if "model" not in st1.session_state:
                st1.session_state.model = "gpt-4o-mini"

            # user input
            if user_prompt := st1.chat_input("Your prompt"):
                st1.session_state.messages.append({"role": "user", "content": user_prompt})
                with st1.chat_message("user"):
                    st1.markdown(user_prompt)

                # generate responses
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    for response in client.chat.completions.create(
                            model=st1.session_state.model,
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ],
                            stream=True,
                    ):
                        full_response += response.choices[0].delta.content or ""
                        message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

            StartTime = datetime.now()
            timestamp = str(StartTime.strftime("%m-%d-%Y-%H-%M-%S"))
            FileName = "AI-Response" + timestamp
            clear = "No"
            if full_response != "":
                st.download_button(
                    label="Download Last Response Text",
                    data=full_response,
                    file_name=FileName + ".txt",
                    mime="text/plain"
                )
            if st1.button("Clear Chats"):
                for end in range(1, 3):
                    st1.session_state.messages.clear()
                    st1.rerun()

            #     if st1.button("Clear Chat"):
            #         clear = "Yes"
            #
            # if clear == "Yes":
            #     for end in range(1, 3):
            #         st1.session_state.messages.clear()
            #         st1.rerun()


    except Exception as e11:
        st.error(str(e11))
