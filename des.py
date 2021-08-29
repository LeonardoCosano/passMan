# Des implementation
import numpy as np
import math

############################
# Runs algorithm - cipher ##
############################

def des(text, key):
    #Inputs and algorithm variables
    InitialPerm = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    InitialPermInv = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
    binaryTextSplited = splitBlocks(text2bin(text))
    binaryKey = formatKey(key)
    binaryCipher = ""

    #Algorithm
    subKeys = splitKey(binaryKey)
    for blocks in range(len(binaryTextSplited)):
        # 1.Initial permutation
        message = applyPerm(binaryTextSplited[blocks], InitialPerm)
        # 2.Feistel rounds (contains 3.switch)
        result64bits = applyFeistelRounds(message,subKeys)
        # 4.Final permutation
        message = applyPerm(result64bits,InitialPermInv)
        # Store block result
        binaryCipher += message
    
    hexadecimalCipher = bin2hex(binaryCipher)
    return hexadecimalCipher

############################
# Runs algorithm decipher ##
############################

def unDes(code, key):
    #Inputs and algorithm variables
    InitialPerm = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    InitialPermInv = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
    code = splitBlocks(checkInput(code))
    binaryKey = formatKey(key)
    resolvedBinary = []

    #Algorithm
    subKeys = flip(splitKey(binaryKey))
    for block in range(len(code)):
        # 1.Initial permutation
        message = applyPerm(code[block],InitialPerm)
        # 2.Feistel rounds (contains 3.switch)
        result64bits = applyFeistelRounds(message,subKeys)
        # 4.Final permutation
        message = applyPerm(result64bits, InitialPermInv)
        # Store block result
        resolvedBinary.append(message)

    resolved = bin2text(''.join(resolvedBinary))
    return resolved
    

############################################################################
############################################################################
############################################################################
########################## Conversiones ####################################
############################################################################
############################################################################
############################################################################


# Converts string into binary
# Returns binary as string
def text2bin(text):
    binaryRepresentation = ""
    array = bytearray(text, "utf8")
    for byte in array:
        binary = bin(byte)[2:]
        while len(binary) < 8:
            binary = "0" + binary
        binaryRepresentation = binaryRepresentation + binary

    return binaryRepresentation

# Converts binary representation into string decimal
def bin2dec(binary):
    return int(binary, 2)

# Converts binary representation into text
def bin2text(binario):
    text = ""
    end = 8
    for i in range(int(len(binario)/8)):
        text += chr(bin2dec(binario[i*8:end]))
        end += 8

    return text

# Converts string binary representation into hexadecimal
# Returns hexadecimal as string
def bin2hex(binary): 
    return hex(int(binary, 2))[2:]

# Converts hexadecimal representation into string binary representation
# Returns binary rep as string
def hex2bin(hexadecimal):
    return dec2bin(int(hexadecimal,16),4*len(hexadecimal))

# Converts decimal representation into string binary
def dec2bin(decimal, size=2):
    binary = bin(decimal)[2:]
    while len(binary)<size:
        binary = "0" + binary
    return binary

def bin2decimal(binary):
    decimal = []
    for i in range(len(binary)):
        bin2decimalBlock(binary[i], decimal)
    
    return decimal

def bin2decimalBlock(binaryString, decimal):
    for i in range(8):
        decimal.append(bin2dec(binaryString[i*8:i*8+8]))


############################################################################
############################################################################
############################################################################
##################### FUNCIONES DEL ALGORITMO ##############################
############################################################################
############################################################################
############################################################################
############################################################################


# Adapts given key to DES algorithm key required (64 bits long)
def formatKey(actualKey):
    binaryKey = text2bin(actualKey)

    while len(binaryKey) < 64:
        binaryKey += binaryKey
    
    return binaryKey[0:64]

# Returns an input into binary, input can be either binary or hexadecimal
def checkInput(code):
    inputType = "bin"
    for letter in range(len(code)):
        if code[letter]!="0" and code[letter]!="1":
            inputType = "hex"

    if inputType == "bin":
        return code
    else: 
        return hex2bin(code)

# Split binary representation "BinaryText" into parts of 64 bits
def splitBlocks(BinaryText):
    nOfBlocks = math.ceil(len(BinaryText)/64)
    mBlocks = []
    for i in range(nOfBlocks):
        mBlocks.append(BinaryText[64*i:64*(i+1)])

    while len(mBlocks[nOfBlocks-1])<64:
    #    mBlocks[nOfBlocks-1] += "1"          
       mBlocks[nOfBlocks-1] += mBlocks[nOfBlocks-1]

    mBlocks[nOfBlocks-1] = mBlocks[nOfBlocks-1][0:64]
    return mBlocks

# It applies a permutation (perm) to a binary string (binary)
def applyPerm(binary, perm):
    binaryPermutated = ""
    for i in range(len(perm)):
        binaryPermutated = binaryPermutated + binary[perm[i]-1]
    
    return binaryPermutated

# Splits the key into 16 subkeys needed for DES
def splitKey(key):
    PermC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    PermC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    subKeys = []
    # 64bits key -> 56bits-key
    Permutation = applyPerm(key, PermC1)
    C0 = Permutation[0:28]
    D0 = Permutation[28:56]

    for subKey in range(16):
        shift = 2
        if subKey == 0 or subKey == 1 or subKey == 8 or subKey == 15:
            shift = 1
        C1 = []
        D1 = []
        C1[:0] = C0
        D1[:0] = D0
        C0 = ''.join(np.roll(C1,28-shift))
        D0 = ''.join(np.roll(D1,28-shift))
        complete = str(C0) + str(D0)
        subKeys.append(applyPerm(complete, PermC2))

    return subKeys

# Applies XOR logic operation
def XOR(one, another):  
    result = ""
    for digit in range(len(one)):
        XOR = bool(float(one[digit])) != bool(float(another[digit]))
        if XOR:
            result += "1"
        else:
            result += "0"
        
    return result

# Applies the DES boxes proccess
def applySBoxes(PartsOfS):
    SBoxesResult = ""
    S1 = [14, 4,   13,  1,   2,   15,  11,  8,   3,   10,  6,   12,  5,   9,   0,   7, 0,    15,  7, 4,     14,   2,  13,  1,    10,  6,  12, 11, 9, 5, 3, 8, 4, 1, 14, 8,	13, 6, 2,	11,	15,	12,	9,	7,	3,	10,	5,	0, 15,	12,	8,	2,	4,	9,	1,	7,	5,	11,	3,	14,	10,	0,	6,	13]
    S2 = [15,	1,	8,	14,	6,	11,	3,	4,	9,	7,	2,	13,	12,	0,	5,	10, 3,	13,	4,	7,	15,	2,	8,	14,	12,	0,	1,	10,	6,	9,	11,	5,0,	14,	7,	11,	10,	4,	13,	1,	5,	8,	12,	6,	9,	3,	2,	15,13,	8,	10,	1,	3,	15,	4,	2,	11,	6,	7,	12,	0,	5,	14,	9]
    S3 = [10,	0,	9,	14,	6,	3,	15,	5,	1,	13,	12,	7,	11,	4,	2,	8,13,	7,	0,	9,	3,	4,	6,	10,	2,	8,	5,	14,	12,	11,	15,	1,13,	6,	4,	9,	8,	15,	3,	0,	11,	1,	2,	12,	5,	10,	14,	7,1,	10,	13,	0,	6,	9,	8,	7,	4,	15,	14,	3,	11,	5,	2,	12]
    S4 = [7,	13,	14,	3,	0,	6,	9,	10,	1,	2,	8,	5,	11,	12,	4,	15,13,	8,	11,	5,	6,	15,	0,	3,	4,	7,	2,	12,	1,	10,	14,	9,10,	6,	9,	0,	12,	11,	7,	13,	15,	1,	3,	14,	5,	2,	8,	4, 3,	15,	0,	6,	10,	1,	13,	8,	9,	4,	5,	11,	12,	7,	2,	14]
    S5 = [2,	12,	4,	1,	7,	10,	11,	6,	8,	5,	3,	15,	13,	0,	14,	9,14,	11,	2,	12,	4,	7,	13,	1,	5,	0,	15,	10,	3,	9,	8,	6,4,	2,	1,	11,	10,	13,	7,	8,	15,	9,	12,	5,	6,	3,	0,	14,11,	8,	12,	7,	1,	14,	2,	13,	6,	15,	0,	9,	10,	4,	5,	3]
    S6 = [12,	1,	10,	15,	9,	2,	6,	8,	0,	13,	3,	4,	14,	7,	5,	11,10,	15,	4,	2,	7,	12,	9,	5,	6,	1,	13,	14,	0,	11,	3,	8,9,	14,	15,	5,	2,	8,	12,	3,	7,	0,	4,	10,	1,	13,	11,	6,4,	3,	2,	12,	9,	5,	15,	10,	11,	14,	1,	7,	6,	0,	8,	13]
    S7 = [4,	11,	2,	14,	15,	0,	8,	13,	3,	12,	9,	7,	5,	10,	6,	1,13,	0,	11,	7,	4,	9,	1,	10,	14,	3,	5,	12,	2,	15,	8,	6,1,	4,	11,	13,	12,	3,	7,	14,	10,	15,	6,	8,	0,	5,	9,	2,6,	11,	13,	8,	1,	4,	10,	7,	9,	5,	0,	15,	14,	2,	3,	12]
    S8 = [13,	2,	8,	4,	6,	15,	11,	1,	10,	9,	3,	14,	5,	0,	12,	7,1,	15,	13,	8,	10,	3,	7,	4,	12,	5,	6,	11,	0,	14,	9,	2,7,	11,	4,	1,	9,	12,	14,	2,	0,	6,	10,	13,	15,	3,	5,	8,2,	1,	14,	7,	4,	10,	8,	13,	15,	12,	9,	0,	3,	5,	6,	11]
    SBoxes = [S1, S2, S3, S4, S5, S6, S7, S8]

    for i in range(8):
        SboxBits = PartsOfS[i]
        row = bin2dec(SboxBits[0]+SboxBits[5])
        col = bin2dec(SboxBits[1:5])

        value = SBoxes[i][row*16+col]
        value = dec2bin(value,4)
        SBoxesResult += value

    return SBoxesResult

# Applies 16 feistel rounds
def applyFeistelRounds(message, subKeys):
    Li = message[0:32]
    Ri = message[32:64]

    for round in range(16):
        Rprev = Ri
        Lprev = Li
        # Feistel function contains 4 steps
        Ri = applyFeistel(Rprev, subKeys[round])
        # 5. Li XOR Ri
        Ri = XOR(Ri, Lprev)
        Li = Rprev

    # 3. Switch
    return Ri + Li

# Applies 1 feistel round
def applyFeistel(Ri, Ki):
    # 1. Expand Ri
    ExpansionPerm = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    Ri = applyPerm(Ri, ExpansionPerm)
    
    # 2. Ri XOR Ki
    xor = XOR(Ri, Ki)

    # 3. Apply sboxes
    partsOfS = []
    start = 0
    for i in range(8):
        partsOfS.append(xor[start:start+6])
        start += 6
    Sboxes = applySBoxes(partsOfS)

    # 4. Apply substitution permutation
    PermP = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    
    return applyPerm(Sboxes, PermP)

# Flips a vector
def flip(array):
    flipedArray = []
    for i in range(16):
        flipedArray.append(array[15-i])
    
    return flipedArray


############################################################################
############################################################################
############################################################################
############################################################################
############################# DEBUGGING ####################################
############################################################################
############################################################################
############################################################################


def main():
    mensaje = "sepalosepalo"
    clave = "oculta2"
    #claveIncorrecta = "LEONARDO"
    
    cifrado = des(mensaje, clave)
    descifradoCorrecto = unDes(cifrado, clave)
    #descifradoIncorrecto = unDes(cifrado, claveIncorrecta)

    print("\nCIFRADO COMPLETADO --->" + cifrado + "<---\n")
    print("DESCIFRADO CORRECTO --->" + descifradoCorrecto + "<---\n")
    #print("DESCIFRADO INCORRECTO --->" + descifradoIncorrecto + "<---\n")


if __name__ == "__main__":
    main()