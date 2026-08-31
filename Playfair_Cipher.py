import numpy as np
alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def sanitize(text):
    text = text.upper().replace("J", "I")
    return "".join(c for c in text if c in alpha)

def build_matrix(key):
    matrix = []
    for c in key:
        if c not in matrix:
            matrix.append(c)
    for c in alpha:
        if c not in matrix:
            matrix.append(c)
    return np.array(matrix).reshape(5, 5)

def prepare_pair(msg):
    prepared = ""
    i = 0
    while i < len(msg):
        a = msg[i]
        if i + 1 < len(msg):
            b = msg[i + 1]
            if a == b:
                filler = 'Q' if a == 'X' else 'X'
                prepared += a + filler
                i += 1
            else:
                prepared += a + b
                i += 2
        else:
            filler = 'Q' if a == 'X' else 'X'
            prepared += a + filler
            i += 1
    return prepared

def locate(matrix, letter):
    row, col = np.where(matrix == letter)
    return row[0], col[0]

def encrypt(msg, key):
    key = sanitize(key)
    msg = sanitize(msg)
    matrix = build_matrix(key)
    prepared = prepare_pair(msg)
    enc = ""
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i + 1]
        ra, ca = locate(matrix, a)
        rb, cb = locate(matrix, b)

        if ra == rb:
            enc += matrix[ra, (ca + 1) % 5]
            enc += matrix[rb, (cb + 1) % 5]
        elif ca == cb:
            enc += matrix[(ra + 1) % 5, ca]
            enc += matrix[(rb + 1) % 5, cb]
        else:
            enc += matrix[ra, cb]
            enc += matrix[rb, ca]

    return matrix, prepared, enc

def decrypt(msg, key):
    key = sanitize(key)
    msg = sanitize(msg)
    matrix = build_matrix(key)

    dec = ""
    for i in range(0, len(msg), 2):
        a, b = msg[i], msg[i + 1]
        ra, ca = locate(matrix, a)
        rb, cb = locate(matrix, b)

        if ra == rb:
            dec += matrix[ra, (ca - 1) % 5]
            dec += matrix[rb, (cb - 1) % 5]
        elif ca == cb:
            dec += matrix[(ra - 1) % 5, ca]
            dec += matrix[(rb - 1) % 5, cb]
        else:
            dec += matrix[ra, cb]
            dec += matrix[rb, ca]
    return matrix, dec

while True:
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    opt = int(input("Enter your option: "))
    if opt == 1:
        msg = input("Enter message: ")
        key = input("Enter key: ")
        matrix, prepared, enc_msg = encrypt(msg, key)
        print("\nKey matrix:\n", matrix)
        print("\nPrepared message:", prepared)
        print("\nEncrypted message:", enc_msg, "\n")
    elif opt == 2:
        msg = input("Enter message: ")
        key = input("Enter key: ")
        matrix, dec_msg = decrypt(msg, key)
        print("\nKey matrix:\n", matrix)
        print("\nDecrypted message:", dec_msg)
        print("(Note: any 'X'/'Q' fillers inserted during encryption")
        print(" remain in this output and may need manual removal.)\n")
    elif opt == 3:
        print("Exit successful.")
        break
    else:
        print("Invalid option. Please try again.\n")