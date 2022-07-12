from enum import Enum
import os
import random


def rateFax(Message: dict):
    """Rates Fax from render Queue, Pushes to Ready Queue and Archive Collection\n
    Returns Message with rendered statments ranked"""

    def drawScreen() -> dict:
        """Creates UI and returns dictionary of statments ranked"""

        class Draw(Enum):
            Title = """\nRate Statments"""
            Instruct = """\n[Rate which statments are 'Good' when Prompted]\n"""

        def drawPhrases():
            ct = 0
            for Phrase in Message["render"]:
                print(f"    [{ct}] - {Phrase}")
                ct += 1
            print()

        def captureInput(Mod: str = "Good", message: list = Message["render"]) -> dict:

            out = {}
            # Opts is ints of the array values of good statments
            opts = input(f"   Select which statment(s) are '{Mod}'\n").split()

            def autoComplete(Array: list = message, Options: list = opts):
                ct = 0
                out = []
                while ct <= (len(Array) - 1):
                    if str(ct) not in Options:
                        out.append(ct)
                    ct += 1
                return out

            for opt in opts:
                out.update({message[int(opt)]: Mod})
            # Auto Label leftovers as bad
            for opt in autoComplete():
                out.update({message[int(opt)]: "Bad"})

            return out

        # [Draw]
        # Clear Console
        os.system("cls")  #'clear'
        # Draw Title & Intructions
        print(Draw.Title.value, Draw.Instruct.value)
        # Draw Statements
        drawPhrases()
        # Ask Opts
        print("Enter mutliple Options seperated with a space EX: 0 1 2...")
        # Compiles statments and ranks to dictionary
        """ranks = {}
        for Opts in ["Good", "Bad"]:
            ranks.update(captureInput(Opts))"""
        ranks = {}
        ranks.update(captureInput())

        return ranks

    Message["render"] = drawScreen()

    return Message


def askQuit():
    Finals = [
        "I love you <3",
        "Come Back Soon!",
        "lol kek",
        "Don't let the door hit you on the way out!",
        "Please come back and help again!",
        "Dank Memes won't Melt Steel Dreams!",
        "Please tell your friends!",
        "Please tell your friends, I'm a lonely AI :(",
        "Always Welcome back!",
        "Save the Bees!",
        "Farewell!",
        "I'll be watching... <0>|<0>",
        "dOwNLoAd mORe RaM toDaY ?!@#",
    ]
    if input("Want to Continue (ENTER) or Quit (AnyKey)?\n"):
        print(f"Thanks for helping, {random.choice(Finals)}")
        exit()

#askQuit()