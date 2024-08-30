"""Print matrices in an easy way"""


def _pad_to_len(text: str, length: int):
	lt = len(text)
	if lt >= length:
		return text
	return ' ' * (length - lt) + text


def print_matrix(matrix: list, indent_row: int = 1, indent_col: int = 1,
                 sepx: str = ' ', sepy: str = '',
                 print_indexes: bool = False, represent_empty: str = None):
	"""
	Print matrices in a better way
	:param matrix: Matrix to print
	:param indent_row: How many spaces between printed row index and row itself
	:param indent_col: How many new lines between printed column index and column itself
	:param sepx: Separation between elements
	:param sepy: Separation between rows, add '\n' for every row to be divided by empty new line
	:param print_indexes: If it should print indexes of columns and rows
	:param represent_empty: If not all rows are equal - there will be empty spaces in some of them,
	represent them here with any string.
	A string should be smaller than a maximum element in a matrix, otherwide it will be cut.
	"""
	max_element_len = 0
	max_line_len = 0
	row_index_len = len(matrix) // 10 + 1
	
	for line in matrix:
		max_element_len = max(max_element_len, len(str(max(line, key=lambda n: len(str(n))))))
		max_line_len = max(max_line_len, len(line))
	
	if print_indexes:
		max_element_len = max(max_element_len, len(str(max_line_len)))
		print(_pad_to_len('', row_index_len), end=sepx)
		print(' ' * indent_row, end='')
		print(*(_pad_to_len(str(i), max_element_len) for i in range(max_line_len)), sep=sepx,
		      end='\n' * indent_col)
	
	if represent_empty:
		line_end = ''
	else:
		line_end = None
	
	for index, line in enumerate(matrix):
		if print_indexes:
			print(_pad_to_len(str(index), row_index_len), end=sepx)
			print(' ' * indent_row, end='')
		
		print(*(_pad_to_len(str(n), max_element_len) for n in line), sep=sepx, end=line_end)
		if represent_empty:
			print('', *[_pad_to_len(represent_empty, max_element_len)] * (max_line_len - len(line)), sep=sepx)
		print(sepy, end='')


if __name__ == '__main__':
	arr1 = [[j for j in range(i * 10, i * 10 + 10)] for i in range(11)]
	print_matrix(arr1, print_indexes=True, indent_row=2, indent_col=2)
	
	print()
	print()
	arr2 = [["abc", 1234, "asdfas"], [19282390, '', "print", "i'm stupid"], ["why tho"]]
	print_matrix(arr2, print_indexes=True, indent_row=2, indent_col=2, sepx=' | ')
	
	print()
	print()
	print_matrix(arr2, print_indexes=True, indent_row=2, indent_col=2, sepx=' | ', represent_empty='---')
	
	print()
	print()
	print_matrix(arr1, print_indexes=True, indent_row=4, indent_col=2, sepy='\n')
	
	print()
	print()
	arr3 = [[1 for x in range(101)] for y in range(11)]
	print_matrix(arr3, print_indexes=True)
