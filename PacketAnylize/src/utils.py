def get_min(lst):
	"""
	Find the minimum value in a list.
	
	Args:
		lst (list): A list of numbers.
		
	Returns:
		float: The minimum value in the list.
	"""
	if not lst:
		raise ValueError("The list is empty.")
	
	min_value = lst[0]
	for num in lst:
		if num < min_value:
			min_value = num
	return min_value

def get_max(lst):
	"""
	Find the maximum value in a list.
	
	Args:
		lst (list): A list of numbers.
		
	Returns:
		float: The maximum value in the list.
	"""
	if not lst:
		raise ValueError("The list is empty.")
	
	max_value = lst[0]
	for num in lst:
		if num > max_value:
			max_value = num
	return max_value

def get_mean(lst):
	"""
	Calculate the mean of a list.
	
	Args:
		lst (list): A list of numbers.
		
	Returns:
		float: The mean of the list.
	"""
	if not lst:
		raise ValueError("The list is empty.")
	
	total = 0
	for num in lst:
		total += num
	return total / len(lst)

def get_median(lst):
	"""
	Calculate the median of a list.
	
	Args:
		lst (list): A list of numbers.
		
	Returns:
		float: The median of the list.
	"""
	if not lst:
		raise ValueError("The list is empty.")
	
	sorted_lst = quick_sort(lst)
	n = len(sorted_lst)
	mid = n // 2
	
	if n % 2 == 0:
		return (sorted_lst[mid - 1] + sorted_lst[mid]) / 2
	else:
		return sorted_lst[mid]
	
def quick_sort(lst):
	"""
	Sort a list using the quicksort algorithm.
	
	Args:
		lst (list): A list of numbers.
		
	Returns:
		list: The sorted list.
	"""
	if len(lst) <= 1:
		return lst
	else:
		pivot = lst[len(lst) // 2]
		left = []
		right = []
		middle = []
		for i in range(len(lst)):
			if lst[i] < pivot:
				left.append(lst[i])
			elif lst[i] == pivot:
				middle.append(lst[i])
			elif lst[i] > pivot:
				right.append(lst[i])
			else:
				raise ValueError("Invalid value in list.")
		result = []
		result.extend(quick_sort(left))
		result.extend(middle)
		result.extend(quick_sort(right))
		return result

def verify_sorted(lst, original):
	"""
	Check if a list is sorted.
	
	Args:
		lst (list): A list of numbers.
		original (list): The original list to compare against.
		
	Returns:
		ValueError: If the list is not sorted or if the original list is empty.
	"""
	lst_copy = [0] * len(lst)
	for i in range(len(lst)):
		lst_copy[i] = lst[i]
	lst_len = len(lst)
	print("Verifying sorted list...")
	if not lst:
		raise ValueError("The list is empty.")
	if len(lst) == 1:
		return
	if len(lst) != len(original):
		raise ValueError("The length of the sorted list is not equal to the original list.")

	for i in range(len(lst) - 1):
		if lst[i] > lst[i + 1]:
			raise ValueError("There are elements in the list that are not sorted.")
		
	result = [0] * len(lst)

	for i in range(len(original)):
		bs_index = binary_search(lst_copy, lst_len, original[i])
		if bs_index == -1:
			raise ValueError("The sorted list contains elements that are not in the original list.")
		for j in range(bs_index, len(lst) - 1):
			lst_copy[j] = lst_copy[j + 1]
		lst_copy[len(lst) - 1] = None
		lst_len -= 1

	if (lst_len != 0):
		raise ValueError("The sorted list contains elements that are not in the original list.")
	

	print("The sorted list is sorted correctly.")
	return


def binary_search(lst, lst_len, target):
	"""
	Perform binary search on a sorted list.
	
	Args:
		lst (list): A sorted list of numbers.
		target (float): The target value to search for.
		
	Returns:
		int: The index of the target value index in the list, or -1 if not found.
	"""
	left = 0
	right = lst_len - 1
	
	while left <= right:
		mid = (left + right) // 2
		if lst[mid] == target:
			return mid
		elif lst[mid] < target:
			left = mid + 1
		else:
			right = mid - 1
	
	return -1