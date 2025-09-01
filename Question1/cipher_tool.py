
# uppercase rule completed here at total

ALPHA = 26

def _shift_letter(ch, k, base):
    idx = ord(ch) - ord(base)
    return chr(ord(base) + ((idx + k) % ALPHA))

def _transform_char(ch, shift1, shift2, encrypt):
    if 'a' <= ch <= 'z':
        if ch <= 'm':  # a-m forward
            k = shift1 * shift2
            k = k if encrypt else -k
            return _shift_letter(ch, k, 'a')
        else:  # n-z backward
            k = shift1 + shift2
            k = -k if encrypt else k
            return _shift_letter(ch, k, 'a')
    elif 'A' <= ch <= 'Z':
        if ch <= 'M':  # A-M backward
            k = shift1
            k = -k if encrypt else k
            return _shift_letter(ch, k, 'A')
        else:  # N-Z forward shift2^2
            k = shift2 * shift2
            k = k if encrypt else -k
            return _shift_letter(ch, k, 'A')
    else:
        return ch  
#added file read/write for encrypt and decrypt
def transform_text(text, shift1, shift2, encrypt):
    return ''.join(_transform_char(c, shift1, shift2, encrypt) for c in text)

def encrypt_file(inp="raw_text.txt", outp="encrypted_text.txt", shift1=0, shift2=0):
    with open(inp, "r", encoding="utf-8") as f:
        raw = f.read()
    enc = transform_text(raw, shift1, shift2, True)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(enc)

def decrypt_file(inp="encrypted_text.txt", outp="decrypted_text.txt", shift1=0, shift2=0):
    with open(inp, "r", encoding="utf-8") as f:
        enc = f.read()
    dec = transform_text(enc, shift1, shift2, False)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(dec)

def verify():
    pass

def main():
    pass

if __name__ == "__main__":
    main()
