from typing import Dict, List, Any, re

import pandas as pd


def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    """
    Reverses the input list by groups of n elements.
    """
    # Your code goes here.

    lst = []

    # Traversing the list in steps for n
    for i in range(0, len(lst), n):
        group = lst[i:i + n]

        # Reverse the group
        # create an empty reverse group list

        reversed_group = []

        for j in range(len(group)):
            reversed_group.append(group[len(group) - 1 - j])

        # Append the reversed group to the result
        lst.extend(reversed_group)

    return lst


def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    """
    Groups the strings by their length and returns a dictionary.
    """

    # Initialize an empty dictionary to store the result
    dict = {}

    # Iterate through each string in the input list
    for value in lst:
        # Get the length
        value_length = len(value)

        # If the length is already a key in the dictionary, append the word to the list
        if value_length in dict:
            dict[value_length].append(value)
        else:
            # If the length is not in the dictionary, create a new entry with this length
            dict[value_length] = [value]

    # Return the dictionary without sorting
    return dict


def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    """
    Flattens a nested dictionary into a single-level dictionary with dot notation for keys.
    
    :param nested_dict: The dictionary object to flatten
    :param sep: The separator to use between parent and child keys (defaults to '.')
    :return: A flattened dictionary
    """
    # Your code here
    # Initialize an empty dictionary to store the flattened result
    flat_dict = {}

    # Helper function to perform recursive flattening
    def flatten(current_key: str, value: Any):

        # If the value is a dictionary, recursively flatten it
        if isinstance(value, dict):
            for k, v in value.items():
                new_key = f"{current_key}{sep}{k}" if current_key else k
                flatten(new_key, v)

        # If the value is a list, iterate through it and flatten each element
        elif isinstance(value, list):
            for i, item in enumerate(value):
                new_key = f"{current_key}[{i}]"
                flatten(new_key, item)

        else:
            # Base case: no more nesting, add the flattened key-value pair to the result
            flat_dict[current_key] = value

    # Start the recursive flattening process
    flatten('', nested_dict)

    return flat_dict
    # the reason I have changed dict to flat_dict is because of built-in dict type in Python


def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list that may contain duplicates.
    
    :param nums: List of integers (may contain duplicates)
    :return: List of unique permutations
    """
    # Your code here
    def backtrack(start=0):
        # put the nums in result
        if start == len(nums):
            result.append(nums[:])  # Append a copy of the current permutation
            return

        seen = set()  # Tracking elements of start

        for i in range(start, len(nums)):
            # Skip duplicates
            if nums[i] in seen:
                continue
            seen.add(nums[i])  # Mark this number as seen
            # Swap to place nums[i] at the 'start' position
            nums[start], nums[i] = nums[i], nums[start]
            # Recur with the next index
            backtrack(start + 1)
            # Backtrack (swap back)
            nums[start], nums[i] = nums[i], nums[start]

    result = []
    nums.sort()  # Sort to ensure duplicates are adjacent
    backtrack()
    return result

    pass


def find_all_dates(text: str) -> List[str]:
    """
    This function takes a string as input and returns a list of valid dates
    in 'dd-mm-yyyy', 'mm/dd/yyyy', or 'yyyy.mm.dd' format found in the string.
    
    Parameters:
    text (str): A string containing the dates in various formats.

    Returns:
    List[str]: A list of valid dates in the formats specified.
    """

    # Regular expression patterns for different date formats
    date_patterns = [
        r'\b\d{2}-\d{2}-\d{4}\b',  # dd-mm-yyyy
        r'\b\d{2}/\d{2}/\d{4}\b',  # mm/dd/yyyy
        r'\b\d{4}\.\d{2}\.\d{2}\b'  # yyyy.mm.dd
    ]

    # List to store all matching dates
    matches = []

    # Search for each pattern in the text
    for pattern in date_patterns:
        matches.extend(re.findall(pattern, text))

    return matches
    pass


def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    """
    Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    
    Args:
        polyline_str (str): The encoded polyline string.

    Returns:
        pd.DataFrame: A DataFrame containing latitude, longitude, and distance in meters.
    """
    return pd.Dataframe()


def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Rotate the given matrix by 90 degrees clockwise, then multiply each element 
    by the sum of its original row and column index before rotation.
    
    Args:
    - matrix (List[List[int]]): 2D list representing the matrix to be transformed.
    
    Returns:
    - List[List[int]]: A new 2D list representing the transformed matrix.
    """
    # Your code here

    n = len(matrix)  # Get the size of the matrix

    # Step 1: Rotate the matrix by 90 degrees clockwise
    rotated_matrix = [[0] * n for _ in range(n)]  # Create an empty rotated matrix
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n - 1 - i] = matrix[i][j]

    # Step 2: Transform the rotated matrix
    final_matrix = [[0] * n for _ in range(n)]  # Create an empty final matrix
    for i in range(n):
        for j in range(n):
            # Calculate the sum of the current row and column in the rotated matrix
            row_sum = sum(rotated_matrix[i])  # Sum of the i-th row
            col_sum = sum(rotated_matrix[k][j] for k in range(n))  # Sum of the j-th column
            # Replace the current element with the sum of row and column excluding itself
            final_matrix[i][j] = row_sum + col_sum - rotated_matrix[i][j]

    return final_matrix

    # return []


def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
