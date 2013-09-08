from __future__ import division
import argparse 
import math
from SimpleCV import Image, Color, Features
from recordtype import recordtype
import numpy
import os
DEBUG = 1
Rectangle =  recordtype('rectangle', ['x', 'y', 'w', 'h', 'color', 'shape', 'parent'])
WebRectangle  = recordtype('webrectangle', ['x', 'y', 'w', 'h', 'shape', 'children', 'parent', 'box_type']) 
colors = [Color.YELLOW, Color.HOTPINK, Color.CYAN, Color.RED, Color.BLUE, Color.GREEN]
Grid = recordtype('grid', ['x','y', 'origin', 'end'])
Point = recordtype('point', ['x','y'])

def find_shapes(img, i):
    markupImage = img
    bwImage = markupImage.binarize(i)
    blobs = bwImage.findBlobs()
    rectangles = [] 
    for b in blobs:
        info = b.boundingBox()
        x = info[0]
        y = info[1]
        w = info[2]
        h = info[3]
        #markupImage.drawRectangle(x, y, w, h)
        r = Rectangle(x, y, w, h, "black", 0, None)
        r.color = analyze_color(r, markupImage)
	rectangles.append(r)
    if DEBUG:
        max_rectangle = max(rectangles, key=lambda rect: rect.w * rect.h) 
        markupImage.drawRectangle(max_rectangle.x, max_rectangle.y, max_rectangle.w, max_rectangle.h, Color.ORANGE) 
    return rectangles, max_rectangle
 
def best_detection(img):
    img = Image(img)
    included = True
    rects = []

    for i in range (20,100,10):
	if not included:
		included = True
		continue


        info = find_shapes(img, i)
	rects = info[0]
	maxrect = info[1]
	for rect in rects:
		if (~inside(maxrect, rect)):
		    included = False
		    break
	if included == True:
	    print i
	    print rects
	    return rects, img
    return rects, img
	
def grid_transform(info):
    rects, img = info 
    max_rectangle = max(rects, key=lambda rect: rect.w * rect.h)
    rects.remove(max_rectangle) 
    rects.sort(key=lambda rect: -1 * rect.w * rect.h)  
    find_rects_metadata(rects, img)
    origin = Point(max_rectangle.x, max_rectangle.y)
    end = Point(max_rectangle.x + max_rectangle.w, max_rectangle.y + max_rectangle.h)
    gridx = int(math.ceil(max_rectangle.w/14))
    gridy = int(math.ceil(max_rectangle.h/9))
    grid = Grid(gridx, gridy, origin, end)  
    web_rects = [] 
    for rect in rects:
        web_rects.append(transform_rect(rect, grid))
    find_webrects_metadata(rects, web_rects) 
    draw_web_rects(img, web_rects, grid) 
    return list(filter(lambda rect: rect.w != 0 and rect.h != 0, web_rects)), img

def find_rects_metadata(rects, img):
    for i, rect in enumerate(rects):
        parent = None 
        for j in range(i, -1, -1):
            if inside(rect, rects[j]):  
                rect.parent = rects[j]
                break     
        rect.shape = get_type(rect, img)

def find_webrects_metadata(rects, webrects):
    for i, webrect in enumerate(webrects): 
        webrect.box_type = imagetonum(rects[i].color)
	if (rects[i].parent):
            index = rects.index(rects[i].parent)
            parent = webrects[index]
            webrect.parent=parent 
    for rect in webrects:
        if rect.parent:
            if rect.shape: 
                rect.parent.box_type = 1
                rect.box_type = 2
            rect.parent.children.append(rect) 

def imagetonum(str):
    print str
    if str == "red":
	return 3
    elif str == "green":
	return 4
    elif str == "blue":
	return 5
    else:
	return 0

    
def get_type(rect, img):
    cropped =  img.crop(rect.x, rect.y, rect.w, rect.h)
    corners = cropped.findCorners(minquality=0.7) 
    print len(corners)
    if len(corners) == 3: 
        return 1 
    else:
        return 0 

       
 
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
	if ((~(rect == r)) and (inside(r,rect))):
	    subshapes.append(r)
    return subshapes

def inside(shape, rectangle):
    if ((shape.x > rectangle.x) and (shape.y > rectangle.y) and (shape.w < rectangle.w) and (shape.h < rectangle.h)):
	return True
    else:
        return False
 
def transform_rect(rect, grid):
    '''Takes rectangle on paper and transforms it into a web rectangle with certain 
    properties'''
     
    upper_corner = transform_point(Point(rect.x, rect.y), grid) 
    lower_corner = transform_point(Point(rect.x + rect.w, rect.y + rect.h), grid) 
    print lower_corner
    return WebRectangle(upper_corner.x, upper_corner.y, abs(upper_corner.x - lower_corner.x),
                 abs(upper_corner.y - lower_corner.y), rect.shape , [], None, 0)

    
def transform_point(point, grid):
    up_x = int(math.ceil((point.x - grid.origin.x)/grid.x))
    down_x = int((point.x - grid.origin.x)/grid.x)
    if abs(point.x - up_x) >= abs(point.x - down_x): 
        new_x = down_x
    else:
        new_x = up_x
    if new_x < 0:
        new_x = 0
    if new_x >= 14:
        new_x = 13
    up_y = int(math.ceil((point.y - grid.origin.y)/grid.y))
    down_y = int((point.y - grid.origin.y)/grid.y)
    if abs(point.y - up_y) >= abs(point.y - down_y): 
        new_y = down_y
    else:
        new_y = up_y
    if new_y >= 9:
        new_y = 8
    if new_y < 0:
        new_y = 0
    return Point(new_x, new_y)

     
def draw_grid(image, grid):
    for i, x in enumerate(range(grid.origin.x, grid.end.x, grid.x)):
        for j, y in enumerate(range(grid.origin.y, grid.end.y, grid.y)):
            image.drawRectangle(x, y, grid.x, grid.y, Color.GREEN)
    return image 

def draw_web_rects(image, web_rects, grid):
    for rect in web_rects: 
        a_x  = rect.x * grid.x + grid.origin.x
        a_y  = rect.y * grid.y  + grid.origin.y
        a_w =  grid.x * rect.w 
        a_h =  grid.y * rect.h
        image.drawRectangle(a_x, a_y, a_w, a_h, colors[rect.box_type]) 
    return image
    
def analyze_color(rect, markupImage):
    red_image = markupImage - markupImage.colorDistance(Color.RED)
    green_image = markupImage - markupImage.colorDistance(Color.GREEN)
    blue_image  = markupImage - markupImage.colorDistance(Color.BLUE)
    return find_color(rect.x, rect.y, red_image, green_image, blue_image)   


def find_color(x,y, red, green, blue):
    redimg = red.crop(x,y,5,5)
    greenimg = green.crop(x,y,5,5)
    blueimg = blue.crop(x,y,5,5)
    redlevel = redimg.meanColor()
    greenlevel = greenimg.meanColor()
    bluelevel = blueimg.meanColor()
    if max(max(bluelevel), max(redlevel), max(greenlevel)) > 0.3:
        color = max([bluelevel, redlevel, greenlevel], key=max)
        if color == greenlevel:
            return "green"
        elif color == redlevel:
            return "red"
        elif color == bluelevel:
            return "blue"
    return "black"
        
def analyze(img):
    return grid_transform(best_detection(img))

def get_rows(webrectangles, img):
    rows = [[] for i in range(9)] 
    for rect in webrectangles:
        rows[rect.y].append(rect) 
    return rows 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Please enter an image to be analyzed")    
    parser.add_argument('image', type=str,
                               help='path to image to be analyzed')
    args = parser.parse_args()
    print(analyze(args.image))

