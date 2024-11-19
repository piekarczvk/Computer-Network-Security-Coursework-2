import random  # for generating random numbers
#provides greates common divisor function, to check if two numbers are coprime (share no common factor other than 1)
from math import gcd  
# type hinting
from typing import List, Tuple  


class CryptoSystem:
    def generate_keypair(self, n: int) -> Tuple[Tuple[List[int], int, int], List[int]]:
        """
        Generate public/private keypair.
        Returns ((e, q, w), h) where (e, q, w) is the private key and h is the public key.
        """
        #generate a sequence e where each number is greater than sum of the prvious 2 numbers 
        e = []
        current_sum = 0
        for _ in range(n):
            # Ensure the next number is greater than the sum of previous numbers
            next_num = random.randint(current_sum + 1, current_sum * 2 + 10)
            e.append(next_num)
            current_sum += next_num

        # generate a prime number  q > 2 * e[n]
        q = self._generate_prime(2 * e[-1] + 1)

        # compute  w coprime to q
        while True:
            w = random.randint(2, q - 1)
            if gcd(w, q) == 1:
                break

        #  generate public key h using hi = (w * ei) % q
        h = [(w * ei) % q for ei in e]

        return ((e, q, w), h)
    #encrypt the message using key h 
    def encrypt(self, message: List[int], public_key: List[int]) -> int:
        
        if len(message) != len(public_key):
            raise ValueError("Message and key must have the same length")
        return sum(mi * hi for mi, hi in zip(message, public_key))
    #decrypt the message (using e,q,w)
    def decrypt(self, ciphertext: int, private_key: Tuple[List[int], int, int]) -> List[int]:
        
        e, q, w = private_key

        # compute the modular inverse of w mod q
        w_inv = pow(w, -1, q)

        # compute c' = (ciphertext * w_inv) % q
        c_prime = (ciphertext * w_inv) % q

        message = []
        remaining = c_prime

        for ei in reversed(e):
            if remaining >= ei:
                message.insert(0, 1)
                remaining -= ei
            else:
                message.insert(0, 0)

        return message
    #generate smallest prime number greater or equal to min value
    def _generate_prime(self, min_value: int) -> int:
        
        def is_prime(n: int) -> bool:
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True

        num = min_value
        while not is_prime(num):
            num += 1
        return num


def main():
    print("Public-Key Encryption System")
    crypto = CryptoSystem()

    # generate keys
    n = int(input("Enter the size of the key (number of bits): "))
    private_key, public_key = crypto.generate_keypair(n)
    print(f"\nPrivate Key (e, q, w): {private_key}")
    print(f"Public Key (h): {public_key}")

    # take input in  binary m
    print("\nEnter your binary message in binary with space between each bit(e.g., '1 0 1 1'):")
    message = list(map(int, input().strip().split()))
    if len(message) != n:
        print(f"Error: Message must have {n} bits.")
        return

    # encrypt the message
    ciphertext = crypto.encrypt(message, public_key)
    print(f"\nCiphertext: {ciphertext}")

    # decrypt the message
    decrypted_message = crypto.decrypt(ciphertext, private_key)
    print(f"Decrypted Message: {decrypted_message}")


if __name__ == "__main__":
    main()
