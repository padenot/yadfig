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

def is_image(mime):
  if mime.find("image") == 0:
    return True
  return False

def list_files():
  if not os.path.exists(".c"):
    os.makedirs(".c")

  filenames = os.listdir(os.curdir)
  for name in filenames:
    if is_image(str(mimetypes.guess_type(name)[0])):
      metadata = pyexiv2.ImageMetadata(name)
      metadata.read()
      images.append([name, metadata])

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
        dates.append(i[1]['Exif.Image.DateTime'].value)
      except KeyError:
        continue
    dates.sort()
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
    if not PLACE:
      template = template.replace('__DATE__', get_date_interval())
    else:
      template = template.replace('__DATE__', get_date_interval()+',')
    pics = get_pictures()
    template = template.replace('__GALLERY__', pics);
    f = open("index.html", "w")
    f.write(template)
    f.close()

def create_thumbs():
    for i in images:
        im = Image.open(i[0])
        im.thumbnail([im.size[0]/4, im.size[0]/4], Image.ANTIALIAS)
        im.save(".c/"+i[0])


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
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in arg:
        if o in ("-p", "--place"):
            PLACE=a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-t", "--title"):
            TITLE=a
        else:
            assert False, "unhandled option"
    list_files()
    images.sort()
    create_thumbs()
    output_html()
    print "generated index.html & .c/"

if __name__ == "__main__":
    main()
