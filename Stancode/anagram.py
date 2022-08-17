"""
File: anagram.py
Name: Marinda
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 23

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop


def main():
    """
    Find all anagrams for string user input and print, if string user input equals EXIT code (default as -1), the
    program will be ended.
    """

    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')
    while True:
        s = input('Find anagrams for: ')
        start = time.time()
        if s == EXIT:
            break
        find_anagrams(s)
        end = time.time()
        print('----------------------------------')
        print(f'The speed of your anagram algorithm: {end-start} seconds.')


def read_dictionary(s):
    """
    Stores words with equal length with target string s in file (file path: FILE) in a Python list dictionary_list,
    and return the dictionary_list.
    :param s: str, target string
    :return dictionary_list: Python list, stored all the words in dictionary from file path (FILE)
    """
    with open(FILE, 'r') as f:
        character_list = []
        massive_dictionary_list = []
        dictionary_list = []

        # 只存長度跟s相等的詞
        for line in f:
            if len(line[0:len(line)-1]) == len(s):
                massive_dictionary_list.append(line[0:len(line)-1])

        # 把target string中的character先存成一個list
        for ch in s:
            character_list.append(ch)

        # 只留下有用到target string中的character的詞
        for word in massive_dictionary_list:
            match_characters = 0
            for ch in word:
                if ch in character_list:
                    match_characters += 1
            if match_characters == len(word):
                dictionary_list.append(word)
        return dictionary_list


def find_anagrams(s):
    """
    Print the 1st "Searching..." and call function find_anagrams_helper() to find and print all the anagrams of the
    target string s. Then print the final result.
    :param s: str, target string to be find all the anagrams
    """
    lst = read_dictionary(s)
    print('Searching...')
    ans = find_anagrams_helper(s, lst, [], "", [], [])
    print(f"{len(ans)} anagrams: {ans}")


def find_anagrams_helper(s, dictionary_list, answer_list, current_s, chosen_index_list, chosen_ch_list):
    """
    Find all the anagrams by back tracking method and early breaking by has_prefix() function. Print all the anagrams
    and return list of anagrams.
    :param s: str, target string to be find all the anagrams
    :param dictionary_list: Python list, list of words in dictionary
    :param answer_list: Python list, list of anagram words found
    :param current_s: str, current string during backtracking process
    :param chosen_index_list: Python list, list of index which has been chosen
    :param chosen_ch_list: Python list, list of first characters which have been chosen
    :return answer_list: Python lise, list of anagram words found
    """
    # Base case
    if len(current_s) == len(s) and current_s in dictionary_list and current_s not in answer_list:
        print(f"Found: {current_s}")
        print('Searching...')
        answer_list.append(current_s)
        return answer_list

    else:
        if has_prefix(current_s, dictionary_list):  # Early breaking: 檢查dictionary_list中有沒有以current_s開頭的單字
            for i in range(len(s)):
                if len(current_s) == 0 and s[i] in chosen_ch_list:  # 重複的首字母不需要再跑一次
                    pass
                elif i not in chosen_index_list:  # 確認門牌號碼沒有重複選
                    # Choose
                    chosen_index_list.append(i)
                    if len(current_s) == 0:
                        chosen_ch_list.append(s[i])
                    current_s += s[i]
                    # Explore
                    find_anagrams_helper(s, dictionary_list, answer_list, current_s, chosen_index_list, chosen_ch_list)
                    # Un-choose
                    chosen_index_list.pop()
                    current_s = current_s[0:len(current_s)-1]
        return answer_list


def has_prefix(sub_s, dictionary_list):
    """
    Check if sub_s is compatible with starting characters of any words in dictionary_list.
    :param sub_s: str, target string to be compared
    :param dictionary_list: Python list, list of words in dictionary
    :return: Boolean, "True" means there're compatible words in dictionary_list, "False" means there're not.
    """
    for word in dictionary_list:
        if word.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
