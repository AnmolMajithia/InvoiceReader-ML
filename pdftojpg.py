from pdf2image import convert_from_path
pages = convert_from_path('p2.pdf', 500)
for page in pages:
    page.save('outf.jpg', 'JPEG')
    break