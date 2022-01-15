import sys
import struct

with open(sys.argv[1], "rb") as jpeg_in:
    jpeg_bin = jpeg_in.read()

with open(sys.argv[2], "rb") as js_in:
    js_bin  = js_in.read()

out = bytearray()
jpeg_pointer = 0

# jpeg header (always \xFF\xD8) 
out.extend(jpeg_bin[jpeg_pointer:jpeg_pointer + 2])
jpeg_pointer += 2

# APP0 marker (always \xFF\xe0)
out.extend(jpeg_bin[jpeg_pointer:jpeg_pointer + 2])
jpeg_pointer += 2

# the first four bytes of the jpeg make up a non-ascii identifier in javascript

# APP0 segment size (always two bytes)
# extend this to \x09\x3A ("<tab>:" in ascii, 2362 in decimal) to declare a js label
out.extend(b"\x09\x3a")
app0_size = struct.unpack(">h", jpeg_bin[jpeg_pointer:jpeg_pointer + 2])[0]
app0_end = app0_size + jpeg_pointer
jpeg_pointer += 2

# Add the JFIF APP0 identifier (always \x4A\x46\x49\x46\x00, which is also a valid js identifier
out.extend(jpeg_bin[jpeg_pointer:jpeg_pointer + 5])
jpeg_pointer += 5

# replace the NULL byte of the APP0 identifier with \x2F ("/" in ascii, 47 in decimal)
out[-1] = 47

# Add the JFIF APP0 version (always two bytes)
out.extend(jpeg_bin[jpeg_pointer:jpeg_pointer + 2])
jpeg_pointer += 2

# replace the first version byte with \x2A ("*" in ascii, 42 in decimal)
# together with the "/" from the identifier, this creates a multiline js comment
out[-2] = 42

# add the rest of the header
out.extend(jpeg_bin[jpeg_pointer:app0_end])

pad_with = 2362 - app0_size - len(js_bin) - 4
out.extend(b"\x00" * pad_with) # match the declared segment size by padding NULL bytes
out.extend(b"\x2A\x2F") # Close the js comment
out.extend(js_bin) # inject js code
out.extend(b"\x2F\x2A") # Open another js comment, ignoring all subsequent jpg data

# Add the rest of the jpg, up to the EOI marker
jpeg_pointer = app0_end
out.extend(jpeg_bin[jpeg_pointer:-2])

# add a comment block, 6 bytes long
out.extend(b"\xFF\xFE\00\06")

# close the js multiline comment and start a singleline one
out.extend(b"*///")

# add the EOI marker
out.extend(b"\xFF\xD9")

with open(sys.argv[3], "wb") as out_polyglot:
    out_polyglot.write(out)
