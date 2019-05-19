import cv2
import numpy as np
import pytesseract
import os
from pdf2image import convert_from_path
from PIL import Image

l = []
l2 = []
test = 0
dij = 0

f = open("data.json", "w")

detach_dir = '.'
if 'ProcessedImages' not in os.listdir(detach_dir):
    os.mkdir('ProcessedImages')
if 'Converted' not in os.listdir(detach_dir):
    os.mkdir('Converted')


def pick_text(img, x, y, w, h):
    crop_img = img[y:y + h, x:x + w]
    str = pytesseract.image_to_string(crop_img)
    return str


def blocker(filename):
    global l
    global f
    global test
    global dij
    l = []
    x1 = 10
    y1 = 6
    imgo = cv2.imread(filename)
    gray = cv2.cvtColor(imgo, cv2.COLOR_BGR2GRAY)
    linek = np.zeros((11, 11), dtype=np.uint8)
    linek[5, ...] = 1
    x = cv2.morphologyEx(gray, cv2.MORPH_OPEN, linek, iterations=1)
    gray -= x
    gray = cv2.bitwise_not(gray)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    while (True):
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x1, y1))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=6)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        test = len(contours)
        # print(test)
        if (test < 10):
            x1 -= 1
            y1 -= 1
        elif test > 30:
            x1 += 1
            y1 += 1
        else:
            break
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(imgo, (x, y), (x + w, y + h), (0, 255, 0), 2)
        l.append(pick_text(imgo, x, y, w, h))

    s = ''
    s += " ".join(l)
    s = s.replace('"', '')
    s = '{"content":"' + s
    s.replace('\n', ' ')
    s += '"}'
    s = " ".join(s.splitlines())

    f.write(s + '\n')
    cv2.imwrite('./ProcessedImages/final' + str(dij) + '.png', imgo)
    dij += 1


for files in os.listdir("./attachments"):
    if files.endswith(".png") or files.endswith(".jpg") or files.endswith(".jpeg"):
        blocker("./attachments/" + files)

for pdf_file in os.listdir("./attachments"):
    if pdf_file.lower().endswith(".pdf"):
        pages = convert_from_path("./attachments/"+pdf_file, 300)
        pdf_file = pdf_file[:-4]
        for page in pages:
            page.save("./Converted/"+pdf_file + ".png", "PNG")
            blocker("./Converted/"+pdf_file + ".png")
            break

for imageFile in os.listdir("./attachments"):
    if imageFile.lower().endswith(".gif"):
        filepath, filename = os.path.split(imageFile)
        filterame, exts = os.path.splitext(filename)
        print("Processing: " + imageFile, filterame)
        im = Image.open(imageFile)
        im.save("./Converted/"+ filterame + '.png', 'PNG')
        blocker("./Converted/"+filterame + '.png')

f.close()
