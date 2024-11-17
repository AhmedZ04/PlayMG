def encrypt_numbers(A, B, C, D, E):
    """
    Encrypts five 3-digit numbers into a single large number.
    """
    return A * 10**12 + B * 10**9 + C * 10**6 + D * 10**3 + E


def decrypt_number(N):
    """
    Decrypts a single large number into five 3-digit numbers.
    """
    A = N // 10**12
    B = (N % 10**12) // 10**9
    C = (N % 10**9) // 10**6
    D = (N % 10**6) // 10**3
    E = N % 10**3
    return A, B, C, D, E


# Example usage:
# Five 3-digit numbers
A, B, C, D, E = 548, 546, 489, 302, 868

# Encrypt the numbers
encrypted = encrypt_numbers(A, B, C, D, E)
print("Encrypted number:", encrypted)

# Decrypt the number
decrypted = decrypt_number(encrypted)
print("Decrypted numbers:", decrypted)