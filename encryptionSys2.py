import random 
from math import gcd

#Generate a set of positive integers (e1, e2, ..., en) where each element ei is greater than the sum of all previous elements in the set
#n-elements in the set 
#returns a list
def generate_e(n):
    if n<=0:
        return []
    result=[1]
    for i in range(1,n):
        next_element=sum(result)+1
        result.append(next_element)
    return result
    

    
def calculate_q(e):
    if not e:
        raise ValueError("The input list e cannot be empty.")
    
    en = e[-1]  # e_n is the last element of the list
    q = 2 * en + 1  # start with q > 2 * e_n

    # make sure  q is prime
    while not is_prime(q):
        q += 1  # add 1 to q until it is prime

    return q

# generate a random number w such that gcd(w, q) = 1.

def generate_w(q):
    
    while True:
        w = random.randint(1, q - 1)  
        if gcd(w, q) == 1:
            return w
            
def calculate_h(e, w, q):
        return [(w * ei) % q for ei in e]


        
    
def is_prime(n):
    if n<=1:
        return False
    if n<=3:
        return True
    if n%2==0 or n%3==0:
        return False
    i=5
    while i*i<=n:
        if n%i==0 or n%(i+2)==0:
            return False
        i+=6
    return True
    
def text_to_binary(text):
    binary_text=''.join(format(ord(char),'08b') for char in text)
    return binary_text

def binary_to_text(binary):
    if len(binary)%8 != 0:
        raise ValueError("The length of a binary string must be a multiple of 8")
    
    text=''.join(chr(int(binary[i:i+8],2)) for i in range(0, len(binary),8))
    return text
    
def encrypt(m,h):
    if len(m) != len(h):
        print("Length of the message doesnt match the length of the key")
        
    c=sum(mi*hi for mi, hi in zip(m,h))
    return c

def decrypt(c, w_inverse,q,e):
    c_prime=(c*w_inverse)%q
    m=[]
    for ei in reversed(e):
        if c_prime >=ei:
            m.append(1)
            c_prime-=ei
        else:
            m.append(0)
            
    m.reverse()
    return m
        


 
#test
# Adjust the length of `e` dynamically based on the binary message
input_text = "Hi"
binary_message = text_to_binary(input_text)  # Convert text to binary
message_bits = [int(bit) for bit in binary_message]  # Convert binary string to a list of bits

# Adjust number of `e` values to match message length
n = len(message_bits)  # Number of bits in the binary message
e_values = generate_e(n)  # Generate e values
q = calculate_q(e_values)  # Calculate q
w = generate_w(q)  # Generate w
w_inverse = pow(w, -1, q)  # Calculate modular inverse of w mod q
h_values = calculate_h(e_values, w, q)  # Calculate h values

# Encrypt the message
ciphertext = encrypt(message_bits, h_values)

# Decrypt the message
decrypted_bits = decrypt(ciphertext, w_inverse, q, e_values)

# Convert decrypted bits back to binary string and text
decrypted_binary = ''.join(map(str, decrypted_bits))
decrypted_text = binary_to_text(decrypted_binary)

# Display test results
print("Original Text:", input_text)
print("Binary Message:", binary_message)
print("Generated e Values:", e_values)
print("Prime q:", q)
print("Random w:", w)
print("w Inverse mod q:", w_inverse)
print("Calculated h Values:", h_values)
print("Ciphertext:", ciphertext)
print("Decrypted Binary Message:", decrypted_binary)
print("Decrypted Text:", decrypted_text)

# Validate the result
if input_text == decrypted_text:
    print("Test passed: Decryption is successful.")
else:
    print("Test failed: Decryption is incorrect.")


        
    