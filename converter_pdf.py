# import module
from pdf2image import convert_from_path

path = input("Enter path to pdf file: ")
# Store Pdf with convert_from_path function
images = convert_from_path(path)

for i in range(len(images)):
    # print(type(images[i]))
    images[i].save(path[:-4] + '_page'+ str(i) +'.jpg', 'JPEG')
