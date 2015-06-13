# Copyright Matthew Stokes 2014. All Rights Reserved.

"""1 line desc."""

"""More intense desc."""

__author__ = 'matthewbstokes@gmail.com (Matthew Stokes)'

import sys
import getopt
import csv
import cv2
import numpy as np
from math import sqrt

FILE = "./attendance.csv"
NAME = "attendance.py"

WHITE_THRESHOLD = 100
DEBUG = 1

class Person:
  """Attendance related information for an individual."""

  def __init__(self,fn,ln,nm,days_missed,days):
    self.fn = fn
    self.ln = ln
    self.nm = nm
    self.days_missed = days_missed
    self.days = days

  def __repr__(self):
    return '%s %s %s %d %d' % (self.fn, self.ln, self.nm,
                               self.days_missed, self.days)

  def setDaysMissed(self, days):
    self.days_missed = days
  def addAttendance(self, attended):
    self.days.append(attended)

def main(argv):
  img_file = ""
  
  # parse input
  try:
    opts, args = getopt.getopt(argv, "hi:d:", ["ifile="])
  except getopt.GetoptError:
    print "USAGE: "+NAME+ ' -i <input picture>'
    sys.exit(2)
  
  for opt, arg in opts:
    if opt == '-h':
      print "USAGE: "+NAME+ ' -i <input picture>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      img_file = arg
    else:
      print "USAGE: "+NAME+ ' -i <input picture>'
      sys.exit(2)
  
  if len(argv) != 2:
    print "USAGE: "+NAME+ ' -i <input picture>'
    sys.exit(2)

  # open
  img = cv2.imread(img_file,0)
  
  # normalize
  img = _normalize(img)

  # enhance
  img, e_img = _enhance(img)

  # get attended
  attended = _getAttendance(e_img, img)
  
  # write attended to csv for import in spreadsheet
  write_to_csv(attended)

  # write image
  cv2.imwrite('output.png',e_img)

# FN | LN | ID | Days Missed | Day 1 | Day 2| .....
def write_to_csv(self, attended):
  people = []
  _days_missed = 0;
  _days = []

  # read in from old csv if present
  try:
    with open(FILE, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
        people.append(Person(row[0],row[1],row[2],int(row[3]),row[4:]))
      
    f = open(FILE, 'w')
    for p in people:
      element = attended.pop()
      p.days_missed = p.days_missed + element[1]
      p.days.append(element[1])
      f.write(p.fn+","+p.ln+","+p.nm+","+str(p.days_missed)+","+','.join(str(x) for x in p.days)+"\n")
  
  # no previous history    
  except IOError:
    f = open(FILE, 'w')
    people = _populatePeople(attended)
    for p in people:
      f.write(p.fn+","+p.ln+","+p.nm+","+str(p.days_missed)+","+','.join(str(x) for x in p.days)+"\n")

#non-intelligent way TODO: fix here
def _populatePeople(attended):
  people = []
  element = attended.pop()
  people.append(Person("F1", "L1","SN1",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F2","L2","SN2",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F3","L3","SN3",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F4","L4","SN4",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F5","L5","SN5",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F6","L6","SN6",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F7","L7","SN7",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F8","L8","SN8",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F9","L9","SN9",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F10","L10","SN10",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F11","L11","SN11",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F12","L12","SN12",element[1],[element[1]]))
  element = attended.pop()
  people.append(Person("F13","L13","SN13",element[1],[element[1]]))
  return people

def _normalize(img):
  return img

def _enhance(img):
  img = cv2.medianBlur(img,13)
#  (thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  return (img, cv2.cvtColor(img,cv2.COLOR_GRAY2BGR))

def _getCircles(self, img):
  _circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=15,minRadius=12,maxRadius=20)
  return np.uint16(np.around(_circles))

def _debug_draw_circle(img,x,y,r):
  if DEBUG == 1:
    cv2.circle(img, (x,y),r,(0,0,255),3)

def _getAttendance(e_img, img):

  # get circles
  circles = _getCircles(img)

  # get avg color inside circles
  # turple (height coordinate, attended)
  point_arr = []
  pixels = []

  for i in circles[0,:]:
    del pixels[:] # reset pixels

    for y in range (i[0]-i[2],i[0]+i[2]):
      for x in range (i[1]-i[2],i[1]+i[2]):
        pixel_value = (int(e_img[x,y][0]) + int(e_img[x,y][1]) + int(e_img[x,y][2]))/3
        pixels.append(pixel_value)

    avg_colour = (int)(sum(pixels)/len(pixels))
    print avg_colour
    if avg_colour < WHITE_THRESHOLD:
      point_arr.append((x,1))
    else:
      point_arr.append((x,0))

    _debug_draw_circle(e_img, i[0], i[1], i[2])
    _debug_draw_circle(e_img, i[0], i[1], 2)
    # draw edges of square searching pixel value inside
    _debug_draw_circle(e_img, i[0]-i[2], i[1]-i[2], 2)
    _debug_draw_circle(e_img, i[0]-i[2], i[1]+i[2], 2)
    _debug_draw_circle(e_img, i[0]+i[2], i[1]-i[2], 2)
    _debug_draw_circle(e_img, i[0]+i[2], i[1]+i[2], 2)

  # sort array but lowest height
  point_arr.sort(key=lambda tup: tup[0], reverse=True)
  
  return point_arr[2:]


if __name__ == '__main__':
  main(sys.argv[1:])
