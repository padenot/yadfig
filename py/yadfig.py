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

DEFAULT_ROWCOUNT=4
THUMBNAIL_LIMIT_SIZE=242 # in pixels
folder_template="""__FOLDER_TEMPLATE__"""
index_template="""__INDEX_TEMPLATE__"""

THUMB_DIR=".c"

class Generator:
    def __init__(self, dirname, title = "", place = "", rowcount = DEFAULT_ROWCOUNT):
        self.dirname = dirname
        self.rowcount = rowcount
        self.place = place
        self.title = title
        self.images = []

    def run(self):
        """Launches the generator in the given directory self.dirname. Returns true iff
    the page has been generated, i.e. there was no error and the directory contained images."""
        try:
            self.list_files()
            self.images.sort()
            self.create_thumbs()
            self.output_html()

            print bcolors.OKGREEN + "Generation successful:"
            print "\t" + os.path.join(self.dirname,"index.html")
            print "\t" + os.path.join(self.dirname,THUMB_DIR)+ " for " + str(len(self.images)) + " pictures." + bcolors.ENDC

            return True

        except Warning as warn:
            print bcolors.WARNING + str(warn) + bcolors.ENDC
            return False
        except Exception as error:
            print bcolors.FAIL + str(error) + bcolors.ENDC
            return False

    def is_image(self, mime):
      return mime.find("image") == 0

    def list_files(self):
        try:
            os.stat(self.dirname)
            full = os.path.join(self.dirname, THUMB_DIR)
            if not os.path.exists(full):
                os.makedirs(full)
        except os.error, err:
            raise Exception( "In list_files: " + str(err) )

        filenames = os.listdir(self.dirname)

        for name in filenames:
            full_name = os.path.join(self.dirname, name)
            print name
            if self.is_image(str(mimetypes.guess_type(full_name)[0])):
                metadata = pyexiv2.ImageMetadata(full_name)
                metadata.read()
                self.images.append([name, metadata])
        if len(self.images) == 0:
            raise Warning("No pictures found in " + self.dirname + ", terminating generation.")

    def get_pictures(self):
      i = 0
      out = ""
      out+='<div class="row">'
      for image in self.images:
        if i % self.rowcount == 0:
          out+='</div>'
          out+='<div class="row">'
        out+='<div class="cell"><img class="thumb" src=".c/'
        out+=image[0]
        out+='"><p>'
        out+=os.path.basename(image[0])
        out+='</p></div>'
        i=i+1
      out+="</div>"
      return out

    def get_date_interval(self):
        dates = list()
        for i in self.images:
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

    def output_html(self):
        global folder_template
        ctemplate = folder_template.replace('__TITLE__', self.title)
        ctemplate = ctemplate.replace('__PLACE__', self.place)
        if not self.place:
          ctemplate = ctemplate.replace('__DATE__', self.get_date_interval())
        else:
          ctemplate = ctemplate.replace('__DATE__', self.get_date_interval()+',')
        pics = self.get_pictures()
        ctemplate = ctemplate.replace('__GALLERY__', pics);
        f = open(os.path.join(self.dirname, "index.html"), "w")
        f.write(ctemplate)
        f.close()

    def create_thumbs(self):
        for i in self.images:
            im = Image.open(os.path.join(self.dirname, i[0]))
            # make a thumbnail only if the size is higher than the thumbnail. If the image is too short, use it as the thumbnail.
            if im.size[0] > THUMBNAIL_LIMIT_SIZE:
                im.thumbnail([THUMBNAIL_LIMIT_SIZE, THUMBNAIL_LIMIT_SIZE], Image.ANTIALIAS)
            thumb = os.path.join(self.dirname, THUMB_DIR, os.path.basename(i[0]))
            im.save(thumb)


def usage():
    print "Usage:  %s [-p|--place] name [-t|--title] title" % os.path.basename(sys.argv[0])
    print "\n\tCreate a photo gallery in index.html and a thumbnail directory,"+THUMB_DIR+"/.\n"
    print "\t-p : name of the place the photo have been taken."
    print "\t-t : a title for the page, in single generation mode. In recursive mode, title of the gallery."
    print "\t-d : a directory to operate on."
    print """\t-r : analyse recursively the directories, starting from the directory given by the option -d or the
    current directory by default. In this case, -p is ignored. Each subdirectory of the current
    directory is an album whose title is the name of the directory. An index page is generated in the current directory,
    containing links to the different albums."""

def tuple_sort( t ):
    return t[1]

def walk(initial_dir, title):
    links = []

    for path, dirs, files in os.walk(initial_dir):
        last_subpath = path.split("/").pop()
        if last_subpath != THUMB_DIR: # don't apply the recursive call to thumbnails directories
            g = Generator( path, title=last_subpath )
            if g.run():
                links.append( (path, last_subpath) )

    links.sort(key=tuple_sort)
    # generate HTML
    out = ""
    for path, dirname in links:
        out += """  <li>
        <a href="%s/">%s</a>
    </li>
""" % ( path, dirname )

    ctemplate = index_template.replace('__TITLE__', title)
    ctemplate = ctemplate.replace('__LIST__', out)
    f = open("index.html", "w")
    f.write(ctemplate)
    f.close()

def main():
    title, place = "", ""
    recursive = False

    try:
        arg, opts = getopt.getopt(sys.argv[1:], "rhp:t:d:")
    except getopt.GetoptError, err:
        print bcolors.WARNING + str(err) + bcolors.ENDC
        usage()
        sys.exit(2)

    DIR=os.curdir
    for o, a in arg:
        if o in "-p":
            place=a
        elif o in "-h":
            usage
            sys.exit
        elif o in "-t":
            title=a
        elif o in "-d":
            DIR=a
        elif o in "-r":
            recursive = True
        else:
            assert False, "unhandled option"

    if recursive:
        walk( DIR, title )
    else:
        g = Generator(dirname = DIR, title = title, place = place)
        g.run()

if __name__ == "__main__":
    main()
