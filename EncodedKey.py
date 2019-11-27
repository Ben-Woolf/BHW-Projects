from tkinter import *
import EncDictTrie
import time
import math

root = Tk()
root.title("Encoded Keyboard")
root.geometry("800x600")

class keyCode():
    def __init__(self):
        self.keyOrder = [['a', 'a', 0], ['b', 'b', 0], ['c', 'c', 0], ['d', 'd', 0], ['e', 'e', 0], ['f', 'f', 0],
                         ['g', 'g', 0], ['h', 'h', 0], ['i', 'i', 0], ['j', 'j', 0], ['k', 'k', 0], ['l', 'l', 0],
                         ['m', 'm', 0], ['n', 'n', 0], ['o', 'o', 0], ['p', 'p', 0], ['q', 'q', 0], ['r', 'r', 0],
                         ['s', 's', 0], ['t', 't', 0], ['u', 'u', 0], ['v', 'v', 0], ['w', 'w', 0], ['x', 'x', 0],
                         ['y', 'y', 0], ['z', 'z', 0]]

        self.keyButton = []                          # List of list, each inner list responds to number button

        self.keyStrings = []

        self.NumofKeys = 9
        self.dropMenuVar = StringVar(root)
        self.dropMenuVar.set("Select Number of Buttons")
        self.currentString = "Type Here -----> "
        self.textOut = "---\n---\n---\n---\n---"
        self.editMode = False
        self.code = ""
        self.codePermu = []
        self.prevPermu = []
        self.permDepth = 0
        self.genKeys()
        self.predResults = []
        self.swapKey = -1

        self.renderMain()

    def enableEdit(self):
        for e in range(len(self.keyOrder)):
            if self.keyOrder[e][2] != 0:
                self.keyOrder[e][2] = 0
        self.swapKey = -1
        self.editMode = not self.editMode
        if self.editMode:
            self.renderEdit()

    def insertCode(self, encode):
        if ord(encode) == 8:
            if len(self.code) > 1:
                self.code = self.code[:-1]
                self.codePermu = self.prevPermu[len(self.code)-1]
                self.prevPermu = self.prevPermu[:-1]
                self.getPred()
            else:
                self.code = ""
                self.codePermu = []
                self.prevPermu = []
                self.textOut = "---\n---\n---\n---\n---"
        else:
            try:
                self.code += str(encode)
                if len(self.codePermu) < 1:
                    for i in range(len(self.keyButton[int(encode)-1])):
                        self.codePermu.append(str(self.keyButton[int(encode)-1][i]))
                else:
                    tempPermu = []
                    for j in range(len(self.codePermu)):
                        if self.codePermu[j] is not None:
                            for i in range(len(self.keyButton[int(encode)-1])):
                                tempPermu.append(str(self.codePermu[j]) + str(self.keyButton[int(encode)-1][i]))
                    self.codePermu = tempPermu
            except IndexError:
                pass
            self.prevPermu.append(self.codePermu)
            self.getPred()

    def getPred(self):
        self.predResults = []
        for i in range(len(self.codePermu)):
            if len(self.predResults) < 1 and self.codePermu[i] is not None:
                tempResults = EncDictTrie.trie.preWord(self.codePermu[i])
                if tempResults[0][0] == "---":
                    self.codePermu[i] = None
                else:
                    self.predResults = tempResults
            else:
                if self.codePermu[i] is not None:
                    tempResults = EncDictTrie.trie.preWord(self.codePermu[i])
                    # print(tempResults)
                    if tempResults[0][0] == "---":
                        self.codePermu[i] = None
                    else:
                        for j in range(len(tempResults[0])):
                            for n in range(len(self.predResults[0])):
                                if int(tempResults[1][j]) < int(self.predResults[1][n]):
                                    for m in range(4, n, -1):
                                        tempShift = [self.predResults[0][m-1], self.predResults[1][m-1]]
                                        self.predResults[0][m] = str(tempShift[0])
                                        self.predResults[1][m] = str(tempShift[1])
                                    self.predResults[1][n] = tempResults[1][j]
                                    self.predResults[0][n] = tempResults[0][j]
                                    break
            # print(" ")

        self.codePermu = list(filter(lambda x: x is not None, self.codePermu))
        # print(self.codePermu)
        # print(self.predResults)
        # print("\n")
        if len(self.predResults) > 0:
            self.textOut = (str(self.predResults[0][0]) + "\n" + str(self.predResults[0][1]) + "\n" +
                            str(self.predResults[0][2]) + "\n" + str(self.predResults[0][3]) + "\n" +
                            str(self.predResults[0][4]))
        else:
            self.textOut = "---\n---\n---\n---\n---"

    def redoKeys(self):
        if self.dropMenuVar.get() == "Four":
            self.NumofKeys = 4
        elif self.dropMenuVar.get() == "Five":
            self.NumofKeys = 5
        elif self.dropMenuVar.get() == "Six":
            self.NumofKeys = 6
        elif self.dropMenuVar.get() == "Seven":
            self.NumofKeys = 7
        elif self.dropMenuVar.get() == "Eight":
            self.NumofKeys = 8
        elif self.dropMenuVar.get() == "Nine":
            self.NumofKeys = 9
        self.keyButton = []
        self.keyStrings = []
        self.code = ""
        self.codePermu = []
        self.prevPermu = []
        self.permDepth = 0
        self.textOut = "---\n---\n---\n---\n---"
        self.predResults = []
        self.genKeys()
        self.renderMain()

    def genKeys(self):
        temp = divmod(26,self.NumofKeys)
        NumofChar = temp[0]
        overflowKeys = self.NumofKeys - temp[1]
        currentKey = 0
        currentButton = 0
        for i in range(self.NumofKeys):
            self.keyStrings.append("")
            tempKeyList = []
            if currentButton < overflowKeys:
                for j in range(NumofChar):
                    tempKeyList.append(str(self.keyOrder[currentKey][1]))
                    self.keyStrings[i] += str(self.keyOrder[currentKey][1])
                    currentKey += 1
            else:
                for j in range(NumofChar + 1):
                    tempKeyList.append(str(self.keyOrder[currentKey][1]))
                    self.keyStrings[i] += str(self.keyOrder[currentKey][1])
                    currentKey += 1
            currentButton += 1
            self.keyButton.append(tempKeyList)

    def mouseClick(self, event):
        pass

    def keyPress(self, event):
        try:
            if len(event.char) > 0:
                if ord(event.char) >= 49 and ord(event.char) <= 57 and self.NumofKeys >= int(event.char) and not self.editMode:
                    self.insertCode(event.char)
                elif ord(event.char) == 8:
                    if len(self.code) > 0:
                        self.insertCode(chr(8))
                    else:
                        for i in range(len(str(self.currentString))-2, 0, -1):
                            if self.currentString[i] == " ":
                                self.currentString = self.currentString[:i+1]
                                break

                elif ord(event.char) == 96:
                    self.enableEdit()

                elif ord(event.char) == 112:
                    self.redoKeys()

                elif len(self.predResults) > 0 or self.predResults[0][0] != "---":
                    if ord(event.char) == 113 and self.predResults[0][0] != "---":
                        self.currentString = self.currentString + str(self.predResults[0][0] + " ")
                        self.code = ""
                        self.codePermu = []
                        self.prevPermu = []
                        self.predResults = []
                        self.textOut = "---\n---\n---\n---\n---"

                    elif ord(event.char) == 119 and self.predResults[0][1] != "---":
                        self.currentString = self.currentString + str(self.predResults[0][1] + " ")
                        self.code = ""
                        self.codePermu = []
                        self.prevPermu = []
                        self.predResults = []
                        self.textOut = "---\n---\n---\n---\n---"

                    elif ord(event.char) == 101 and self.predResults[0][2] != "---":
                        self.currentString = self.currentString + str(self.predResults[0][2] + " ")
                        self.code = ""
                        self.codePermu = []
                        self.prevPermu = []
                        self.predResults = []
                        self.textOut = "---\n---\n---\n---\n---"

                    elif ord(event.char) == 114 and self.predResults[0][3] != "---":
                        self.currentString = self.currentString + str(self.predResults[0][3] + " ")
                        self.code = ""
                        self.codePermu = []
                        self.prevPermu = []
                        self.predResults = []
                        self.textOut = "---\n---\n---\n---\n---"

                    elif ord(event.char) == 116 and self.predResults[0][4] != "---":
                        self.currentString = self.currentString + str(self.predResults[0][4] + " ")
                        self.code = ""
                        self.codePermu = []
                        self.prevPermu = []
                        self.predResults = []
                        self.textOut = "---\n---\n---\n---\n---"

        except AttributeError:
            pass
        except IndexError:
            pass
        self.renderMain()

    def renderMain(self):
        t = Text(root, width=98, height=22, bg="White")
        t.place(x=5, y=5)
        t.insert(END, str(self.currentString))

        Label(relief="groove", text="Code: " + str(self.code), font=("Arial", 13), width=20, height=2, bg="White", anchor=W,
              justify=LEFT).place(x=195, y=365)

        Label(text="Edit", relief=RAISED, width=4, height=2, bg="Green" if self.editMode else "Red", fg="Black").place(
            x=5, y=365)

        OptionMenu(root, self.dropMenuVar, "Four", "Five", "Six", "Seven", "Eight", "Nine").place(x=580, y=365)

        if self.NumofKeys > 0:
            Label(relief=RIDGE, text="1\n" + str(self.keyStrings[0]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=5, y=413)

        if self.NumofKeys > 1:
            Label(relief=RIDGE, text="2\n" + str(self.keyStrings[1]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=195, y=413)

        if self.NumofKeys > 2:
            Label(relief=RIDGE, text="3\n" + str(self.keyStrings[2]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=385, y=413)

        if self.NumofKeys > 3:
            Label(relief=RIDGE, text="4\n" + str(self.keyStrings[3]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=5, y=473)

        if self.NumofKeys > 4:
            Label(relief=RIDGE, text="5\n" + str(self.keyStrings[4]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=195, y=473)
        else:
            Label(relief=RIDGE, width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=195, y=473)

        if self.NumofKeys > 5:
            Label(relief=RIDGE, text="6\n" + str(self.keyStrings[5]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=385, y=473)
        else:
            Label(relief=RIDGE, width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=385, y=473)

        if self.NumofKeys > 6:
            Label(relief=RIDGE, text="7\n" + str(self.keyStrings[6]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=5, y=533)
        else:
            Label(relief=RIDGE, width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=5, y=533)

        if self.NumofKeys > 7:
            Label(relief=RIDGE, text="8\n" + str(self.keyStrings[7]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=195, y=533)
        else:
            Label(relief=RIDGE, width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=195, y=533)

        if self.NumofKeys > 8:
            Label(relief=RIDGE, text="9\n" + str(self.keyStrings[8]), width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=385, y=533)
        else:
            Label(relief=RIDGE, width=18, height=2, font=("Comic Sans MS", 12),
                  bg="White").place(x=385, y=533)

        Label(relief=RIDGE, text="Q", width=2,height=1, font=("Comic Sans MS", 16), bg="Light Grey").place(x=580, y=412)
        Label(relief=RIDGE, text="W", width=2, height=1, font=("Comic Sans MS", 16), bg="Light Grey").place(x=580, y=447)
        Label(relief=RIDGE, text="E", width=2, height=1, font=("Comic Sans MS", 16), bg="Light Grey").place(x=580, y=482)
        Label(relief=RIDGE, text="R", width=2, height=1, font=("Comic Sans MS", 16), bg="Light Grey").place(x=580, y=517)
        Label(relief=RIDGE, text="T", width=2, height=1, font=("Comic Sans MS", 16), bg="Light Grey").place(x=580, y=552)
        p1 = Text(root, width=11, height=5, font=("Comic Sans MS", 18), bg="White")
        p1.place(x=620, y=412)
        p1.insert(END, str(self.textOut))


    def renderEdit(self):
        pass
        ## This was for a second window for the edit function
        # editroot = Tk()
        # editroot.title("Edit Keybinds")
        # editroot.geometry("600x200")
        #
        # posX = 0
        # editroot.Label(relief=RAISED, width=2, height=2, bg="Grey").place(x=5, y=5)
        # for k in range(10):
        #     editroot.Label(text=str(self.keyOrder[k][1]).upper(), relief=RIDGE, width=5, height=2, font=("Comic Sans MS", 10),
        #           bg="White" if self.keyOrder[k][2] == 0 else "Yellow", fg="Black").place(x=30 + posX, y=410)
        #     posX += 50
        #     editroot.Label(relief=RAISED, width=2, height=2, bg="Grey").place(x=30 + posX, y=5)
        #
        # posX = 0
        # editroot.Label(relief=RAISED, width=5, height=2, bg="Grey").place(x=5, y=55)
        # for k in range(9):
        #     editroot.Label(text=str(self.keyOrder[k + 10][1]).upper(), relief=RIDGE, width=5, height=2,
        #           font=("Comic Sans MS", 10),
        #           bg="White" if self.keyOrder[k + 10][2] == 0 else "Yellow", fg="Black").place(x=55 + posX, y=50)
        #     posX += 50
        #     editroot.Label(relief=RAISED, width=5, height=2, bg="Grey").place(x=60 + posX, y=55)
        #
        # posX = 0
        # editroot.Label(relief=RAISED, width=8, height=2, bg="Grey").place(x=5, y=105)
        # for k in range(7):
        #     editroot.Label(text=str(self.keyOrder[k + 19][1]).upper(), relief=RIDGE, width=5, height=2,
        #           font=("Comic Sans MS", 10),
        #           bg="White" if self.keyOrder[k + 19][2] == 0 else "Yellow", fg="Black").place(x=75 + posX, y=100)
        #     posX += 50
        #     editroot.Label(relief=RAISED, width=16, height=2, bg="Grey").place(x=80 + posX, y=105)
        #
        # if editroot.quit():
        #     self.editMode = not self.editMode

kb = keyCode()
root.bind("<Key>", kb.keyPress)
root.bind("<Button-1>", kb.mouseClick)
root.mainloop()