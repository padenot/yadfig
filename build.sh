#!/bin/sh

fail() {
    echo $1;
    exit 1;
}

# Dependancies check
sed 's///' /dev/null 2> /dev/null|| fail "Missing sed"
python --version 2> /dev/null || fail "Missing python"
python -m pip install -r requirements.txt 2> /dev/null || fail "Cant install requirements"

chmod +x comments.sed
# remove comments from css
./comments.sed < css/style.css > out.css
sed ':a;N;$!ba;s/\n/ /g' out.css | tr -s ' ' > out2.css
mv out2.css out.css

python py/rep.py out.css html/folder.html __CSS__ > folder.html
python py/rep.py out.css html/index.html __CSS__ > index.html

python -m jsmin js/script.js > out.js

# insert js
python py/rep.py out.js index.html __SCRIPT__ > index2.html
python py/rep.py out.js folder.html __SCRIPT__ > folder2.html
mv index2.html index.html
mv folder2.html folder.html

# insert full template
python py/rep.py index.html py/yadfig.py __INDEX_TEMPLATE__ > yadfig2.py
python py/rep.py folder.html yadfig2.py __FOLDER_TEMPLATE__ > yadfig
rm yadfig2.py

echo "OK, yadfig generated"

rm index.html
rm folder.html
rm out.js
rm out.css