import sys

# AES S-Box and Inverse S-Box
SBOX = {
    "00":"63","01":"7C","02":"77","03":"7B","04":"F2","05":"6B","06":"6F","07":"C5",
    "08":"30","09":"01","0A":"67","0B":"2B","0C":"FE","0D":"D7","0E":"AB","0F":"76",
    "10":"CA","11":"82","12":"C9","13":"7D","14":"FA","15":"59","16":"47","17":"F0",
    "18":"AD","19":"D4","1A":"A2","1B":"AF","1C":"9C","1D":"A4","1E":"72","1F":"C0",
    "20":"B7","21":"FD","22":"93","23":"26","24":"36","25":"3F","26":"F7","27":"CC",
    "28":"34","29":"A5","2A":"E5","2B":"F1","2C":"71","2D":"D8","2E":"31","2F":"15",
    "30":"04","31":"C7","32":"23","33":"C3","34":"18","35":"96","36":"05","37":"9A",
    "38":"07","39":"12","3A":"80","3B":"E2","3C":"EB","3D":"27","3E":"B2","3F":"75",
    "40":"09","41":"83","42":"2C","43":"1A","44":"1B","45":"6E","46":"5A","47":"A0",
    "48":"52","49":"3B","4A":"D6","4B":"B3","4C":"29","4D":"E3","4E":"2F","4F":"84",
    "50":"53","51":"D1","52":"00","53":"ED","54":"20","55":"FC","56":"B1","57":"5B",
    "58":"6A","59":"CB","5A":"BE","5B":"39","5C":"4A","5D":"4C","5E":"58","5F":"CF",
    "60":"D0","61":"EF","62":"AA","63":"FB","64":"43","65":"4D","66":"33","67":"85",
    "68":"45","69":"F9","6A":"02","6B":"7F","6C":"50","6D":"3C","6E":"9F","6F":"A8",
    "70":"51","71":"A3","72":"40","73":"8F","74":"92","75":"9D","76":"38","77":"F5",
    "78":"BC","79":"B6","7A":"DA","7B":"21","7C":"10","7D":"FF","7E":"F3","7F":"D2",
    "80":"CD","81":"0C","82":"13","83":"EC","84":"5F","85":"97","86":"44","87":"17",
    "88":"C4","89":"A7","8A":"7E","8B":"3D","8C":"64","8D":"5D","8E":"19","8F":"73",
    "90":"60","91":"81","92":"4F","93":"DC","94":"22","95":"2A","96":"90","97":"88",
    "98":"46","99":"EE","9A":"B8","9B":"14","9C":"DE","9D":"5E","9E":"0B","9F":"DB",
    "A0":"E0","A1":"32","A2":"3A","A3":"0A","A4":"49","A5":"06","A6":"24","A7":"5C",
    "A8":"C2","A9":"D3","AA":"AC","AB":"62","AC":"91","AD":"95","AE":"E4","AF":"79",
    "B0":"E7","B1":"C8","B2":"37","B3":"6D","B4":"8D","B5":"D5","B6":"4E","B7":"A9",
    "B8":"6C","B9":"56","BA":"F4","BB":"EA","BC":"65","BD":"7A","BE":"AE","BF":"08",
    "C0":"BA","C1":"78","C2":"25","C3":"2E","C4":"1C","C5":"A6","C6":"B4","C7":"C6",
    "C8":"E8","C9":"DD","CA":"74","CB":"1F","CC":"4B","CD":"BD","CE":"8B","CF":"8A",
    "D0":"70","D1":"3E","D2":"B5","D3":"66","D4":"48","D5":"03","D6":"F6","D7":"0E",
    "D8":"61","D9":"35","DA":"57","DB":"B9","DC":"86","DD":"C1","DE":"1D","DF":"9E",
    "E0":"E1","E1":"F8","E2":"98","E3":"11","E4":"69","E5":"D9","E6":"8E","E7":"94",
    "E8":"9B","E9":"1E","EA":"87","EB":"E9","EC":"CE","ED":"55","EE":"28","EF":"DF",
    "F0":"8C","F1":"A1","F2":"89","F3":"0D","F4":"BF","F5":"E6","F6":"42","F7":"68",
    "F8":"41","F9":"99","FA":"2D","FB":"0F","FC":"B0","FD":"54","FE":"BB","FF":"16"
}

INV_SBOX = {value: key for key, value in SBOX.items()}
RCon = ["01","02","04","08","10","20","40","80","1B","36"]

# Map letters A-Z to 00-19
def mapping(text):
    result = ""
    for character in text:
        if character.isalpha():
            result += f"{ord(character.upper()) - 65:02X}"
    return result

# Build 4x4 state matrix from 32 hex characters
def makeMatrix(hex_string):
    theMatrix = []
    for row in range(4):
        theRow = []
        for column in range(4):
            start = 8 * column + 2 * row
            theRow.append(hex_string[start:start + 2])
        theMatrix.append(theRow)
    return theMatrix

# Galois Field (2^8) multiplication: hexByte * multiplier
def gfMultiply(hexByte, multiplier):
    p = 0
    a = int(hexByte, 16) if isinstance(hexByte, str) else hexByte
    b = int(multiplier, 16) if isinstance(multiplier, str) else multiplier
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return f"{p:02X}"

def subByte(theMatrix):
    res = []
    for row in theMatrix:
        tempList = []
        for item in row:
            tempList.append(SBOX[item])
        res.append(tempList)
    return res

def invSubBytes(theMatrix):
    res = []
    for row in theMatrix:
        tempList = []
        for item in row:
            tempList.append(INV_SBOX[item])
        res.append(tempList)
    return res

def shiftRows(theMatrix):
    newMatrix = []
    for index, row in enumerate(theMatrix):
        theShiftConstant = index
        newMatrix.append(row[theShiftConstant:] + row[:theShiftConstant])
    return newMatrix

def invShiftRows(theMatrix):
    newMatrix = []
    for index, row in enumerate(theMatrix):
        shift = index
        if shift == 0:
            newMatrix.append(row[:])
        else:
            newMatrix.append(row[-shift:] + row[:-shift])
    return newMatrix

MIX_COLUMN_MATRIX = [
    ["02","03","01","01"],
    ["01","02","03","01"],
    ["01","01","02","03"],
    ["03","01","01","02"]
]
INV_MIX_COLUMN_MATRIX = [
    [0x0E,0x0B,0x0D,0x09],
    [0x09,0x0E,0x0B,0x0D],
    [0x0D,0x09,0x0E,0x0B],
    [0x0B,0x0D,0x09,0x0E]
]

def mixColumns(theMatrix):
    newMatrix = [["00"]*4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            b = 0
            for i in range(4):
                b ^= int(gfMultiply(theMatrix[i][col], MIX_COLUMN_MATRIX[row][i]), 16)
            newMatrix[row][col] = f"{b:02X}"
    return newMatrix

def invMixColumns(theMatrix):
    newMatrix = [["00"]*4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            b = 0
            for i in range(4):
                b ^= int(gfMultiply(theMatrix[i][col], INV_MIX_COLUMN_MATRIX[row][i]), 16)
            newMatrix[row][col] = f"{b:02X}"
    return newMatrix

# Key expansion: produces 44 round-key words (W0..W43) from the 16-byte key
def generateRoundKeys(m):
    theWords = []
    for x in range(4):
        theWord = []
        for row in range(4):
            theWord.append(m[row][x])
        theWords.append(theWord)
    for i in range(4, 44):
        if i % 4 == 0:
            wprocesss = theWords[i - 1][1:] + [theWords[i - 1][0]]
            wprocesss = [SBOX[byte] for byte in wprocesss]
            wprocesss[0] = f"{int(wprocesss[0], 16) ^ int(RCon[i // 4 - 1], 16):02X}"
            theNewWord = []
            for j in range(4):
                theNewWord.append(f"{int(wprocesss[j], 16) ^ int(theWords[i - 4][j], 16):02X}")
            theWords.append(theNewWord)
        else:
            theNewWord = []
            for j in range(4):
                theNewWord.append(f"{int(theWords[i - 4][j], 16) ^ int(theWords[i - 1][j], 16):02X}")
            theWords.append(theNewWord)
    return theWords

# Extract the 4x4 round key for a given round number
def makeRoundKeyMatrix(theWords, roundNumber):
    start = roundNumber * 4
    res = []
    for row in range(4):
        tempList = []
        for col in range(4):
            tempList.append(theWords[start + col][row])
        res.append(tempList)
    return res

def addRoundKey(keyMatrix, State):
    res = []
    for i in range(4):
        currList = []
        for j in range(4):
            currList.append(f"{int(keyMatrix[i][j], 16) ^ int(State[i][j], 16):02X}")
        res.append(currList)
    return res

def displayMatrix(m):
    if not m:
        print()
        return

    column_count = len(m[0])
    cell_width = max(2, max(len(str(value)) for row in m for value in row))
    separator = "+" + "+".join("-" * (cell_width + 2) for _ in range(column_count)) + "+"
    print(separator)
    for row in m:
        cells = " | ".join(f"{str(value):>{cell_width}}" for value in row)
        print(f"| {cells} |")
        print(separator)
    print()

def displayKeyMatrix(m):
    print("Original Key Matrix (4x4):")
    displayMatrix(m)

def displayKeySchedule(theWords):
    for i in range(0, 44, 1):
        print(f"W{i}: {theWords[i]}")
    print()

# Single-block AES encryption
def encryptBlock(plaintext_hex, round_words):
    print("Round 0  AddRoundKey:")
    state = addRoundKey(makeRoundKeyMatrix(round_words, 0), makeMatrix(plaintext_hex))
    displayMatrix(state)
    for round_num in range(1, 10):
        state = subByte(state)
        print(f"Round {round_num} --> SubByte:")
        displayMatrix(state)
        state = shiftRows(state)
        print(f"Round {round_num} --> ShiftRows:")
        displayMatrix(state)
        state = mixColumns(state)
        print(f"Round {round_num} --> MixColumns:")
        displayMatrix(state)
        state = addRoundKey(makeRoundKeyMatrix(round_words, round_num), state)
        print(f"Round {round_num} --> AddRoundKey:")
        displayMatrix(state)
    state = subByte(state)
    print("Round 10 --> SubByte:")
    displayMatrix(state)
    state = shiftRows(state)
    print("Round 10 --> ShiftRows:")
    displayMatrix(state)
    state = addRoundKey(makeRoundKeyMatrix(round_words, 10), state)
    print("Round 10 --> AddRoundKey:")
    displayMatrix(state)
    return state

# Single-block AES decryption
def decryptBlock(ciphertext_hex, round_words):
    print("Round 10 --> AddRoundKey (start):")
    state = addRoundKey(makeRoundKeyMatrix(round_words, 10), makeMatrix(ciphertext_hex))
    displayMatrix(state)
    for round_num in range(9, 0, -1):
        state = invShiftRows(state)
        print(f"Round {round_num} --> InvShiftRows:")
        displayMatrix(state)
        state = invSubBytes(state)
        print(f"Round {round_num} --> InvSubBytes:")
        displayMatrix(state)
        state = addRoundKey(makeRoundKeyMatrix(round_words, round_num), state)
        print(f"Round {round_num} --> AddRoundKey:")
        displayMatrix(state)
        state = invMixColumns(state)
        print(f"Round {round_num} --> InvMixColumns:")
        displayMatrix(state)
    state = invShiftRows(state)
    print("Round 0 --> InvShiftRows:")
    displayMatrix(state)
    state = invSubBytes(state)
    print("Round 0 --> InvSubBytes:")
    displayMatrix(state)
    state = addRoundKey(makeRoundKeyMatrix(round_words, 0), state)
    print("Round 0 --> AddRoundKey (end):")
    displayMatrix(state)
    return state

def encryptMessage(message, key):
    key = (key.upper().replace(" ", "") + "Z" * 16)[:16]
    message = message.upper().replace(" ", "")
    if not message:
        return ""
    padded_length = ((len(message) + 16 - 1) // 16) * 16
    message = (message + "Z" * 16)[:padded_length]
    key_matrix = makeMatrix(mapping(key))
    displayKeyMatrix(key_matrix)
    round_words = generateRoundKeys(key_matrix)
    displayKeySchedule(round_words)
    ciphertext = ""
    for start in range(0, len(message), 16):
        block = encryptBlock(mapping(message[start:start + 16]), round_words)
        for col in range(4):
            for row in range(4):
                ciphertext += block[row][col]
    return ciphertext

def decryptMessage(ciphertextHex, key):
    key = (key.upper().replace(" ", "") + "Z" * 16)[:16]
    key_matrix = makeMatrix(mapping(key))
    displayKeyMatrix(key_matrix)
    round_words = generateRoundKeys(key_matrix)
    displayKeySchedule(round_words)
    pt = ""
    for start in range(0, len(ciphertextHex), 16 * 2):
        block = decryptBlock(ciphertextHex[start:start + 16 * 2], round_words)
        for col in range(4):
            for row in range(4):
                v = int(block[row][col], 16)
                if v >= 26:
                    return pt.rstrip("Z")
                pt += chr(v + 65)
    return pt.rstrip("Z")

# CLI menu ------------------------------------------------------------------
while True:
    choice = input("AES Program\n1. Encrypt\n2. Decrypt\n3. Exit\nEnter Your Choice: ")
    if choice == "1":
        pt = input("Plaintext: ")
        key = input("Key: ")
        print("Ciphertext:", encryptMessage(pt, key))
    elif choice == "2":
        ct = input("Ciphertext: ")
        key = input("Key: ")
        print("Plaintext:", decryptMessage(ct, key))
    else:
        sys.exit()
