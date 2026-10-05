import sys
SBOX = {
    "00": "63", "01": "7C", "02": "77", "03": "7B",
    "04": "F2", "05": "6B", "06": "6F", "07": "C5",
    "08": "30", "09": "01", "0A": "67", "0B": "2B",
    "0C": "FE", "0D": "D7", "0E": "AB", "0F": "76",

    "10": "CA", "11": "82", "12": "C9", "13": "7D",
    "14": "FA", "15": "59", "16": "47", "17": "F0",
    "18": "AD", "19": "D4", "1A": "A2", "1B": "AF",
    "1C": "9C", "1D": "A4", "1E": "72", "1F": "C0",

    "20": "B7", "21": "FD", "22": "93", "23": "26",
    "24": "36", "25": "3F", "26": "F7", "27": "CC",
    "28": "34", "29": "A5", "2A": "E5", "2B": "F1",
    "2C": "71", "2D": "D8", "2E": "31", "2F": "15",

    "30": "04", "31": "C7", "32": "23", "33": "C3",
    "34": "18", "35": "96", "36": "05", "37": "9A",
    "38": "07", "39": "12", "3A": "80", "3B": "E2",
    "3C": "EB", "3D": "27", "3E": "B2", "3F": "75",

    "40": "09", "41": "83", "42": "2C", "43": "1A",
    "44": "1B", "45": "6E", "46": "5A", "47": "A0",
    "48": "52", "49": "3B", "4A": "D6", "4B": "B3",
    "4C": "29", "4D": "E3", "4E": "2F", "4F": "84",

    "50": "53", "51": "D1", "52": "00", "53": "ED",
    "54": "20", "55": "FC", "56": "B1", "57": "5B",
    "58": "6A", "59": "CB", "5A": "BE", "5B": "39",
    "5C": "4A", "5D": "4C", "5E": "58", "5F": "CF",

    "60": "D0", "61": "EF", "62": "AA", "63": "FB",
    "64": "43", "65": "4D", "66": "33", "67": "85",
    "68": "45", "69": "F9", "6A": "02", "6B": "7F",
    "6C": "50", "6D": "3C", "6E": "9F", "6F": "A8",

    "70": "51", "71": "A3", "72": "40", "73": "8F",
    "74": "92", "75": "9D", "76": "38", "77": "F5",
    "78": "BC", "79": "B6", "7A": "DA", "7B": "21",
    "7C": "10", "7D": "FF", "7E": "F3", "7F": "D2",

    "80": "CD", "81": "0C", "82": "13", "83": "EC",
    "84": "5F", "85": "97", "86": "44", "87": "17",
    "88": "C4", "89": "A7", "8A": "7E", "8B": "3D",
    "8C": "64", "8D": "5D", "8E": "19", "8F": "73",

    "90": "60", "91": "81", "92": "4F", "93": "DC",
    "94": "22", "95": "2A", "96": "90", "97": "88",
    "98": "46", "99": "EE", "9A": "B8", "9B": "14",
    "9C": "DE", "9D": "5E", "9E": "0B", "9F": "DB",

    "A0": "E0", "A1": "32", "A2": "3A", "A3": "0A",
    "A4": "49", "A5": "06", "A6": "24", "A7": "5C",
    "A8": "C2", "A9": "D3", "AA": "AC", "AB": "62",
    "AC": "91", "AD": "95", "AE": "E4", "AF": "79",

    "B0": "E7", "B1": "C8", "B2": "37", "B3": "6D",
    "B4": "8D", "B5": "D5", "B6": "4E", "B7": "A9",
    "B8": "6C", "B9": "56", "BA": "F4", "BB": "EA",
    "BC": "65", "BD": "7A", "BE": "AE", "BF": "08",

    "C0": "BA", "C1": "78", "C2": "25", "C3": "2E",
    "C4": "1C", "C5": "A6", "C6": "B4", "C7": "C6",
    "C8": "E8", "C9": "DD", "CA": "74", "CB": "1F",
    "CC": "4B", "CD": "BD", "CE": "8B", "CF": "8A",

    "D0": "70", "D1": "3E", "D2": "B5", "D3": "66",
    "D4": "48", "D5": "03", "D6": "F6", "D7": "0E",
    "D8": "61", "D9": "35", "DA": "57", "DB": "B9",
    "DC": "86", "DD": "C1", "DE": "1D", "DF": "9E",

    "E0": "E1", "E1": "F8", "E2": "98", "E3": "11",
    "E4": "69", "E5": "D9", "E6": "8E", "E7": "94",
    "E8": "9B", "E9": "1E", "EA": "87", "EB": "E9",
    "EC": "CE", "ED": "55", "EE": "28", "EF": "DF",

    "F0": "8C", "F1": "A1", "F2": "89", "F3": "0D",
    "F4": "BF", "F5": "E6", "F6": "42", "F7": "68",
    "F8": "41", "F9": "99", "FA": "2D", "FB": "0F",
    "FC": "B0", "FD": "54", "FE": "BB", "FF": "16"
}



def mapping(sentence):
    sentence = sentence.upper().replace(" ", "")
    thedict = {
        "A": "00",
        "B": "01",
        "C": "02",
        "D": "03",
        "E": "04",
        "F": "05",
        "G": "06",
        "H": "07",
        "I": "08",
        "J": "09",
        "K": "0A",
        "L": "0B",
        "M": "0C",
        "N": "0D",
        "O": "0E",
        "P" :"0F",
        "Q": "10",
        "R": "11",
        "S": "12",
        "T": "13",
        "U": "14",
        "V": "15",
        "W": "16",
        "X": "17",
        "Y": "18",
        "Z": "19"
    }
    res = ""
    for letter in sentence:
        res += thedict[letter]
    return res
RCon = ["01", "02", "04", "08", "10", "20", "40", "80", "1B", "36"]

def makeMatrix(sentence):
    sentence = sentence[:32]
    theMatrix = []
    theMatrix.append([sentence[0:2], sentence[8:10], sentence[16:18], sentence[24:26]])
    theMatrix.append([sentence[2:4], sentence[10:12], sentence[18:20], sentence[26:28]])
    theMatrix.append([sentence[4:6], sentence[12:14], sentence[20:22], sentence[28:30]])
    theMatrix.append([sentence[6:8], sentence[14:16], sentence[22:24], sentence[30:32]])
    return theMatrix
def processSentence():
    givenSentence = input("Input a string of length 16 max: ")
    givenSentence = givenSentence[:16]
    if len(givenSentence) < 16:
        givenSentence += "Z" * (16 - len(givenSentence))
    return givenSentence

# def subByte(theMatrix):
#     theMappingDict = {
#         "00": "63",
#         "01": "7C",
#         "02": "77",
#         "03": "7B",
#         "04": "F2",
#         "05": "6B",
#         "06": "6F",
#         "07": "C5",
#         "08": "30",
#         "09": "01",
#         "0A": "67",
#         "0B": "2B",
#         "0C": "FE",
#         "0D": "D7",
#         "0E": "AB",
#         "0F": "76",
#         "10": "CA",
#         "11": "82",
#         "12": "C9",
#         "13": "7D",
#         "14": "FA",
#         "15": "59",
#         "16": "47",
#         "17": "E0",
#         "18": "AD",
#         "19": "D4",
#     }
#     res = []
#     for row in theMatrix:
#         tempList = []
#         for item in row:
#             tempList.append(theMappingDict[item])
#         res.append(tempList)
#     return res

def subByte(theMatrix):
    res = []

    for row in theMatrix:
        tempList = []

        for item in row:
            tempList.append(SBOX[item])

        res.append(tempList)

    return res

def byteMul2(hexByte):
    value = int(hexByte, 16)

    # Check the original MSB
    msb_set = value & 0x80

    # Left shift and keep it to 8 bits
    value = (value << 1) & 0xFF

    # AES reduction
    if msb_set:
        value ^= 0x1B

    return f"{value:02X}"


def byteMul3(hexByte):
    value = int(hexByte, 16)
    mul2 = int(byteMul2(hexByte), 16)

    result = mul2 ^ value

    return f"{result:02X}"


def mixColumns(theMatrix):
    constantMatrix = [
        ["02", "03", "01", "01"],
        ["01", "02", "03", "01"],
        ["01", "01", "02", "03"],
        ["03", "01", "01", "02"]
    ]

    newMatrix = [
    ["00", "00", "00", "00"],
    ["00", "00", "00", "00"],
    ["00", "00", "00", "00"],
    ["00", "00", "00", "00"]
]

    # Process each column
    for col in range(4):
        a0 = theMatrix[0][col]
        a1 = theMatrix[1][col]
        a2 = theMatrix[2][col]
        a3 = theMatrix[3][col]

        # First output byte
        b0 = (
            int(byteMul2(a0), 16) ^
            int(byteMul3(a1), 16) ^
            int(a2, 16) ^
            int(a3, 16)
        )

        # Second output byte
        b1 = (
            int(a0, 16) ^
            int(byteMul2(a1), 16) ^
            int(byteMul3(a2), 16) ^
            int(a3, 16)
        )

        # Third output byte
        b2 = (
            int(a0, 16) ^
            int(a1, 16) ^
            int(byteMul2(a2), 16) ^
            int(byteMul3(a3), 16)
        )

        # Fourth output byte
        b3 = (
            int(byteMul3(a0), 16) ^
            int(a1, 16) ^
            int(a2, 16) ^
            int(byteMul2(a3), 16)
        )

        newMatrix[0][col] = f"{b0:02X}"
        newMatrix[1][col] = f"{b1:02X}"
        newMatrix[2][col] = f"{b2:02X}"
        newMatrix[3][col] = f"{b3:02X}"

    return newMatrix

def shiftRows(theMatrix):
    newMatrix = []
    for index, row in enumerate(theMatrix):
        theShiftConstant = index
        tempRow = ["0", "0", "0", "0"]
        for i, item in enumerate(row):
            newPos = (i - theShiftConstant) % 4
            tempRow[newPos] = item
        newMatrix.append(tempRow)
    return newMatrix
def displayMatrix(m):
    for item in m:
        print(item)




# Code to understand the Word generation process:
def getWord(m, ColIndex):
    wordToBeReturned = []
    for i in range(4):
        wordToBeReturned.append(m[i][ColIndex])
    return wordToBeReturned

def rotWord(word):
    newWord = []
    newWord.append(word[1])
    newWord.append(word[2])
    newWord.append(word[3])
    newWord.append(word[0])
    return newWord

def subWord(word):

    tempList = []
    for item in word:
        tempList.append(SBOX[item])
    return tempList


def makeW4(W0, W3, whatRound):
    wprocesss = rotWord(W3)
    wprocesss = subWord(wprocesss)
    rconArray = [RCon[whatRound], "00", "00", "00"]
    wprocesss = [f"{int(wprocesss[0], 16) ^ int(rconArray[0], 16):02X}",
                  f"{int(wprocesss[1], 16) ^ int(rconArray[1], 16):02X}",
                    f"{int(wprocesss[2], 16) ^ int(rconArray[2], 16):02X}",
                      f"{int(wprocesss[3], 16) ^ int(rconArray[3], 16):02X}"]
    wprocesss = [f"{int(wprocesss[0], 16) ^ int(W0[0], 16):02X}",
                  f"{int(wprocesss[1], 16) ^ int(W0[1], 16):02X}",
                    f"{int(wprocesss[2], 16) ^ int(W0[2], 16):02X}",
                      f"{int(wprocesss[3], 16) ^ int(W0[3], 16):02X}"]
    return wprocesss


def generateRoundKeys(m):
    theWords = []
    for x in range(4):
        theWords.append(getWord(m, x))
    i = 4
    for i in range(4, 44):
        if i % 4 == 0:
            word = makeW4(theWords[i - 4], theWords[i - 1], int(i/4) - 1)
            theWords.append(word)
        else:
            word1 = theWords[i - 4]
            word2 = theWords[i - 1]
            wprocesss = [f"{int(word1[0], 16) ^ int(word2[0], 16):02X}",
                  f"{int(word1[1], 16) ^ int(word2[1], 16):02X}",
                    f"{int(word1[2], 16) ^ int(word2[2], 16):02X}",
                      f"{int(word1[3], 16) ^ int(word2[3], 16):02X}"]
            theWords.append(wprocesss)
    return theWords
def addRoundKey(keyMatrix, State):
    res = []
    for i in range(4):
        currList = []
        for j in range(4):
            currList.append(f"{int(keyMatrix[i][j], 16) ^ int(State[i][j], 16):02X}")
        res.append(currList)
    return res

def completeProcess(theSentence, theKey):
    theSentence = mapping(theSentence)
    print("The mapped Sentence: " + theSentence)
    
    theKey = mapping(theKey)
    print("The mapped Key: " + theKey)

    theKeyMatrix = makeMatrix(theKey)
    print("The key matrix: ")
    displayMatrix(theKeyMatrix)

    theWord = generateRoundKeys(theKeyMatrix)
    for i in range(len(theWord)):
        print(f"W{i}: {theWord[i]}")
    print("")
    theState = makeMatrix(theSentence)
    print("Round 0 The state: ")
    displayMatrix(theState)

    keyStateMatrix = [
    [theWord[0][0], theWord[0 + 1][0], theWord[0 + 2][0], theWord[0 + 3][0]],
    [theWord[0][1], theWord[0 + 1][1], theWord[0 + 2][1], theWord[0 + 3][1]],
    [theWord[0][2], theWord[0 + 1][2], theWord[0 + 2][2], theWord[0 + 3][2]],
    [theWord[0][3], theWord[0 + 1][3], theWord[0 + 2][3], theWord[0 + 3][3]]
]
    theState = addRoundKey(keyStateMatrix, theState)

    print("Round 0 The state After AddRoundKey: ")
    displayMatrix(theState)
    

    for i in range(1, 10):
        
        theState = subByte(theState)
        print(f"Round {i} After sub byte: ")
        displayMatrix(theState)
        theState = shiftRows(theState)
        print(f"Round {i} After shift rows: ")
        displayMatrix(theState)
        theState = mixColumns(theState)
        print(f"Round {i} After Mix Columns: ")
        displayMatrix(theState)

        # Generate the state matrix for the key
        start = i * 4   

        keyStateMatrix = [
        [theWord[start][0], theWord[start + 1][0], theWord[start + 2][0], theWord[start + 3][0]],
        [theWord[start][1], theWord[start + 1][1], theWord[start + 2][1], theWord[start + 3][1]],
        [theWord[start][2], theWord[start + 1][2], theWord[start + 2][2], theWord[start + 3][2]],
        [theWord[start][3], theWord[start + 1][3], theWord[start + 2][3], theWord[start + 3][3]]]
        theState = addRoundKey(keyStateMatrix, theState)
        print(f"Round {i} After AddRoundKey: ")
        displayMatrix(theState)
    
    start = 4 * 10 
    keyStateMatrix = [
        [theWord[start][0], theWord[start + 1][0], theWord[start + 2][0], theWord[start + 3][0]],
        [theWord[start][1], theWord[start + 1][1], theWord[start + 2][1], theWord[start + 3][1]],
        [theWord[start][2], theWord[start + 1][2], theWord[start + 2][2], theWord[start + 3][2]],
        [theWord[start][3], theWord[start + 1][3], theWord[start + 2][3], theWord[start + 3][3]]]
    theState = subByte(theState)
    print(f"Round 10 After sub byte: ")
    displayMatrix(theState)
    theState = shiftRows(theState)
    print(f"Round 10 After shift rows: ")
    displayMatrix(theState)

    theState = addRoundKey(keyStateMatrix, theState)
    print(f"Round 10 After AddRoundKey: ")
    displayMatrix(theState)

#completeProcess("00112233445566778899AABBCCDDEEFF", "000102030405060708090A0B0C0D0E0F")
while True:
    choice = int(input("AES Encryption Program\n1. Encrypt Plaintext using AES\n2. Decrypt Ciphertext using AES\n3. Exit\n"))
    if choice == 1:
        pt = processSentence()
        key = processSentence()
        completeProcess(pt, key)
    elif choice == 2:
        sys.exit()
    else:
        sys.exit()