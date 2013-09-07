from __future__ import division
import argparse 
import math
from SimpleCV import Image, Color, Features
from collections import namedtuple
import os
Rectangle =  namedtuple('rectangle', ['x', 'y', 'w', 'h', 'r', 'g', 'b'])
WebRectangle  = namedtuple('webrectangle', ['x', 'y', 'w', 'h', 'type','inside']) 
Grid = namedtuple('grid', ['x','y', 'origin', 'end'])
Point = namedtuple('point', ['x','y'])
def find_color(x,y, image):
    corner = image.crop(x-2, y-2, 4, 4)
    return corner.meanColor() 

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
        rectangles.append(Rectangle(*((x, y, w, h) + c)))
    max_rectangle = max(rectangles, key=lambda rect: rect.w * rect.h) 
    #markupImage.drawRectangle(max_rectangle.x, max_rectangle.y, max_rectangle.w, max_rectangle.h, Color.ORANGE) 
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
    
    img = draw_grid(img, grid)
    web_rects= classify_rect(info[0], grid) 
    #for rect in info[0]:
       # web_rects.append(transform_rect(rect, grid))
    return web_rects, img

def classify_rect(rects, grid):
    web_rects = []
    for rect in rects:
        coords = transform_rect(rect, grid)
        x = coords[0].x
	y = coords[0].y
        w = abs(coords[0].x - coords[1].x)
	h = abs(coords[0].y - coords[1].y)
        web_rects.append(WebRectangle(x,y,w,h,"text",[]))
    return web_rects   

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
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Please enter an image to be analyzed")    
    parser.add_argument('image', type=str,
                               help='path to image to be analyzed')
    args = parser.parse_args()
    shapes = find_shapes(os.path.abspath(args.image))
    image = grid_transform(shapes)
    while True: 
        image[1].show()


