def encrypt(msg, shift):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""

    shift = shift % 26

    for c in msg:
        if c in lower:
            for i in range(26):
                if c == lower[i]:
                    res += lower[(i + shift) % 26]

        elif c in upper:
            for i in range(26):
                if c == upper[i]:
                    res += upper[(i + shift) % 26]

        else:
            res += c

    return res


def decrypt(msg, shift):
    return encrypt(msg, -shift)


while True:
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")

    opt = int(input("Enter your option: "))

    if opt == 1:
        msg = input("Enter message: ")
        shift = int(input("Enter shift: "))
        print("\nEncrypted message:", encrypt(msg, shift), "\n")

    elif opt == 2:
        msg = input("Enter message: ")
        shift = int(input("Enter shift: "))
        print("\nDecrypted message:", decrypt(msg, shift), "\n")

    elif opt == 3:
        print("Exit successful.")
        break

    else:
        print("Invalid option. Please try again.")