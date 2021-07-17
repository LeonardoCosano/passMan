# Main menu

from main import newAccount, searchAccount
from os import write, system
from utils import colors

def main():
    option = writeMenu()
    while option != False:
        if option == 1:
            searchAccount()
        elif option == 2:
            newAccount()
        else:
            exit()
        option = writeMenu()

# Extensible menu: Shows PassMan functionality.
# Returns number related to selected function (or false if something went wrong)
def writeMenu():
    system("cls")
    print(colors.GREEN + "\n~~~~~~~~~~~~~~~~~~~~~\n")
    print("~~~~~~" + colors.VIOLET + " PassMan " + colors.GREEN + "~~~~~~\n")
    print("~~~~~~~~~~~~~~~~~~~~~\n" + colors.DEFAULT)
    print("1. Search accounts")
    print("2. Add new account")        
    option = int(input ("Choose: "))
    if option > 2:
        return False
    return option

if __name__ == "__main__":
    main()