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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''

PLACE=""
TITLE=""
ROWCOUNT=4
template='''__TEMPLATE__'''
THUMB_DIR=".c"
DIR=os.curdir

images = list()

def is_image(mime):
  if mime.find("image") == 0:
    return True
  return False

def list_files():
    try:
        os.stat(DIR)
        full = os.path.join(DIR, THUMB_DIR)
        if not os.path.exists(full):
            os.makedirs(full)
    except os.error, err:
        print bcolors.FAIL + str(err) + bcolors.ENDC
        exit(1)

    filenames = os.listdir(DIR)

    for name in filenames:
        name = os.path.join(DIR, name)
        if is_image(str(mimetypes.guess_type(name)[0])):
            metadata = pyexiv2.ImageMetadata(name)
            metadata.read()
            images.append([name, metadata])
    if len(images) == 0:
        print bcolors.WARNING + "No pictures found in "+DIR+", exiting." + bcolors.ENDC
        exit(1)


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
    if len(dates) == 0:
      print bcolors.WARNING + "No dates found in EXIF metadata. Disabling date output" + bcolors.ENDC
      return "";

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
        thumb = os.path.join(os.path.dirname(i[0]), THUMB_DIR, os.path.basename(i[0]))
        im.save(thumb)


def usage():
    print "Usage:  %s [-p|--place] name [-t|--title] title" % os.path.basename(sys.argv[0])
    print "\n\tCreate a photo gallery in index.html and a thumbnail directory,"+THUMB_DIR+"/.\n"
    print "\t-p : name of the place the photo have been taken."
    print "\t-t : a title for the page."
    print "\t-d : a directory to operate on."

def main():
    global TITLE, PLACE, DIR
    try:
        arg, opts = getopt.getopt(sys.argv[1:], "hp:t:d:")
    except getopt.GetoptError, err:
        print bcolors.WARNING + str(err) + bcolors.ENDC
        usage()
        sys.exit(2)

    for o, a in arg:
        if o in "-p":
            PLACE=a
        elif o in "-h":
            usage
            sys.exit
        elif o in "-t":
            TITLE=a
        elif o in "-d":
            DIR=a
        else:
            assert False, "unhandled option"
    list_files()
    images.sort()
    create_thumbs()
    output_html()
    print bcolors.OKGREEN + "Generation successful:"
    print "\t" + os.path.join(DIR,"index.html")
    print "\t" + os.path.join(DIR,THUMB_DIR)+ " for " + str(len(images)) + " pictures." + bcolors.ENDC

if __name__ == "__main__":
    main()
