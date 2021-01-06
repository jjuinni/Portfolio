"""
Problem Set 4A
recursive function that takes as input a string and 
figures out all the possible reorderings of the characters in the string.
"""
def get_permutations(sequence):
    '''
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
    '''
#    recursive solution
#    - base case(stop condition): if sequence is a single character. 
#                                 Another way to say, there is only one character left in the string.
#                               -> no recursion required
#    - recursive case: if sequence is longer than one character.
#       *Recursive step: take the first character of the string and 
#                        insert it into all positions of each permutation of the remaining characters. 
    if len(sequence) == 1:
        return sequence
    else:
        permutations = []
        #permute over all but the first character in sequence
        for remaining in get_permutations(sequence[1:]): 
             #Insert the first character in each position
            for i in range(len(remaining) + 1):
#                How to insert a character into a string in Python? -> bound to new object!
#                Strings are immutable, so they cannot be changed directly to a character of a string.
#                So we bound new string object by putting pieces together. The below method is allowed. 
                permutations.append(remaining[:i] + sequence[0] + remaining[i:])
        permutations.sort() #not essential line of code, just for easier testing of expected/actual output.
        return permutations 

if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input_ = 'bust'
    print('Input:', example_input_)
    print('Expected Output:', ['bstu', 'bsut', 'btsu', 'btus', 'bust', 'buts', 'sbtu', 'sbut', 'stbu', 'stub', 'subt', 'sutb', 'tbsu', 'tbus', 'tsbu', 'tsub', 'tubs', 'tusb', 'ubst', 'ubts', 'usbt', 'ustb', 'utbs', 'utsb'])
    print('Actual Output:', get_permutations(example_input_))
    
    example_input__ = '01'
    print('Input:', example_input__)
    print('Expected Output:', ['01', '10'])
    print('Actual Output:', get_permutations(example_input__))    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


