import sys
import os
import string
import collections
import re
import decimal
from decimal import Decimal as dec

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
    # For each subdirectory passed by the command line
    for subdir in sys.argv[1:]:
        # Go into each file.
        for root, dirs, files in os.walk(subdir, topdown=True):
            for file in files:
                process_file(root, file)

def process_file(folder, file_name): 
    path = "{}/{}".format(folder, file_name)
    file = open(path, 'r')
    
    record = dict() # Create an empty dictionary
    for line in file:
        words_by_spaces = line.decode("utf-8").split(" ") # Get a list of words by tokenizing by spaces

        # Tokenize by punctuation too just in case a text does something like (this).
        # Simply removing the punctuation could cause a word to blend together with another

        words = list() 
        for w in words_by_spaces:
            words.extend(re.split('[{}]+'.format(string.punctuation), w)) 
        
        for word in words: # Tokenize the words in each line with the delimiter being a space.
            # Prepare this word for counting
            word = word.strip() # get rid of whitespace, tabs, and newlines
            word = word.lower() # get rid of capital letters
            
            if word != "": # Ignore new lines as being words.
                if word in record:
                    record[word] += 1
                else:
                    record[word] = 1
    
    file.close() # Close the file. We're done here.

    # Begin graphing
    words = record.keys()
    num_words = len(words)
    percentages = map(lambda word: dec(record[word]) / dec(num_words), words)

    y_pos = np.arange(num_words)

    plt.barh(y_pos, percentages)
    plt.yticks(y_pos, words)
    plt.xlabel("Percentage")
    plt.ylabel("Words")
    plt.title("Discrete distribution of {}".format(file_name))

    plt.savefig("{}/{}_hist.png".format(folder, os.path.splitext(file_name)[0])) # Save the file as FILE_hist.png. 

if __name__ == "__main__":
    main()


