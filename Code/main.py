from Jeu.jeu import jeu
from Interface.menu import interface

def main():
    running = True
    skip_intro = False

    while running:
        res = interface(skip_intro=skip_intro)
        skip_intro = False  # reset

        if res is False:
            running = False
        else:
            result = jeu(res)

            if result == "menu":
                skip_intro = True  #
                continue

            elif result == "quit":
                running = False

if __name__ == "__main__":
    main()
