#Problem        : Expecto Palindronum
#Language       : Python
#Compiled Using : py_compile
#Version        : Python 2.7.8
#Input for your program will be provided from STDIN
#Print out all output from your program to STDOUT

from __future__ import print_function
import sys

data = sys.stdin.read().splitlines()

def find_min_palin(word):
    i = 0
    min_add = 0
    n = len(word)
    for j in range(n-1, -1, -1):
        if i == j:
            min_add = n-1-j
        elif word[i] == word[j]:
            i += 1
    return min_add
            

if __name__ == "__main__":
    line = "abc"
    n = len(line)
    #print(min(find_min_palin(line),n-find_min_palin(''.join(reversed(line)))) + n)
    print(find_min_palin(line)+n)