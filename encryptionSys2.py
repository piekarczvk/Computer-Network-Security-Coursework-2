import random
from math import gcd

1
def generate_e(n):
    if n <= 0:
        return []
    result = [1]
    for i in range(1, n):
        next_element = sum(result) + 1
        result.append(next_element)
    return result

def calculate_q(e):
    if not e:
        raise ValueError("The input list e cannot be empty.")
    
    en = e[-1]  # e_n is the last element of the list
    q = 2 * en + 1  # start with q > 2 * e_n

    # make sure q is prime
    while not is_prime(q):
        q += 1  # add 1 to q until it is prime

    return q

def generate_w(q):
    while True:
        w = random.randint(1, q - 1)
        if gcd(w, q) == 1:
            return w

def calculate_h(e, w, q):
    return [(w * ei) % q for ei in e]

def is_prime(n,k=5): 
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    def miller_test(d, n):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                return True
        return False
    
    d = n - 1
    while d % 2 == 0:
        d //= 2
    
    for _ in range(k):
        if not miller_test(d, n):
            return False
    return True


def text_to_binary(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

def binary_to_text(binary):
    if len(binary) % 8 != 0:
        raise ValueError("The length of a binary string must be a multiple of 8")
    
    text = ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))
    return text

def encrypt(m, h):
    if len(m) != len(h):
        print("Length of the message doesn't match the length of the key")
    c = sum(mi * hi for mi, hi in zip(m, h))
    return c

def decrypt(c, w_inverse, q, e):
    c_prime = (c * w_inverse) % q
    m = []
    for ei in reversed(e):
        if c_prime >= ei:
            m.append(1)
            c_prime -= ei
        else:
            m.append(0)

    m.reverse()
    return m

# Command-Line Interface Functions

def encrypt_message(input_text):
    # Convert the input text to binary
    binary_message = text_to_binary(input_text)
    message_bits = [int(bit) for bit in binary_message]  # Convert to bit list

    # Adjust number of `e` values to match message length
    n = len(message_bits)
    e_values = generate_e(n)
    q = calculate_q(e_values)
    w = generate_w(q)
    w_inverse = pow(w, -1, q)
    h_values = calculate_h(e_values, w, q)

    # Encrypt the message
    ciphertext = encrypt(message_bits, h_values)

    return ciphertext, e_values, q, w_inverse, message_bits


def decrypt_message(ciphertext, e_values, q, w_inverse):
    # Decrypt the message
    decrypted_bits = decrypt(ciphertext, w_inverse, q, e_values)

    # Convert decrypted bits back to binary string and text
    decrypted_binary = ''.join(map(str, decrypted_bits))
    decrypted_text = binary_to_text(decrypted_binary)
    
    return decrypted_text

# Main Command-Line Interface Loop
def main():
    print("Welcome to the Public-Key Encryption Command Line Tool!")
    
    while True:
        print("\nSelect an option:")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            # Encrypt message
            input_text = input("Enter the plaintext message to encrypt: ").strip()
            ciphertext, e_values, q, w_inverse, message_bits = encrypt_message(input_text)
            print(f"\nCiphertext: {ciphertext}")
            print(f"Generated e Values: {e_values}")
            print(f"Prime q: {q}")
            print(f"Random w: {w_inverse}")
            print(f"w Inverse mod q: {w_inverse}")
            print(f"Encrypted Message (Ciphertext): {ciphertext}")
        
        elif choice == "2":
            # Decrypt message
            try:
                ciphertext = int(input("Enter the ciphertext to decrypt: ").strip())
                decrypted_text = decrypt_message(ciphertext, e_values, q, w_inverse)
                print(f"\nDecrypted Text: {decrypted_text}")
            except NameError:
                print("Please encrypt a message first.")
            except Exception as e:
                print(f"Error in decryption: {e}")
        
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
