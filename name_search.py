import numpy as np 
import argparse
import string

class NameSearch:

    def __init__(self, Name_List, Name_Algorithm, Name_Length):
        # Matrix of the word search puzzle 
        self.matrix = np.load("./data/matrix.npy")
        # Name of the algorithm
        self.Name_Algorithm = Name_Algorithm
        # Length of the name
        self.Name_Length = Name_Length
        # List of all potential names 
        with open("./data/names/"+Name_List+".txt", 'r') as f:
            self.names = f.read().splitlines()
        self.names = [n.upper().strip() for n in self.names]

        # Shift table
        self.shift_table = dict.fromkeys(string.ascii_uppercase, 0)

        # Number of columns and rows in the matrix
        self.n_rows, self.n_cols = self.matrix.shape

    def match_BruteForce(self, pattern, text):
        # String matching by brute force
        # we get each letter in the text and get each letter in the pattern and compare it one by one

        index = 0 # this is the index of pattern to move through the name
        for letter in text:
            if letter == pattern[index]:
                index += 1
            else:
                index = 0
            if index == len(pattern):
                print('Using', self.Name_Algorithm, 'the length of the name is', index, 'and the name is', pattern)
                break

    def match_Horspool(self, pattern, text):
        # String matching by Horspool's algorithm

        # looping through the shift table to initialize its values correctly
        table_size = len(self.shift_table) # 26
        pattern_size = len(pattern) # pattern's length m in the pseudocode given
        for i in range(0, table_size):
            # Changing i to a character alphabet by using the chr function (A is 65, B is 66)
            self.shift_table[chr(i + 65)] = pattern_size
            for j in range(0, pattern_size-1):
                self.shift_table[pattern[j]] = pattern_size - 1 - j

        index = pattern_size - 1 # position of the pattern's right end

        while index <= (len(text) - 1):
            matched = 0 # Number of matched characters
            while matched <= pattern_size-1 and pattern[pattern_size - 1 - matched] == text[index - matched]:
                matched += 1
            if matched == pattern_size:
                # prints out the name because the return statement just returns a number
                print('Using', self.Name_Algorithm, 'the length of the name is', matched, 'and the name is', pattern)
                return index - (pattern_size+1)
            else:
                index += self.shift_table[text[index]]
        return -1

    def calc_row(self, matrix, row):
        text = ''
        for col in range(self.n_cols):
            text += matrix[row, col]
        return text

    def calc_col(self, matrix, col):
        text = ''
        for row in range(self.n_rows):
            text += matrix[row, col]
        return text

    def calc_diagonals_l(self, matrix):
        text = ''
        # In the for loop, with that '-', we get the range of -19 up to 20
        for diagonal in range(-(self.n_rows - 1), self.n_cols):
            i = max(0, -diagonal) # max ensures that both i and j do not go below 0 because it's the lowest row/col index
            #                     # for the negative values of diagonal, this max function just puts them as 0
            j = max(0, diagonal)

            # Now to traverse the diagonal from top left to bottom right
            while i < self.n_rows and j < self.n_cols:
                text += matrix[i][j]
                i += 1
                j += 1
        return text

    def calc_diagonals_r(self, matrix):
        text = ''
        for diagonal in range(self.n_rows + self.n_cols - 1):
            if diagonal < self.n_cols:
                i = 0  # Start with row 0 so we go right to left when the column changes
                j = diagonal  # For every col, go top to bottom
            else:
                j = self.n_cols - 1  # Get the last column
                i = diagonal - j  # Get the last row

                # Now to traverse the diagonal from top right to bottom left
            while i < self.n_rows and j >= 0:
                text += matrix[i][j]
                i += 1  # i (the row) will go down
                j -= 1  # j (the col) will go left
        return text

    def search(self):
        # pattern is each name in self.names
        # text is each horizontal, vertical, and diagonal strings in self.matrix

        # initializing the text as a string so the lists of rows, cols and diagonals get saved in a string
        text = ''

        for pattern in self.names:
            if len(pattern) == self.Name_Length:
                for row in range(self.n_rows):
                    text = self.calc_row(self.matrix, row)
                    if self.Name_Algorithm == "BruteForce":
                        self.match_BruteForce(pattern, text)
                    elif self.Name_Algorithm == "Horspool":
                        self.match_Horspool(pattern, text)
                for col in range(self.n_cols):
                    text = self.calc_col(self.matrix, col)
                    if self.Name_Algorithm == "BruteForce":
                        self.match_BruteForce(pattern, text)
                    elif self.Name_Algorithm == "Horspool":
                        self.match_Horspool(pattern, text)
                # For top left to bottom right direction
                text = self.calc_diagonals_l(self.matrix)
                if self.Name_Algorithm == "BruteForce":
                    self.match_BruteForce(pattern, text)
                elif self.Name_Algorithm == "Horspool":
                    self.match_Horspool(pattern, text)
                # For top right to bottom left direction
                text = self.calc_diagonals_r(self.matrix)
                if self.Name_Algorithm == "BruteForce":
                    self.match_BruteForce(pattern, text)
                elif self.Name_Algorithm == "Horspool":
                    self.match_Horspool(pattern, text)


if __name__ == "__main__":
        
    parser = argparse.ArgumentParser(description='Word Searching')
    parser.add_argument('-name', dest='Name_List', required = True, type = str, help='Name of name list')
    parser.add_argument('-algorithm', dest='Name_Algorithm', required = True, type = str, help='Name of algorithm')
    parser.add_argument('-length', dest='Name_Length', required = True, type = int, help='Length of the name')
    args = parser.parse_args()

    # Example:
    # python name_search.py -algorithm BruteForce -name Mexican -length 5

    obj = NameSearch(args.Name_List, args.Name_Algorithm, args.Name_Length)
    obj.search()


