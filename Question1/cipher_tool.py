


ALPHA = 26 # english alphabet size

def _shift_letter(ch, k, base):
    idx = ord(ch) - ord(base)
    return chr(ord(base) + ((idx + k) % ALPHA))


def _build_maps(shift1, shift2):
    
    enc_map = {}
    # lowercase source alphabet
    for code in range(ord('a'), ord('z') + 1):
        c = chr(code)
        if c <= 'm':  # a–m forward by shift1*shift2
            k = shift1 * shift2
            enc_map[c] = _shift_letter(c, k, 'a')
        else:        # n–z backward by (shift1 + shift2)
            k = -(shift1 + shift2)
            enc_map[c] = _shift_letter(c, k, 'a')
    # uppercase source alphabet
    for code in range(ord('A'), ord('Z') + 1):
        c = chr(code)
        if c <= 'M':  # A–M backward by shift1
            k = -shift1
            enc_map[c] = _shift_letter(c, k, 'A')
        else:         # N–Z forward by shift2^2
            k = shift2 * shift2
            enc_map[c] = _shift_letter(c, k, 'A')
    # inverse for decryption
    dec_map = {v: k for k, v in enc_map.items()}
    return enc_map, dec_map

def _transform_with_map(text, mapping):
    return ''.join(mapping.get(ch, ch) for ch in text)

def encrypt_text(plain_text, shift1, shift2):
    enc_map, _ = _build_maps(shift1, shift2)
    return _transform_with_map(plain_text, enc_map)

def decrypt_text(cipher_text, shift1, shift2):
    _, dec_map = _build_maps(shift1, shift2)
    return _transform_with_map(cipher_text, dec_map)


    
#added file read/write for encrypt and decrypt

def transform_text(text, shift1, shift2, encrypt):
    return ''.join(_transform_char(c, shift1, shift2, encrypt) for c in text)

# open raw_text.txt and save encrypted here

def encrypt_file(inp="raw_text.txt", outp="encrypted_text.txt", shift1=0, shift2=0):

    with open(inp, "r", encoding="utf-8") as f:
        raw = f.read()
        # Using the reversible map-based encryption 
    enc = encrypt_text(raw, shift1, shift2)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(enc)

def decrypt_file(inp="encrypted_text.txt", outp="decrypted_text.txt", shift1=0, shift2=0):

    # reading the  encrypted and write back down  decrypted text

    with open(inp, "r", encoding="utf-8") as f:
        enc = f.read()
        # Using  true inverse mapping for decryption
    dec = decrypt_text(enc, shift1, shift2)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(dec)

#now I add verify and connect in main

def _normalize_newlines(s):
    return s.replace("\r\n", "\n").replace("\r", "\n")

def verify(original="raw_text.txt", decrypted="decrypted_text.txt"):
    #  compareing here that  original and decrypted if same or not
    with open(original, "r", encoding="utf-8") as f1, open(decrypted, "r", encoding="utf-8") as f2:
        return _normalize_newlines(f1.read()) == _normalize_newlines(f2.read())

def main():
                    # first asking the  shift numbers
    try:
        shift1 = int(input("Enter shift1: ").strip())
        shift2 = int(input("Enter shift2: ").strip())
    except ValueError:
        print("Wrong input: shift must be number")
        return
# this is the  encrypt step
    try:
        encrypt_file(shift1=shift1, shift2=shift2)
        print("Encrypted -> encrypted_text.txt")
    except FileNotFoundError:
        print("raw_text.txt not found, pls make file and try again")
        return

# it is the decrypt step
    decrypt_file(shift1=shift1, shift2=shift2)
    print("Decrypted -> decrypted_text.txt")
# it is  the
    ok = verify()
    if ok:
        print("Verification SUCCESS, file match same")
    else:
        print("Verification FAIL, file not same")


if __name__ == "__main__":
    main()
