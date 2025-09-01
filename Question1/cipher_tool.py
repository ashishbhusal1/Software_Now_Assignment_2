
ALPHA = 26 # english alphabet size

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
        return ch  # there is no changes on space number and symbol heres
    
#added file read/write for encrypt and decrypt

def transform_text(text, shift1, shift2, encrypt):
    return ''.join(_transform_char(c, shift1, shift2, encrypt) for c in text)

# open raw_text.txt and save encrypted here

def encrypt_file(inp="raw_text.txt", outp="encrypted_text.txt", shift1=0, shift2=0):

    with open(inp, "r", encoding="utf-8") as f:
        raw = f.read()
    enc = transform_text(raw, shift1, shift2, True)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(enc)

def decrypt_file(inp="encrypted_text.txt", outp="decrypted_text.txt", shift1=0, shift2=0):

    # reading the  encrypted and write back down  decrypted text

    with open(inp, "r", encoding="utf-8") as f:
        enc = f.read()
    dec = transform_text(enc, shift1, shift2, False)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(dec)

#now I add verify and connect in main

def verify(original="raw_text.txt", decrypted="decrypted_text.txt"):
    #  compareing here that  original and decrypted if same or not
    with open(original, "r", encoding="utf-8") as f1, open(decrypted, "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()

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
# it is  the verify step
    ok = verify()
    if ok:
        print("Verification SUCCESS, file match same")
    else:
        print("Verification FAIL, file not same")


if __name__ == "__main__":
    main()
