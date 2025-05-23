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
