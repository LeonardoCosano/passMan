# Main menu

from os import write, system

def main():
    option = writeMenu()
    while option != False:
        if option == 1:
            print ("searchAccount()")
        elif option == 2:
            print ("addAccount()")
        else:
            print ("Leaving")
            exit()
        option = writeMenu()

# Extensible menu: Shows PassMan functionality.
# Returns number related to selected function (or false if something went wrong)
def writeMenu():
    print("\n---------------------\n")
    print("-------PassMan-------\n")
    print("---------------------\n")
    print("1. Search my accounts")
    print("2. Add new accounts")
    option = int(input ("Choose: "))
    if option > 2:
        return False
    return option

if __name__ == "__main__":
    main()