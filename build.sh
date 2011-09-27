#!/bin/sh

# Pack CSS in out.css
cat css/style.css | sed -e '
s/^[ \t]*//g;         # remove leading space
s/[ \t]*$//g;         # remove trailing space
s/\([:{;,]\) /\1/g;   # remove space after a colon, brace, semicolon, or comma
s/ {/{/g;             # remove space before a semicolon
s/\/\*.*\*\///g;      # remove comments
/^$/d                 # remove blank lines
' | sed -e :a -e '$!N; s/\n\(.\)/\1/; ta # remove all newlines
' > out.css

# Put it in index.html
sed 's/__CSS__/`cat out.css`/' yadfig.html > index.html

rm out.css

# minify js
jsmin < js/script.js > out.js

sed -i 's/__SCRIPT__/`cat out.js`/' index.html

rm out.js

sed 's/__TEMPLATE__/`cat index.html`/' yadfig.py > yadfig

