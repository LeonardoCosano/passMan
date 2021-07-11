# Main file

import random 

# Writes new account to storageFile
def addAccount():
    service = input('Introduce the service: (Google, Facebook, Amazon...)').lower()
    userId = input('Write username: (email or nickname)')
    password = getPassword()

# Returns accounts password
def getPassword():
    option = input('Wanna generate a random secure password? (y/n)')
    if option == "y":
        return generatePassword()
    
    password = input('Type your account´s password')
    confirmation = input ('Is <' + password + '> well typed? (y/n)')
    while confirmation != "n":
        password = input('Type your account´s password')
        confirmation = input ('Is <' + password + '> well typed? (y/n)')
    return password

# Generates a random secure password
def generatePassword():
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z"]
    tokens = ["@", "#", "*", "-", "_", "ç"]
    generatedPassword = ""

    random.seed()
    while generatePassword.length < 20:
        alphaIndex = (random.randint(0,26), False) [random.randint(0,100) > 50]
        alphaIndex = random.randint(0,100) > 50 ? random.randint(0,26) : False
        numberIndex = random.randint(0,100) > 50 ? random.randint(0,9) : False
        tokenIndex = random.randint(0,100) > 50 ? random.randint(0,5) : False

        if alphaIndex.isNumber():



    a = 12345