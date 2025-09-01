
# added shift helper and lowercase only


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
    else:
        return ch  # later adding the  uppercase
def encrypt_file():
    pass

def decrypt_file():
    pass

def verify():
    pass

def main():
    pass

if __name__ == "__main__":
    main()
