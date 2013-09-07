from SimpleCV import Image, Color, Features

markupImage = Image("/home/varma/Desktop/markup/markup.jpg")
blobs = markupImage.findBlobs()

rectangles = []
for b in blobs:
    info = b.boundingBox()
    x = info[0]
    y = info[1]
    w = info[2]
    h = info[3]
    markupImage.drawRectangle(x,y,w,h)
while True:
    markupImage.show()




