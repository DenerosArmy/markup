from SimpleCV import Image, Color, Features, cv, cv2, np

def find_color(x,y):
    corner = markupImage.crop(x-2, y-2, 4, 4)
    return corner.meanColor()






markupImage = Image("/home/varma/Desktop/markup/markup.jpg")
blobs = markupImage.findBlobs()

rectangles = []
for b in blobs:
    info = b.boundingBox()
    x = info[0]
    y = info[1]
    w = info[2]
    h = info[3]
    c = find_color(x,y)
    markupImage.drawRectangle(x,y,w,h)
    #c is the rgb tuple of the border of blob b  


while True:
    markupImage.show()





