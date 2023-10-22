from django.shortcuts import render,HttpResponse
import os
from PyPDF2 import PdfReader, PdfWriter
def extract_pages_to_single_pdf(input_pdf, output_pdf, desired_pages, error):
    # Convert the input and output paths to absolute paths
    # input_pdf = os.path.abspath(input_pdf)
    # output_pdf = os.path.abspath(output_pdf)

    # Open the input PDF file using PdfReader
    pdf = PdfReader(input_pdf)

    # Create a PdfWriter to collect the desired pages into a single PDF
    pdf_writer = PdfWriter()

    # Iterate through the desired pages and add them to the PdfWriter
    for page_num in desired_pages:
        if page_num+error < 1 or page_num+error > len(pdf.pages):
            continue  # Skip invalid page numbers
        pdf_writer.add_page(pdf.pages[page_num+error - 1])  # Page numbers are 0-based

    # Write the collected pages to the output PDF
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

# Create your views here.
def split(request):
    if request.method=="POST":
        error=request.POST.get('error')
        error=int(error)
        numb=request.POST.get('numb')
        result = []
        elements = numb.split(',')
        for element in elements:
            if '-' in element:
                start, end = map(int, element.split('-'))
                result.extend(range(start, end + 1))
            else:
                result.append(int(element))
        input_pdf_file = request.FILES["inputFile"]
        # document=FilesUpload.objects.create(file=input_pdf_file)
        # document.save()
        # return HttpResponse("Uploaded")
        output_pdf_file = './static/output.pdf'
        desired =result
        extract_pages_to_single_pdf(input_pdf_file, output_pdf_file, desired,error)
        variables={
            "error":error,
            "numb":numb,
        }
        print(error,numb)
        print(type(numb[0]))
        return render(request,'out.html',variables)
    return render(request,'form.html')

