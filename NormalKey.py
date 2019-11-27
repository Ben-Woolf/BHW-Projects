from tkinter import *
import time
import DictTrie

root = Tk()
root.title("Class and Keybinds")
root.geometry("800x600")

class keyTable():
    def __init__(self):
        self.keyBinds = [['q', 'q', 0], ['w', 'w', 0], ['e', 'e', 0], ['r', 'r', 0], ['t', 't', 0], ['y', 'y', 0], ['u', 'u', 0], ['i', 'i', 0],
                         ['o', 'o', 0], ['p', 'p', 0], ['a', 'a', 0], ['s', 's', 0], ['d', 'd', 0], ['f', 'f', 0], ['g', 'g', 0], ['h', 'h', 0],
                         ['j', 'j', 0], ['k', 'k', 0], ['l', 'l', 0], ['z', 'z', 0], ['x', 'x', 0], ['c', 'c', 0], ['v', 'v', 0], ['b', 'b', 0],
                         ['n', 'n', 0], ['m', 'm', 0]]
        self.defaultKeys = [['q', 'q', 0], ['w', 'w', 0], ['e', 'e', 0], ['r', 'r', 0], ['t', 't', 0], ['y', 'y', 0],
                            ['u', 'u', 0], ['i', 'i', 0], ['o', 'o', 0], ['p', 'p', 0], ['a', 'a', 0], ['s', 's', 0],
                            ['d', 'd', 0], ['f', 'f', 0], ['g', 'g', 0], ['h', 'h', 0], ['j', 'j', 0], ['k', 'k', 0],
                            ['l', 'l', 0], ['z', 'z', 0], ['x', 'x', 0], ['c', 'c', 0], ['v', 'v', 0], ['b', 'b', 0],
                            ['n', 'n', 0], ['m', 'm', 0]]
        self.undoList = []
        self.currentString = "Type Here ----> "
        self.textPred1 = "---"
        self.textPred2 = "---"
        self.textPred3 = "---"
        self.textPreds = "---\n---\n---"
        self.editMode = False
        self.swapChar = ""
        self.swapKey = -1
        self.word = ""
        self.render()

    def enableEdit(self):
        for e in range(len(self.keyBinds)):
            if self.keyBinds[e][2] != 0:
                self.keyBinds[e][2] = 0
        self.swapKey = -1
        self.editMode = not self.editMode
        # print(self.editMode)

    def insertChar(self, nextchar):
        if ord(nextchar) == 8:
            self.word = self.word[:-1]
            self.getPred((self.word))
        elif ord(nextchar) == 32:
            self.currentString += str(nextchar)
            self.word = ""
            self.textPreds = "---\n---\n---"
        else:
            self.currentString += str(nextchar)
            self.word += str(nextchar.lower())
            self.getPred((self.word))
        # print(self.word)

    def getPred(self, pre):
        startTime = time.time()
        results = DictTrie.trie.preWord(str(pre))
        self.textPred1 = str(results[0])
        self.textPred2 = str(results[1])
        self.textPred3 = str(results[2])
        self.textPreds = str(self.textPred1 + "\n" + self.textPred2 + "\n" + self.textPred3)
        print(str(pre) + " time taken " + str((time.time() - startTime)*100) + " ms")
        # print(self.word)
        # print(self.textPreds + "\n")

    def keyPress(self, event):
        if len(event.char) > 0:
            if ((ord(event.char) >= 65 and ord(event.char) <= 90) or (ord(event.char) >= 97 and ord(event.char) <= 122)) and not self.editMode:
                for k in range(len(self.keyBinds)):
                    if str(event.char) == str(self.keyBinds[k][0]):
                        self.insertChar(str(self.keyBinds[k][1]))
                        break
                    elif str(event.char) == str(self.keyBinds[k][0]).upper():
                        self.insertChar(str(self.keyBinds[k][1]).upper())
                        break
            elif ((ord(event.char) >= 65 and ord(event.char) <= 90) or (ord(event.char) >= 97 and ord(event.char) <= 122)) and self.editMode:
                if self.swapKey == -1:
                    for k in range(len(self.keyBinds)):
                        if (str(event.char) == str(self.keyBinds[k][0])) and self.keyBinds[k][2] == 0:
                            self.keyBinds[k][2] = 1
                            self.swapChar = self.keyBinds[k][1]
                            self.swapKey = k
                            break
                else:
                    for k in range(len(self.keyBinds)):
                        if (str(event.char) == str(self.keyBinds[k][0])) and not self.keyBinds[k][2] == 1:
                            self.undoList.append([self.keyBinds[self.swapKey][0], self.keyBinds[k][0]])
                            self.keyBinds[self.swapKey][2] = 0
                            self.keyBinds[self.swapKey][1] = self.keyBinds[k][1]
                            self.keyBinds[k][1] = self.swapChar
                            self.swapKey = -1
                            break
            elif ord(event.char) == 8:
                self.currentString = self.currentString[:-1]
                self.insertChar(chr(8))
            elif ord(event.char) == 32:
                self.insertChar(chr(32))
            elif ord(event.char) == 96:
                self.enableEdit()
            elif ord(event.char) == 49 and self.textPred1 != "---":
                self.currentString = self.currentString + str(self.textPred1[len(self.word):len(self.textPred1)] + " ")
                self.word = ""
                self.textPred1 = "---"
                self.textPreds = "---\n---\n---"
            elif ord(event.char) == 50 and self.textPred2 != "---":
                self.currentString = self.currentString + str(self.textPred2[len(self.word):len(self.textPred2)] + " ")
                self.word = ""
                self.textPred2 = "---"
                self.textPreds = "---\n---\n---"
            elif ord(event.char) == 51 and self.textPred3 != "---":
                self.currentString = self.currentString + str(self.textPred3[len(self.word):len(self.textPred3)] + " ")
                self.word = ""
                self.textPred3 = "---"
                self.textPreds = "---\n---\n---"
            elif ord(event.char) == 92:
                if len(self.undoList) > 0:
                    swapNum1 = -1
                    swapNum2 = -1
                    swapTemp = ''
                    undoTemp = self.undoList[-1]
                    for i in range(len(self.keyBinds)):
                        if undoTemp[0] == self.keyBinds[i][0]:
                            swapNum1 = i
                            break
                    for j in range(len(self.keyBinds)):
                        if undoTemp[1] == self.keyBinds[j][0]:
                            swapNum2 = j
                            break
                    swapTemp = self.keyBinds[swapNum1][1]
                    self.keyBinds[swapNum1][1] = self.keyBinds[swapNum2][1]
                    self.keyBinds[swapNum2][1] = swapTemp
                    self.undoList = self.undoList[:-1]
                    print(self.undoList)
            elif ord(event.char) == 47:
                self.keyBinds = self.defaultKeys
                self.undoList = []
        self.render()

    def mouseClick(self, event):
        # print("x = %s, y = %s" % (event.x, event.y))
        if event.x > 0 and event.x < 35 and event.y > 0 and event.y < 35:
            self.enableEdit()
        self.render()

    def render(self):
        posX = 0
        t = Text(root, width=98, height=25, bg="White")
        t.place(x=5, y=5)
        t.insert(END, str(self.currentString))
        # t.insert(END, "Dummy")

        Label(relief=RAISED, width=2, height=2, bg="Grey").place(x=5, y=413)
        for k in range(10):
            Label(text=str(self.keyBinds[k][1]).upper(), relief=RIDGE, width=5, height=2, font=("Comic Sans MS", 10),
                  bg="White" if self.keyBinds[k][2] == 0 else "Yellow", fg="Black").place(x=30 + posX, y=410)
            posX += 50
        Label(relief=RAISED, width=2, height=2, bg="Grey").place(x=30+posX, y=413)

        posX = 0
        Label(relief=RAISED, width=5, height=2, bg="Grey").place(x=5, y=463)
        for k in range(9):
            Label(text=str(self.keyBinds[k+10][1]).upper(), relief=RIDGE, width=5, height=2, font=("Comic Sans MS", 10),
                  bg="White" if self.keyBinds[k+10][2] == 0 else "Yellow", fg="Black").place(x=55 + posX, y=460)
            posX += 50
        Label(relief=RAISED, width=5, height=2, bg="Grey").place(x=60+posX, y=463)

        posX = 0
        Label(relief=RAISED, width=8, height=2, bg="Grey").place(x=5, y=513)
        for k in range(7):
            Label(text=str(self.keyBinds[k+19][1]).upper(), relief=RIDGE, width=5, height=2, font=("Comic Sans MS", 10),
                  bg="White" if self.keyBinds[k+19][2] == 0 else "Yellow", fg="Black").place(x=75 + posX, y=510)
            posX += 50
        Label(relief=RAISED, width=16, height=2, bg="Grey").place(x=80+posX, y=513)

        Label(text="Edit", relief=RAISED, width=4, height=2, bg="Green" if self.editMode else "Red", fg="Black").place(x=5, y=555)

        p1 = Text(root, width=14, height=3, font=("Comic Sans MS", 18), bg="White")
        p1.place(x=580, y=412)
        p1.insert(END, str(self.textPreds))
        # p1.insert(END, "---\n---\n---")





kb = keyTable()
root.bind("<Key>", kb.keyPress)
root.bind("<Button-1>", kb.mouseClick)
root.mainloop()