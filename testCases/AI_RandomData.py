import os
import sys
import time
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from openai import OpenAI
from utilities.readProperties import ReadConfig


class Test_Data_Generator:

    def test_generate_random_data_with_ai(self, data_type):
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

        with open(basePathGit + "/OpenAIToken.txt", "r") as file:
            content = file.read()
            OpenAIToken = content

        #data_type = "email"
        data_type = data_type.lower()

        'provide unique data in the same order as given in the list ("First Name", "Phone", "Email", "First Name") 2 times in python list format.'
        if data_type == 'name':
            prompt = "Generate a single unique random name. It should be first name only. Do not add any other text. Only show First name."

        elif data_type == 'phone':
            prompt = "Generate a single random phone numbers in a realistic format. Do not add any other text. Only show phone number in US format. DO not use display character other than numbers."

        elif data_type == 'email':
            prompt = "Generate a single random email address. Do not add any other text. Only show email address."

        elif data_type == 'address':
            prompt = "Generate a single random address from US. House number, street name, city and state should be comma separated."

        else:
            return "Unsupported data type"

        response_text = ""
        client = OpenAI(api_key=OpenAIToken)

        for response  in client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
        ):
            response_text += response.choices[0].delta.content or ""

        if response_text != "":
            #print(response_text)
            return response_text
