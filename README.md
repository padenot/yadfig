# yadfig, a damn fine image gallery generator

## Once was genethumb.sh…

Yes, it worked quite nicely, but it was kind of ugly and sucked (according to
its creator). At the price of a few dependencies (`PIL`, since I don't
consider python to be a real dependency on a machine that will host pictures),
you can have something much nicer (in my point of view).

As `genethumb.sh`, is produces a single HTML file, which should work in any
reasonably recent web browser (since it uses HTML5 & co. delicacies), and is very
easy to host on any web server, without having to use any server side
programming, hopefully increasing speed and security.

I could write for hours, but nothing would bet a working demo, so here they are:

- http://paul.cx/photos/sweden/vasa/
- https://okok7711.github.io/yadfig/examples/

## Ok, I'm convinced, what next ?

### I just want to use it, you know…
Then grab `yadfig` in the download section, make sure to have `PIL`
installed (as well as Python, of course), and you're good to go.

### I want to build it myself from source…

Just run the `build.sh`, it should install everything for you.

    sudo sh build.sh

The build script uses `sed` (any flavor) and `tr`, but everybody should have
those.

Speaking of build script, here are the steps to install it:

``` sh
git clone https://github.com/padenot/yadfig
cd yadfig
./build.sh
chmod +x yadfig
mv yadfig ~/bin # or other directory in $PATH
````

## Usage

To enjoy `yadfig`, go to a directory which happen to contain pictures
(it supports all formats that PIL support, and there's formats you probably
_never heard about_), and invoke :

```
yadfig
```

An `index.html` file should appear, as well as a `.c` directory containing
thumbnails. If you want to, you can invoke it that way :

```
yadfig -p "The location where the photo were taken" -t "A title"
```

It produces a somewhat nicer output.

If you need more details about the execution of the process, just add the verbose option:

```
yadfig -p "The location" -t "The title" -v
```

Do you have a lot of images directories and you don't want to launch yadfig in each one? No problem!
yadfig knows how to generate a collection of albums, with the recursive option. Just launch it from the
directory containing the albums:

```
yadfig -t "Example" -r -d /media/photos/ -b "/galeries/example/"
```

(note that -b gives the url of the base directory containing the sub directories.)
This one produces a gallery like [this one](http://benjb.gagahome.fr/galeries/example/).

## Yeah, but it doesn't do _that_ !
Patches are welcome, but the whole thing is aimed at simplicity.

## It's broken, I use IE or Opera !
I haven't tested IE, and Opera for 30 seconds, and it silently failed. There are
great free and open-source browser you can try instead that happen to work.

## Your code is crappy !
I know, I just started with js and web stuff. The codebase quality will
eventually get better with time. If you see something really nasty, drop me a
line at [@padenot](http://twitter.com/padenot) or somewhere else.

Contact [@njbenji](http://twitter.com/njbenji) for every complaint related to
recursive processing.

## Why hot pink when the text is highlighted ?
This guy knows why, and I aggree : http://paulirish.com.

## License
New BSD License : http://www.freebsd.org/copyright/license.html

## Tools
js, html5 & css3, python, PIL, sh, vim, html5boilerplate, obviously
Firefox and Chromium, love.
