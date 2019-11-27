# Project-Design-of-Keyboards-and-Other-Interfaces-for-Users-with-Reduced-Capabilities

Includes:

  -SortedDict.txt - A cross referenced result of words sorted by popularity from Peter Norvig's collection of 100k most popular "words" with a text file containing 330k words in alphabetical order from Scrabble, which is recongnised by Oxford Dictionary. Cross checking the text files resulted in this dictionary containing approximately 56k words in order of popularity.
  
  -DictTrie.py - A program that was used to first build the Trie using SortedDict.txt and is used to find the 3 most popular results in the trie when building a word in the Normal Keyboard Program
  
  -EncDictTrie.py - An altered program to that above that works for the encoded keyboard specific rules. Needs to decode the available letters and return the most popular word available within the given code.
  
  -EncodedKey.py - The Encoded Keyboard program, Using the numbers 1-9 (by default) you can type a code to present the 5 most popular words resulting form said code (each number represents all letters seen under it)
   
   >Use Q, W, E, R, T to select which word from the given list you would like to input into the textbox
   
   >If you want to change the number of keys to code with (drag down menu above the suggestions), once you have changed the number press P to refresh the keyboard.
   
   >Edit function not implemented
  
  -NormalKey.py - A normal keyboard GUI, you can type directly to the textbox.
    
   >Whilst typing to the textbox, you can use suggestions of the 3 most popular words using that prefix via 1, 2 or 3 on the keyboard.
   
   >You can enter Edit mode via clicking the edit button, this will allow you to press two keys on the keyboard to swap them on the GUI. After exiting Edit mode via clicking again, all keypresses will respect what is represented in the GUI when typing into the textbox.
   
   >Return to default with \
  


To run either of these programs you will require the following:
 
 -Python3
 
 -tkinter module for Python3 (python3-tk)

Known issues:
  
  -Text wrapping in the textbox, can be fixed with a mod equal to the character length of one line to calculate when a word should be put onto a new line
  
  -Beyond Word Suggestions, When using Encoded Keyboard and a code extends beyond the word listings, it will restart from the next input. This is a simple fix by checking that there is currently a code being typed out
  
  -GUI problems. This program was made for Windows 10, there have been visual issues when running the same program in Linux where buttons overlap, however program is still fully functional
