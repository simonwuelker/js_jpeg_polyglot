# js_jpeg_polyglot
This allows you to create a file that is **both** a javascript **and** a JPEG file at the same time. 
This is called a polyglot file. There are various other types of polyglots, like GIF and RAR or JPEG and PHAR.
In theory, this allows you to bypass CSP.
However, this attack is not really practical due to MIME-type restrictions on scripts.

## How to run
First you need both a source javascript and JPEG file. 
Then, run
```
python3 polyglot.py <jpeg_file> <js_file> <polyglot_file>
```
to merge `<jpeg_file>` and `<js_file>` into `<polyglot_file>`.

Note that using a charset like `utf-8` for the document will corrupt the javascript (its in `ascii`). To prevent that from happening, you need to specify a charset that contains ascii,
for example `ISO-8859-1`
```html
<script charset = "ISO-8859-1" src=url></script>
```

## Proof of concept
To run the example, execute the following in the proof_of_concept directory:
```
pip3 install -r requirements.txt
flask run
```
The example only works on IE, Firefox and Chrome don't execute the javascript.

## Credits
I did not come up with this idea. Read [this article](https://portswigger.net/research/bypassing-csp-using-polyglot-jpegs) for more information.
