'''
Contains methods to help you better visualize the information displayed in the console.
'''
import os


def clear():
    '''
    Clears the console.
    '''
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    '''
    Pauses the console.
    '''
    input("Press ENTER to continue...")
