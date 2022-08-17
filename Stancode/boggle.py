"""
File: boggle.py
Name: Marinda
----------------------------------------
This program demonstrates "Boggle" game by printing all the results following rule of boggle game after user
input 4 rows of letters.
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


def main():
	"""
	Ask user to input 4 rows of letters and check if it follows the rule (4 character in a row in tsv type), program
	terminated if input format is not correct. After user input, find all the boggle results and print.
	"""
	start = time.time()
	illegal_format = 0
	target_lst = []
	for i in range(4):
		user_input = input(f"{i+1} row of letters: ")
		# Case-insensitive & split by space
		target_lst.append(user_input.lower().split())

		# Check if input format is correct
		for j in range(4):
			if len(target_lst[i][j]) != 1:
				print('Illegal input')
				illegal_format = 1
				break
		if illegal_format == 1:
			break

	# If user input format correct, proceed word_search function
	if illegal_format == 0:
		word_search(target_lst)
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def word_search(target_lst):
	"""
	Define dictionary_lst which will be compared with back tracking results to find answer. Also to find length of the
	longest word in dictionary as one of condition of early breaking. Call helper function to find and print boggles
	result by applying back tracking method from every characters of each rows.
	:param target_lst: Python list, list of 4 groups of 4 characters input by user
	"""
	dictionary_lst = read_dictionary(target_lst)

	# 找出長度最長單字
	word_length_max = 0
	for word in dictionary_lst:
		if len(word) > word_length_max:
			word_length_max = len(word)
	ans_lst = []

	# 以16個字分別為起點來做Back tracking
	for x in range(4):
		for y in range(4):
			ans_lst = word_search_helper(target_lst, dictionary_lst, ans_lst, "", [], x, y, word_length_max)
	print(f"There are {len(ans_lst)} words in total.")


def word_search_helper(target_lst, dictionary_lst, ans_lst, current_s, chosen_index_lst, x, y, word_length_max):
	"""
	Back tracking to find all the string combination by connecting characters within 九宮格 of 起始單字. Base case is when
	the string meets words in dictionary_lst and haven't been found and added in ans_lst, the function will print the
	string and add it in ans_lst. Also, function will be early broken if there's no any words in dictionary_lst starting
	by current_s.
	:param target_lst: Python list, list of 4 groups of 4 characters input by user
	:param dictionary_lst: Python list, list of words in dictionary
	:param ans_lst: Python list, words found from target_lst follows boggle rule which meets words in dictionary_lst
	:param current_s: str, current string during backtracking process
	:param chosen_index_lst: Python list, list of tuples of location(x,y) which has been chosen
	:param x: int, x-axis of user input matrix which represents the column chosen from the matrix
	:param y: int, y-axis of user input matrix which represents the row chosen from the matrix
	:param word_length_max: int, length of the longest word in dictionary
	:return ans_lst: Python list, words found from target_lst follows boggle rule which meets words in dictionary_lst
	"""
	# Early breaking: 檢查dictionary_list中有沒有以current_s開頭的單字 & current_s有無超過長度上限
	if has_prefix(current_s, dictionary_lst) and len(current_s) <= word_length_max:

		# Base case
		if current_s in dictionary_lst and current_s not in ans_lst:
			print(f'Found: "{current_s}"')
			ans_lst.append(current_s)

		for i in range(-1, 2, 1):
			for j in range(-1, 2, 1):
				# 確認 new_x & new_y 都在矩陣內, 且門牌號碼沒有重複選
				if 0 <= x+i <= 3 and 0 <= y+j <= 3 and (x+i, y+j) not in chosen_index_lst:
					# Choose
					chosen_index_lst.append((x+i, y+j))
					current_s += target_lst[x+i][y+j]
					# Explore
					word_search_helper(target_lst, dictionary_lst, ans_lst, current_s, chosen_index_lst, x+i, y+j, word_length_max)
					# Un-choose
					chosen_index_lst.pop()
					current_s = current_s[0:len(current_s) - 1]
	return ans_lst


def read_dictionary(lst):
	"""
	Stores words with equal length with target string s in file (file path: FILE) in a Python list dictionary_list,
	and return the dictionary_list.
	:param lst: Python list, list of target characters
	:return dictionary_list: Python list, stored all the words in dictionary from file path (FILE)
	"""
	with open(FILE, 'r') as f:
		character_list = []
		massive_dictionary_list = []
		dictionary_list = []

		# 只存長度大於等於4的詞
		for line in f:
			if len(line[0:len(line) - 1]) >= 4:
				massive_dictionary_list.append(line[0:len(line) - 1])

		# 把 target lst裡面的字拆開存成一個lst
		for small_lst in lst:
			for ch in small_lst:
				character_list.append(ch)

		# 從字典中去除那些用到user沒有input的字母的單字
		for word in massive_dictionary_list:
			match_characters = 0
			for ch in word:
				if ch in character_list:
					match_characters += 1
			if match_characters == len(word):
				dictionary_list.append(word)
		return dictionary_list


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
