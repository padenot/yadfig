#!/bin/sh

fail() {
    echo $1;
    exit 1
}

# Dependancies check
sed 's///' /dev/null 2> /dev/null|| fail "Missing sed"
jsmin < /dev/null 2> /dev/null || fail "Missing a jsmin in PATH"
python --version 2> /dev/null || fail "Missing python"
python -c "import Image" 2> /dev/null || fail "Missing PIL (Python Imaging Library)"
python -c "import pyexiv2" 2> /dev/null || fail "Missing pyexiv2 (python EXIF library)"

chmod +x comments.sed
# remove comments from css
./comments.sed < css/style.css > out.css
# remove space
sed ':a;N;$!ba;s/\n/ /g' out.css | tr -s ' ' > out2.css
mv out2.css out.css

# insert CSS
python py/rep.py out.css html/yadfig.html __CSS__ > index.html

# minify js
jsmin < js/script.js > out.js

# insert js
python py/rep.py out.js index.html __SCRIPT__ > index2.html
mv index2.html index.html

# insert full template
python py/rep.py index.html py/yadfig.py __TEMPLATE__ > yadfig

echo "OK, yadfig generated"

rm index.html
rm out.js
rm out.css
