# Main file

from os import write
from types import TracebackType 
from utils import colors
import des as ds
import random
import pyperclip
import des

# Generates a new entry for register
def newAccount():
    service = input('\n\nIntroduce the ' + colors.VIOLET + 'service' + colors.DEFAULT + ': (Google, Facebook, Amazon...) ').lower()
    userId = input('Write ' + colors.VIOLET + 'your username' + colors.DEFAULT + ': (email or nickname) ')
    password = getPassword()

    # Checks wether service is already present or not
    isNewService = False
    storageFile = open('storageFile', 'r')
    if storageFile.read().find(service) == -1:
        isNewService = True
    storageFile.close()

    if checkData(service, userId, password) == True:
        key = input('\nIntroduce a ' + colors.GREEN + 'key' + colors.DEFAULT + ' for DES encryption: ').lower()
        addAccount(isNewService, service, userId, password, key)

# Write new data to storageFile
def addAccount(isNewService, service, userId, password, key):
    #If there is not a previous registry, its added to chat
    if isNewService:
        addStorageFile = open('storageFile', 'a')
        addStorageFile.write("+" + service + "\n-" + userId + "\n" + cipher(password, key) + "\n")
        addStorageFile.close()
        return
    

    # Save text before first service registry
    readStorageFile = open('storageFile', 'r')
    serviceFound = False
    text = ""
    while serviceFound == False:
        nextChar = readStorageFile.read(1)
        text = text + nextChar
        if text.find(service) == True:
            serviceFound = True

    # 
    nextEntryFound = False
    while nextEntryFound == False:
        nextChar = readStorageFile.read(1)
        if nextChar == "+":
            nextEntryFound = True
        else:
            text = text + nextChar
    
    text += "-" + userId + "\n" + cipher(password,key) + "\n+" + readStorageFile.read()
    writeRegister = open("storageFile", "w")
    writeRegister.write(text)
    readStorageFile.close()
    writeRegister.close()
    
# Returns account´s password
# It can be input from user or a randomly generated one
def getPassword():
    option = input('Wanna generate a random password? (y/n) ')
    if option == "y":
        return generatePassword()
    
    password = input('Type ' + colors.VIOLET + 'your password ' + colors.DEFAULT + ': ')
    confirmation = input ('Is ' + colors.GREEN + '<' + password + '>' + colors.DEFAULT + ' well typed? (y/n) ')
    while confirmation != "y":
        password = input('Type ' + colors.VIOLET + 'your password ' + colors.DEFAULT + ': ')
        confirmation = input ('Is ' + colors.GREEN + '<' + password + '>' + colors.DEFAULT + ' well typed? (y/n) ')
    return password

# Generates a random secure password
# It includes letters, numbers and symbols.
def generatePassword():
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]
    # la cecedilla da problemas con des
    tokens = ["@", "#", "*", "<", ">", "ç", "%", "$"]
    generatedPassword = ""

    random.seed()
    while len(generatedPassword) < 20:
        alphaIndex = (random.randint(0,51), False) [random.randint(0,100) > 50]
        numberIndex = (random.randint(0,9), False) [random.randint(0,100) > 50]
        tokenIndex = (random.randint(0,7), False) [random.randint(0,100) > 33]

        if alphaIndex != False:
            generatedPassword = generatedPassword + alphabet[alphaIndex]
        if numberIndex != False:
            generatedPassword = generatedPassword + str(numberIndex)
        if tokenIndex != False:
            generatedPassword = generatedPassword + tokens[tokenIndex]

    print("Generated " + colors.VIOLET + "password: " + colors.DEFAULT + generatedPassword)
    pyperclip.copy(generatedPassword)
    return generatedPassword

# Resumes information about to be registered at local file
# Returns user confirmation
def checkData(service, userId, password):
    print("\nIs everything correct? (y/n)")
    print("Service:\t" + colors.VIOLET + service + colors.DEFAULT)
    print("Username:\t" + colors.VIOLET + userId + colors.DEFAULT)
    confirmation = input("Password:\t" + colors.VIOLET + password + colors.DEFAULT + "\n")

    if confirmation == "y":
        return True
    return False

# Prints user information found after search by service
# Text is complete storageFile info, index is first service ocurrence
def printData(text, index, service, key):
    indexService = index
    indexNextService = text.find("+", indexService+1)
    text = text[indexService:indexNextService]
    nAccounts = text.count("-")

    print(colors.GREEN + "\n~~~~~~~~~~~~~~~~~~~~~")
    print(colors.DEFAULT + "Information found:" + colors.GREEN)
    print("~~~~~~~~~~~~~~~~~~~~~"+ colors.DEFAULT)
    indexEOF = text.find("\n", 1)
    for account in range(nAccounts):
        secondEOF = text.find("\n", indexEOF+1)
        thirdEOF = text.find("\n", secondEOF+1)

        print("Username:\t" + colors.VIOLET + text[indexEOF+2:secondEOF] + colors.DEFAULT)
        secondEOF = text.find("\n", indexEOF+1)
        print("Key:\t\t" + colors.VIOLET + decipher(text[secondEOF+1:thirdEOF], key) + colors.DEFAULT)
        print(colors.GREEN +"~~~~~~~~~~~~~~~~~~~~~"+ colors.DEFAULT)

        indexEOF = thirdEOF

    eof=text.find("\n", 1)




# Encripts text
def cipher(password, key):
    return ds.des(password,key)
    #return password

# Unencripts text
def decipher(password, key):
    return ds.unDes(password,key)
    #return password

def searchAccount():
    service = input('\n\n1. Introduce the ' + colors.VIOLET + 'service' + colors.DEFAULT + ': ').lower()
    storageFile = open('storageFile', 'r')
    text = storageFile.read()
    index = text.find(service)
    if index == -1:
        print("Account" + colors.RED + " not found " + colors.DEFAULT + "for " + service + "\n")
        Exit = input("Press " + colors.VIOLET + "any key" + colors.DEFAULT + " to continue...\n") 
        return
    
    key = input('2. Introduce the ' + colors.VIOLET + 'key' + colors.DEFAULT + ' for DES encryption: ')
    printData(text, index, service, key)
    Exit = input("\nPress " + colors.VIOLET + "any key" + colors.DEFAULT + " to continue...\n")    