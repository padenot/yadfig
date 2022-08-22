#!/usr/bin/python
# -- coding: utf-8 --

import sys
import os
import getopt
import mimetypes
import getopt
from PIL import Image


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


DEFAULT_ROWCOUNT = 4
THUMBNAIL_LIMIT_SIZE = 242  # in pixels
folder_template = """__FOLDER_TEMPLATE__"""
index_template = """__INDEX_TEMPLATE__"""

THUMB_DIR = ".c"


class Generator:
    def __init__(self, dirname, title="", place="", rowcount=DEFAULT_ROWCOUNT, verbose=False, root=None):
        self.dirname = dirname
        self.rowcount = rowcount
        self.place = place
        self.title = title
        self.images = []
        self.verbose = verbose
        self.root = root

    def run(self):
        """Launches the generator in the given directory self.dirname. Returns true if
    the page has been generated, i.e. there was no error or warning and the directory contained images."""
        try:
            if self.verbose:
                print("Listing files...")
            self.list_files()
            if self.verbose:
                print("Sorting images...")
            self.images.sort()
            if self.verbose:
                print("Creating thumbs...")
            self.create_thumbs()
            if self.verbose:
                print("Generating html...")
            self.output_html()

            print(f"{bcolors.OKGREEN} Generation successful:")
            print("\t" + os.path.join(self.dirname, "index.html"))
            print("\t" + os.path.join(self.dirname, THUMB_DIR) + \
                " for " + str(len(self.images)) + " pictures." + bcolors.ENDC)
            return True
        except Warning as warn:
            print(bcolors.WARNING + str(warn) + bcolors.ENDC)
            return False
        except Exception as error:
            print(bcolors.FAIL + str(error) + bcolors.ENDC)
            return False

    def is_image(self, mime: str, file: str): return (mime.find("image") == 0) and (not file.endswith(("svg", "gif")))

    def list_files(self):
        try:
            os.stat(self.dirname)
            full = os.path.join(self.dirname, THUMB_DIR)
            if not os.path.exists(full):
                os.makedirs(full)
        except os.error as err:
            raise Exception("In list_files: " + str(err))

        filenames = os.listdir(self.dirname)

        for name in filenames:
            full_name = os.path.join(self.dirname, name)
            if self.verbose:
                print(name)
            if self.is_image(str(mimetypes.guess_type(full_name)[0]), name):
                self.images.append([name])
        if len(self.images) == 0:
            raise Warning("No pictures found in " +
                          self.dirname + ", terminating generation.")

    def get_pictures(self):
        out = ""
        out += '<div class="row">'
        for i, image in enumerate(self.images):
            if i % self.rowcount == 0:
                out += '</div>'
                out += '<div class="row">'
            out += '<div class="cell"><img class="thumb" src=".c/'
            out += image[0]
            out += '"><p>'
            out += os.path.basename(image[0])
            out += '</p></div>'
        out += "</div>"
        return out

    def output_html(self):
        ctemplate = folder_template.replace('__TITLE__', self.title)
        ctemplate = ctemplate.replace('__PLACE__', self.place)
        pics = self.get_pictures()
        ctemplate = ctemplate.replace('__GALLERY__', pics)

        if self.root:
            link = """<a href="%s">Back to index</a>""" % self.root
            ctemplate = ctemplate.replace('__BACK_LINK__', link)
        else:
            ctemplate = ctemplate.replace('__BACK_LINK__', '')

        with open (os.path.join(self.dirname, "index.html"), "w") as f:
            f.write(ctemplate)

    def create_thumbs(self):
        for i in self.images:
            im = Image.open(os.path.join(self.dirname, i[0]))
            # make a thumbnail only if the size is higher than the thumbnail. If the image is too short, use it as the thumbnail.
            if im.size[0] > THUMBNAIL_LIMIT_SIZE:
                im.thumbnail(
                    [THUMBNAIL_LIMIT_SIZE, THUMBNAIL_LIMIT_SIZE], Image.Resampling.LANCZOS)
            thumb = os.path.join(self.dirname, THUMB_DIR,
                                os.path.basename(i[0]))
            im.save(thumb)


def usage():
    print(f"Usage:  {os.path.basename(sys.argv[0])} [-p|--place] name [-t|--title] title"
    "\n\tCreate a photo gallery in index.html and a thumbnail directory,"+THUMB_DIR+"/.\n"
    "\t-p : name of the place the photo have been taken."
    "\t-t : a title for the page, in single generation mode. In recursive mode, title of the gallery."
    "\t-d : a directory to operate on."
    """\t-r : analyse recursively the directories, starting from the directory given by the option -d or the
    current directory by default. In this case, -p is ignored. Each subdirectory of the current
    directory is an album whose title is the name of the directory. An index page is generated in the current directory,
    containing links to the different albums.
    \t-v: adds verbosity (more details during the process).
    \t-b: absolute path to the base directory, for recursive analysis. It should be the prefix URL to access the
    generated index.html"""
    )


def walk(initial_dir, title, verbose, prefix):
    links = []

    for path, dirs, files in os.walk(initial_dir):
        last_subpath = path.split("/").pop()
        if last_subpath != THUMB_DIR:  # don't apply the recursive call to thumbnails directories
            print(path)
            g = Generator(path, title=last_subpath,
                          verbose=verbose, root=prefix)
            if g.run():
                links.append((path, last_subpath))

    links.sort(key=lambda t: t[1])
    out = ""
    for path, dirname in links:
        out += """  <li>
        <a href="%s/">%s</a>
    </li>
""" % (path, dirname)

    ctemplate = index_template.replace('__TITLE__', title)
    ctemplate = ctemplate.replace('__LIST__', out)
    f = open("index.html", "w")
    f.write(ctemplate)
    f.close()


def main():
    title, place = "", ""
    recursive = False
    verbose = False

    try:
        arg, opts = getopt.getopt(sys.argv[1:], "b:rhvp:t:d:")
    except getopt.GetoptError as err:
        print(bcolors.WARNING + str(err) + bcolors.ENDC)
        usage()
        sys.exit(2)

    DIR = os.curdir
    baseurl = DIR
    for o, a in arg:
        if o in "-p":
            place = a
        elif o in "-h":
            usage
            sys.exit
        elif o in "-t":
            title = a
        elif o in "-d":
            DIR = a
            baseurl = DIR
        elif o in "-r":
            recursive = True
        elif o in "-v":
            verbose = True
        elif o in "-b":
            baseurl = a
        else:
            assert False, "unhandled option"

    if recursive:
        walk(DIR, title, verbose=verbose, prefix=baseurl)
    else:
        g = Generator(dirname=DIR, title=title, place=place, verbose=verbose)
        g.run()


if __name__ == "__main__":
    main()
