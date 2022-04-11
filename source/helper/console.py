import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input('Press ENTER to continue...')
