#!/bin/sh

# Pack CSS in out.css
./comments.sed < css/style.css > out.css
sed ':a;N;$!ba;s/\n/ /g' out.css | tr -s ' ' > out2.css
mv out2.css out.css

# Put it in index.html
echo "css"
python rep.py out.css yadfig.html __CSS__ > index.html

echo "js"
jsmin < js/script.js > out.js

python rep.py out.js index.html __SCRIPT__> index2.html
mv index2.html index.html

echo "py"
python rep.py index.html yadfig.py __TEMPLATE__ > yadfig

rm index.html
rm out.js
rm out.css
