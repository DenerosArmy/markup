from __future__ import division
import argparse 
import math
from SimpleCV import Image, Color, Features
from collections import namedtuple
import os
import numpy
DEBUG = 0
Rectangle =  namedtuple('rectangle', ['x', 'y', 'w', 'h', 'r', 'g', 'b', 'type', 'subshapes'])
WebRectangle  = namedtuple('webrectangle', ['x', 'y', 'w', 'h', 'type','subshapes']) 
Grid = namedtuple('grid', ['x','y', 'origin', 'end'])
Point = namedtuple('point', ['x','y'])

def find_shapes(img):
    markupImage = Image(img)
    bwImage = markupImage.binarize() 
    blobs = bwImage.findBlobs()
    rectangles = [] 
    for b in blobs:
        info = b.boundingBox()
        x = info[0]
        y = info[1]
        w = info[2]
        h = info[3]
        c = find_color(x, y, markupImage)
        markupImage.drawRectangle(x, y, w, h)
        rectangles.append(Rectangle(x,y,w,h,c[0], c[1], c[2],"text",[]))
    if DEBUG:
	max_rectangle = max(rectangles, key=lambda rect: rect.w * rect.h) 
   	markupImage.drawRectangle(max_rectangle.x, max_rectangle.y, max_rectangle.w, max_rectangle.h, Color.ORANGE) 
    return rectangles, markupImage 

def grid_transform(info):
    max_rectangle = max(info[0], key=lambda rect: rect.w * rect.h)
    info[0].remove(max_rectangle) 
    img = info[1]
    origin = Point(max_rectangle.x, max_rectangle.y)
    end = Point(max_rectangle.x + max_rectangle.w, max_rectangle.y + max_rectangle.h)
    gridx = int(math.ceil(max_rectangle.w/14))
    gridy = int(math.ceil(max_rectangle.h/9))
    grid = Grid(gridx, gridy, origin, end) 
    
    web_rects= classify_rect(info, grid)
    return web_rects, img

def classify_rect(info, grid):
    rects = info[0]
    img = info[1]
    
    mid_rects =[]
    #need to fix for TRIANGLE SUBSHAPE DETECTION
    for i, rect in enumerate(rects): 
	subshapes = find_subshapes(rects,rect)
        if (len(subshapes) == 0):
	    cc= rect[0:4]
	    a = img.crop(cc)
	    a.save('f{0}.jpg'.format(i))  
            shape = "triangle"
	else:
	    shape = "none"
	mid_rects.append(Rectangle(rect[0], rect[1], rect[2], rect[3],0,0,0, shape, subshapes))
    
    web_coord_rects = []
    for mrect in mid_rects:
        coords = transform_rect(mrect, grid)
        x = coords[0].x
        y = coords[0].y
        w = abs(coords[0].x - coords[1].x)
        h = abs(coords[0].y - coords[1].y)
        web_coord_rects.append(WebRectangle(x,y,w,h,"text",mrect.inside))

    web_rects = []
    _type = "text"
    for wcrect in web_coord_rects:
	for s in wcrect.inside:
	    if ((s.type == "triangle") and (len(wcrect.inside) == 1)):
		_type = "image"
	web_rects.append(WebRectangle(wcrect[0], wcrect[1], wcrect[2], wcrect[3], _type, wcrect.inside))
    return web_rects   

def detect_triangle(img):
    c = img.findCorners(10,.5)
    if len(c) == 3:
	return True

    return False
       

 
#ONLY FOR TESTING AND DRAWING PURPOSES
def analyze_shapes(info):
    img = info[1]
    max_rectangle = max(info[0], key=lambda rect: rect.w * rect.h)
    info[0].remove(max_rectangle)

    for r in info[0]:
	sub = find_subshapes(info[0], r)
        img.drawRectangle(r.x, r.y, r.w, r.h, Color.BLUE)
        for s in sub:
            img.drawRectangle(s.x, s.y, s.w, s.h)
    return image
         
 
def find_subshapes(rectangles, rect):
    subshapes = []
    for r in rectangles:
	if ((~(rect == r)) and (includes(r,rect))):
	    subshapes.append(r)
    return subshapes

def includes(shape, rectangle):
    if ((shape.x > rectangle.x) and (shape.y > rectangle.y) and (shape.w < rectangle.w) and (shape.h < rectangle.h)):
	return True
    else:
        return False

	    
def transform_rect(rect, grid):
    '''Takes rectangle on paper and transforms it into a web rectangle with certain 
    properties'''
     
    #_type = "text"
    upper_corner = transform_point(Point(rect.x, rect.y), grid) 
    lower_corner = transform_point(Point(rect.x + rect.w, rect.y + rect.h), grid) 
    return upper_corner, lower_corner
#return WebRectangle(upper_corner.x, upper_corner.y, abs(upper_corner.x - lower_corner.x),
                 #abs(upper_corner.y - lower_corner.y), _type , [])

    
def transform_point(point, grid):
    up_x = int(math.ceil((point.x + grid.origin.x)/grid.x))
    down_x = int((point.x + grid.origin.x)/grid.x)
    if abs(point.x - up_x) >= abs(point.x - down_x): 
        new_x = down_x
    else:
        new_x = up_x
    up_y = int(math.ceil((point.y + grid.origin.y)/grid.y))
    down_y = int((point.y + grid.origin.y)/grid.y)
    if abs(point.y - up_y) >= abs(point.y - down_y): 
        new_y = down_y
    else:
        new_y = up_y
    return Point(new_x, new_y)

     
def draw_grid(image, grid):
    for i, x in enumerate(range(grid.origin.x, grid.end.x, grid.x)):
        for j, y in enumerate(range(grid.origin.y, grid.end.y, grid.y)):
            image.drawRectangle(x, y, grid.x, grid.y, Color.GREEN)
    return image 
    
def analyze_color(rect, markupImage):
    red_image = markupImage - markupImage.colorDistance(Color.RED)
    green_image = markupImage - markupImage.colorDistance(Color.GREEN)
    blue_image  = markupImage - markupImage.colorDistance(Color.BLUE)
    find_color(rect[0], rect[1], red_image, green_image, blue_image)   

def find_color(x,y, red, green, blue):
    redimg = red.crop(x,y,5,5)
    greenimg = green.crop(x,y,5,5)
    blueimg = blue.crop(x,y,5,5)
    redlevel = redimg.meanColor()
    greenlevel = greenimg.meanColor()
    bluelevel = blueimg.mean color()
    if max(max(bluelevel), max(redlevel), max(greenlevel)) > 0.5:
	color = max([bluelevel, redlevel, greenlevel], key=max)
	if color == greenlevel:
		return "green"
	elif color == redlevel:
		return "red"
	else:
		return "blue"
    else:
	return "black"



















if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Please enter an image to be analyzed")    
    parser.add_argument('image', type=str,
                               help='path to image to be analyzed')
    args = parser.parse_args()
    #shapes = find_shapes(os.path.abspath(args.image))
    #image = grid_transform(shapes)
    img = Image("markup.jpg")
    blob = img.findBlobs()
    for b in blob:
	info = b.boundingBox()
	analyze_color((info[0], info[1], info[2], info[3]), img)
    while True: 
        img.show()


