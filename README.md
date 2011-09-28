# yadfig, a dame fine image gallery generator

## Once was genethumb.sh

Yes, it worked quite nicely, but it was kind of ugly and sucked (according to
its creator). At the price of a few dependencies (`pyexiv2` and PIL, since I don't
consider python to be a real dependency on a machine that will host pictures),
you can have something much nicer (in my point of view).

As `genethumb.sh`, is produces a single HTML file, which should work in any
reasonably recent web browser (since it uses HTML & co. delicacies), and is very
easy to host on any web server, without having to use any server side
programming, hopefully increasing speed and security.

I could write for hours, but nothing would bet a working demo, so here it is :
http://paul.cx/photos/sweden/vasa/

## Ok, I'm convinced, what next ?

You need to install the dependencies : `jsmin` and a couple python library.

    sudo aptitude install python-pyexiv2 python-imaging

The build script uses `sed` (any flavor) and `tr`, but everybody should have
those. Also, put a copy of jsmin (compiled from 
[this file](http://www.crockford.com/javascript/jsmin.c)), and put it somewhere in
the `$PATH`. `pyexiv2` should be in version 0.3.

Speaking of build script, here are the steps to install it when dependencies are
satisfied :

``` sh
git clone https://github.com/padenot/yadfig
cd yadfig
./build
chmod +x yadfig
mv yadfig ~/bin # or other directory in $PATH
````

Then you can enjoy `yadfig`: go to a directory which happen to contain pictures
(it supports all formats that PIL support), and invoke :

```
yadfig
```

An `index.html` file should appear, as well as a `.c` directory containing
thumbnails. If you want to, you can invoke it that way :

```
yadfig -p "The location where the photo were taken" -t "A title"
```

## Yeah, but it doesn't do _that_
Patches are welcome.

## It's broken, I use IE or Opera
I haven't tested IE, and Opera for 30 seconds, and it silently failed. There are
great free and open-source browser you can try instead that happen to work.

## You code is crappy
I know, I begining messing with js and web stuff. The codebase quality will
eventually get better with time. If you see something really nasty, drop me a
line at @padenot or somewhere else.

## Why hot pink when the text is highlighted ?
This guy knows why, and I aggree : http://paulirish.com.

# License
New BSD License http://www.freebsd.org/copyright/license.html
