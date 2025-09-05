

import sys                  # I use this to show error messages when something goes wrong
from typing import List, Tuple   # I use this just to describe the types like lists and strings


# HERE IS THE ENCRYPT FUNCTION

def encrypt_file(in_path: str, out_path: str, shift1: int, shift2: int) -> Tuple[str, List[int]]:
    # This function reads the original text files and applies my rules to change the letters
    # and then writes the secret (encrypted) text into another file.
    # I also keep a list of rules used so that I can chnage them later.

    with open(in_path, "r", encoding="utf-8") as fr:   # Open the original file
        original_text = fr.read()                      #  For Reading  the content from the file

    encrypted_chars: List[str] = []   # Here I store all the encrypted characters
    rules: List[int] = []             # Here I remember which rule I used for each character

    for ch in original_text:          # Going through each character one by one
        if 'a' <= ch <= 'z':          # It is for the Lower Case
            if ch <= 'm':             # It is for the first half (a–m)
                #  shift forward by shift1 * shift2
                new_index = (ord(ch) - ord('a') + (shift1 * shift2)) % 26
                encrypted_chars.append(chr(new_index + ord('a')))
                rules.append(0)
            else:                     # If it is in the second half (n–z)
                # shift backward by shift1 + shift2
                new_index = (ord(ch) - ord('a') - (shift1 + shift2)) % 26
                encrypted_chars.append(chr(new_index + ord('a')))
                rules.append(1)

        elif 'A' <= ch <= 'Z':        # If it is an uppercase letter
            if ch <= 'M':             # If it is in the first half (A–M)
                #  shift backward by shift1
                new_index = (ord(ch) - ord('A') - shift1) % 26
                encrypted_chars.append(chr(new_index + ord('A')))
                rules.append(2)
            else:                     # If it is in the second half (N–Z)
                #  shift forward by shift2 squared
                new_index = (ord(ch) - ord('A') + (shift2 ** 2)) % 26
                encrypted_chars.append(chr(new_index + ord('A')))
                rules.append(3)

        else:                         # If it is not a letter then leave it unchanged (numbers,spaces,symbols)
            encrypted_chars.append(ch)
            rules.append(4)

    encrypted_text = "".join(encrypted_chars)   # Join the encrypted characters back into a string

    with open(out_path, "w", encoding="utf-8") as fe:  # Saving the encrypted string into a file
        fe.write(encrypted_text)

    return encrypted_text, rules   # Return the encrypted text and the rules list


# DECRYPT FUNCTION

def decrypt_file(in_path: str, out_path: str, rules: List[int], shift1: int, shift2: int) -> str:
    # This function does the opposite of encryption.
    # It reads the encrypted text and uses the rules list to get the original back.

    with open(in_path, "r", encoding="utf-8") as fe:   # Encrypted file is opened
        encrypted_text = fe.read()                     # Contents Reading

    if len(encrypted_text) != len(rules):              # Checking  if text and rules match in length
        raise ValueError("Mismatch: encrypted text and rules length differ.")

    decrypted_chars: List[str] = []   #  The decrypted characters is stored  here

    for i, ch in enumerate(encrypted_text):   # Go through each encrypted character
        rule = rules[i]                       # Find which rule was used before

        if rule == 0:  # lowercase a–m shifted forward
            idx = ord(ch) - ord('a')
            orig_index = (idx - (shift1 * shift2)) % 26
            decrypted_chars.append(chr(orig_index + ord('a')))

        elif rule == 1:  # lowercase n–z shifted backward
            idx = ord(ch) - ord('a')
            orig_index = (idx + (shift1 + shift2)) % 26
            decrypted_chars.append(chr(orig_index + ord('a')))

        elif rule == 2:  # uppercase A–M shifted backward
            idx = ord(ch) - ord('A')
            orig_index = (idx + shift1) % 26
            decrypted_chars.append(chr(orig_index + ord('A')))

        elif rule == 3:  #  uppercase N–Z shifted forward
            idx = ord(ch) - ord('A')
            orig_index = (idx - (shift2 ** 2)) % 26
            decrypted_chars.append(chr(orig_index + ord('A')))

        else:          
            decrypted_chars.append(ch)

    decrypted_text = "".join(decrypted_chars)   # Joining the decrypted characters into a string

    with open(out_path, "w", encoding="utf-8") as fd:  # decrypted text into file
        fd.write(decrypted_text)

    return decrypted_text   # Return the final decrypted string



# VERIFY FUNCTION

def verify_files(original_path: str, decrypted_path: str) -> bool:
    # This function checks if the decrypted file is the same as the original.
    # If they are the same return True. Otherwise return False.

    with open(original_path, "r", encoding="utf-8") as fr:
        original = fr.read()
    with open(decrypted_path, "r", encoding="utf-8") as fd:
        decrypted = fd.read()

    return original == decrypted


# MAIN PROGRAM

def main() -> None:
    # This is the main function that controls everything 

    try:
        # Asking two numbers from the user (shift1 and shift2)
        shift1 = int(input("Enter shift1: ").strip())
        shift2 = int(input("Enter shift2: ").strip())
    except ValueError:
        # If the input is not a number, show an error and stop
        print("Invalid input. Please enter numbers only.", file=sys.stderr)
        return

    # File names I am using in this program
    raw_path = "Question1/raw_text.txt"        # Original file
    enc_path = "Question1/encrypted_text.txt"  # Encrypted file
    dec_path = "Question1/decrypted_text.txt"  # Decrypted file

    try:
        #  Encrypt the original file
        _, rules = encrypt_file(raw_path, enc_path, shift1, shift2)
        print(f"Encrypted -> {enc_path}")

        # Decrypt the encrypted file
        decrypt_file(enc_path, dec_path, rules, shift1, shift2)
        print(f"Decrypted -> {dec_path}")

        #  Verify if decrypted text matches the original text
        if verify_files(raw_path, dec_path):
            print("Verification succeeded: decrypted text matches the original.")
        else:
            print("Verification failed: decrypted text does NOT match the original.")

    except FileNotFoundError as e:
        # If the original file is missing
        print(f"File error: {e}. Make sure '{raw_path}' exists.", file=sys.stderr)
    except Exception as e:
        # Handle any unexpected errors
        print(f"Unexpected error: {e}", file=sys.stderr)



if __name__ == "__main__":
    main()
