# Main file

from os import write
import random
from types import TracebackType 

# Generates a new entry for register
def newAccount():
    service = input('Introduce the service: (Google, Facebook, Amazon...)').lower()
    userId = input('Write username: (email or nickname)')
    password = getPassword()

    # Checks wether service is already present or not
    isNewService = False
    storageFile = open('storageFile', 'r')
    if storageFile.read().find(service) == -1:
        isNewService = True
    storageFile.close()

    addAccount(isNewService, service, userId, password)

# Write new data to storageFile
def addAccount(isNewService, service, userId, password):
    addStorageFile = open('storageFile', 'a')
    if isNewService:
        addStorageFile.write("\n+" + service + "\n-" + userId + "\n" + cipher(password))
        addStorageFile.close()
        return
    
    readStorageFile = open('storageFile', 'r')
    text = ""
    serviceFound = False
    while serviceFound == False:
        nextChar = readStorageFile.read(1)
        text = text + nextChar
        if text.find(service) == True:
            serviceFound = True

    nextEntryFound = False
    while nextEntryFound == False:
        nextChar = readStorageFile.read(1)
        if nextChar == "+":
            nextEntryFound = True
        else:
            text = text + nextChar
    
    text = text + "-" + userId + "\n" + cipher(password) + "\n+" + readStorageFile.read()

    
    writeRegister = open("storageFile", "w")
    writeRegister.write(text)
    readStorageFile.close()
    writeRegister.close()
    
# Returns account´s password
# It can be input from user or a randomly generated one
def getPassword():
    option = input('Wanna generate a random secure password? (y/n)')
    if option == "y":
        return generatePassword()
    
    password = input('Type your account´s password')
    confirmation = input ('Is <' + password + '> well typed? (y/n)')
    while confirmation != "y":
        password = input('Type your account´s password')
        confirmation = input ('Is <' + password + '> well typed? (y/n)')
    return password

# Generates a random secure password
# It includes letters, numbers and symbols.
def generatePassword():
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]
    tokens = ["@", "#", "*", "-", "_", "ç", "%", "$"]
    generatedPassword = ""

    random.seed()
    while len(generatedPassword) < 20:
        alphaIndex = (random.randint(0,52), False) [random.randint(0,100) > 50]
        numberIndex = (random.randint(0,9), False) [random.randint(0,100) > 50]
        tokenIndex = (random.randint(0,7), False) [random.randint(0,100) > 50]

        if alphaIndex != False:
            generatedPassword = generatedPassword + alphabet[alphaIndex]
        if numberIndex != False:
            generatedPassword = generatedPassword + str(numberIndex)
        if tokenIndex != False:
            generatedPassword = generatedPassword + tokens[tokenIndex]

    print("Save it carefully: " + generatedPassword)
    return generatedPassword

# Sets encryption
def cipher(password):
    return password