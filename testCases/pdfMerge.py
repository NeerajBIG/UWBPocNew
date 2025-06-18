from PyPDF2 import PdfMerger

merger = PdfMerger()
pdfs = ['C:/Users/neera/PycharmProjects/UWB2/Reports/UWB1-Output_Report.pdf', 'C:/Users/neera/PycharmProjects/UWB2/Reports/UWB-Output_Report.pdf']

for pdf in pdfs:
    merger.append(pdf)

merger.write("Resulter.pdf")