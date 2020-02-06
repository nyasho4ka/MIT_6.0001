# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx


def get_permutations(sequence):
    """
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    """
    if len(sequence) == 1:
        return [sequence]

    permutations = []

    first_letter = sequence[0]
    recursive_permutations = get_permutations(sequence[1:])

    for permutation in recursive_permutations:
        for i in range(len(sequence)):
            new_permutation = insert_char_in_line(permutation, first_letter, i)
            permutations.append(new_permutation)

    return permutations


def insert_char_in_line(line, char, position):
    """
    Insert char in string into position
    :param string:
    :param char:
    :param position:
    :return: new_line -> string
    """
    return line[:position] + char + line[position:]


def test_get_permutations(user_input, expected_output):
    print('Input:', user_input)
    print('Expected output:', expected_output)

    actual_output = get_permutations(user_input)
    print('Actual output:', actual_output)
    if set(expected_output) == set(actual_output):
        return True
    return False


def test_all(user_inputs, expected_outputs):
    results = []
    for user_input, expected_output in zip(user_inputs, expected_outputs):
        test_result = test_get_permutations(user_input, expected_output)
        results.append(test_result)

    if all(results) is True:
        print("SUCCESS!")
    else:
        print("FAILURE")


if __name__ == '__main__':
    #    #EXAMPLE
    #    example_input = 'abc'
    #    print('Input:', example_input)
    #    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    #    print('Actual Output:', get_permutations(example_input))

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)
    user_inputs = ['z', 'nm', 'olp']
    expected_outputs = [['z'], ['nm', 'mn'], ['olp', 'opl', 'plo', 'pol', 'lop', 'lpo']]
    test_all(user_inputs, expected_outputs)
