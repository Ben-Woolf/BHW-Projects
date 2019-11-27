class treeNode:
        def __init__(self):
            self.item = None
            self.dictword = None
            self.freq = None
            self.children = []
            for _ in range(27):
                self.children.append(0)

class Tree:
    def __init__(self):
        self.root = treeNode()

    def newWord(self, word, freq):
        current = self.root
        for letter in word[0]:
            if current.children[ord(letter) - 97] != 0:
                current = current.children[ord(letter) - 97]
            else:
                newNode = treeNode()
                newNode.item = letter
                current.children[ord(letter) - 97] = newNode
                current = current.children[ord(letter) - 97]
        if current.freq is None:
            current.dictword = word
            current.freq = freq
            current.children[26] = '$'
        elif int(current.freq) < int(current.freq):
            current.dictword = word
            current.freq = freq
            current.children[26] = '$'

    def preWord(self, pre):
        current = self.root
        results = []
        inc = ''

        top3Word = []
        top3Word.append("---")
        top3Word.append("---")
        top3Word.append("---")
        top3Freq = []
        top3Freq.append(1000000)
        top3Freq.append(1000000)
        top3Freq.append(1000000)

        for letter in pre:
            inc = letter
            if letter == None:
                break
            try:
                if current.children[ord(letter)-97].item == letter:
                    current = current.children[ord(letter)-97]
            except AttributeError:
                break
            except IndexError:
                break
        if current.item == inc:
            results.append(self.auxWord(current, results))
            results.__delitem__(len(results)-1)
            print(len(results))
            if len(results) > 0:

                for p in range(len(results)):
                    for f in range(len(top3Freq)):
                        if int(results[p][1]) < int(top3Freq[f]):
                            top3Word.insert(f, results[p][0])
                            del top3Word[-1]
                            top3Freq.insert(f, results[p][1])
                            del top3Freq[-1]
                            break
        return top3Word

    def auxWord(self, current, results):
        try:
            if current.children[26] == '$':
                temp = []
                temp.append(str(current.dictword[0]))
                temp.append(str(current.freq))
                results.append(temp)
            for i in range(len(current.children)-2):
                if current.children[i] is not None:
                    self.auxWord(current.children[i], results)
        except AttributeError:
            pass
        return results

words = []
word = []
wcount = 1
try:
    f = open('SortedDict.txt', 'r')
    for line in f:
        word = line.split()
        words.append([word, wcount])
        wcount += 1
    f.close()
except IOError:
    print('? Text not Found ?')

trie = Tree()

for i in range(len(words)):
    trie.newWord(words[i][0], words[i][1])

# print(trie.preWord("the"))