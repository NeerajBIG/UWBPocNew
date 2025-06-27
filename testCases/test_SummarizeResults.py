import sys
from os.path import dirname, join, abspath
import PyPDF2
from openai import OpenAI
sys.path.insert(0, abspath(join(dirname(__file__), '..')))


class Test_SummarizeResult:
    dic = {}

    def test_SummarizeResultMeth(self):
        client = OpenAI(api_key='')
        pdf_file = open("text.pdf", "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_summary  = "None"
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            print(page_text)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role":"system",
                        "content":"You are a helpful research assistant."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this: {page_text}"
                    }
                ]
            )
            page_summary = response.choices[0].message.content
        print(page_summary)