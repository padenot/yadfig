#!/usr/bin/python
# -- coding: utf-8 --

import sys
import os
import getopt
import mimetypes
import pyexiv2
import datetime
import getopt
import Image

PLACE=""
TITLE=""
ROWCOUNT=4
template='''__TEMPLATE__'''

images = list()
exif_keys = ['Exif.Image.Make',
'Exif.Image.Model',
'Exif.Image.Orientation',
'Exif.Image.XResolution',
'Exif.Image.YResolution',
'Exif.Image.ResolutionUnit',
'Exif.Image.Software',
'Exif.Image.DateTime',
'Exif.Image.ExifTag',
'Exif.Photo.ExposureTime',
'Exif.Photo.FNumber',
'Exif.Photo.ExposureProgram',
'Exif.Photo.ISOSpeedRatings',
'Exif.Photo.ExifVersion',
'Exif.Photo.ExposureBiasValue',
'Exif.Photo.MaxApertureValue',
'Exif.Photo.MeteringMode',
'Exif.Photo.LightSource',
'Exif.Photo.Flash',
'Exif.Photo.FocalLength']

def is_image(mime):
  if mime.find("image") == 0:
    return True
  return False

def list_files():
  if not os.path.exists(".c"):
    os.makedirs(".c")

  filenames = os.listdir(os.curdir)
  for i in filenames:
    if is_image(str(mimetypes.guess_type(i)[0])):
      try:
        image = pyexiv2.Image(i)
        image.readMetadata()
        images.append([i, image])
      except:
        continue

def get_pictures():
  i = 0
  out = ""
  out+='<div class="row">'
  for image in images:
    if i % ROWCOUNT == 0:
      out+='</div>'
      out+='<div class="row">'
    out+='<div class="cell"><img class="thumb" src=".c/'
    out+=image[0]
    out+='"><p>'
    out+=image[0]
    out+='</p></div>'
    i=i+1
  out+="</div>"
  return out

def get_date_interval():
    dates = list()
    for i in images:
      try:
        dates.append(i[1]['Exif.Image.DateTime'])
      except:
        continue
    dates.sort()
    print len(dates)
    formatdate = "%d %B %Y"
    formattime = "%H:%M"
    formatfull = formatdate + " at " + formattime
    date1 = dates[0].strftime(formatdate)
    date2 = dates[1].strftime(formatdate)
    if date1 == date2:
      return "The " + dates[0].strftime(formatdate) + ", from " + dates[0].strftime(formattime) + " to " + dates[-1].strftime(formattime)
    else:
      return "From the " + dates[0].strftime(formatfull) + " to the " + dates[-1].strftime(formatfull)

def output_html():
    global template
    template = template.replace('__TITLE__', TITLE)
    template = template.replace('__PLACE__', PLACE)
    template = template.replace('__DATE__', get_date_interval())
    pics = get_pictures()
    template = template.replace('__GALLERY__', pics);
    #print template
    f = open("index.html", "w")
    f.write(template)
    f.close()

def create_thumbs():
    for i in images:
        im = Image.open(i[0])
        im.thumbnail([im.size[0]/4, im.size[0]/4], Image.ANTIALIAS)
        im.save(".c/"+i[0], "JPEG")


def usage():
    print "Usage:  %s [-p|--place] name [-t|--title] title" % os.path.basename(sys.argv[0])
    print "\n\tCreate a photo gallery in index.html and a thumbnail directory, .c.\n"
    print "\t-p|--place : name of the place the photo have been taken."
    print "\t-t|--title : a title for the page."

def main():
    global TITLE
    global PLACE
    try:
        arg, opts = getopt.getopt(sys.argv[1:], "hp:t:", ["help", "place", "title"])
        print arg, opts
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in arg:
        if o in ("-p", "--place"):
            print "got a place"
            PLACE=a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-t", "--title"):
            print "got a title"
            TITLE=a
        else:
            assert False, "unhandled option"
    list_files()
    images.sort()
    create_thumbs()
    output_html()

if __name__ == "__main__":
    main()
