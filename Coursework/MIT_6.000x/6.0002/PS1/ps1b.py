"""
Problem Set 1b: Space Change
After the Aucks transport the cows, one of their interns finds flocks of golden geese.
 Due to budget cuts they are forced to downsize their ships so they can’t simply 
 take the geese back, but instead decide to take their golden eggs back. 
 Their ships can only hold a certain amount of weight, and are very small inside. 
 So, because all the eggs are the same size, but have different weights, 
 they want to bring back as few eggs as possible that fill their ship’s weight limit.
 Golden eggs are all the same size, but may have different densities, 
 thus 1 two-pound egg is better than 2 one-pound eggs.
"""

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
#    """
#    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
#    an infinite supply of eggs of each weight, and there is always a egg of value 1.
#    
#    Parameters:
#    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
#    target_weight - int, amount of weight we want to find eggs to fit
#    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
#    
#    Returns: int, smallest number of eggs needed to make target weight
#    """
    # TODO: Your code here
    
    #RECURSIVE GREEDY ALGORITHM   
#    heaviest_egg = len(egg_weights)-1 #index of the heaviest_egg
#    numberEggs = target_weight//egg_weights[heaviest_egg]
#    remain_weight = target_weight%egg_weights[heaviest_egg]
#    memo[egg_weights[heaviest_egg]] = numberEggs
#    
#    if remain_weight == 0:
#        result = sum(memo.values())
#        return result
#    else:
        #need to return the recursive function, 
        #otherwise the function simply ends after executing that statement, 
        #returning 'None'.
#        return dp_make_weight(egg_weights[0:heaviest_egg], remain_weight)
    
    #DYNAMIC PROGRAMMING WITHOUT RECURSION (no need to use memo)
    assert 1 in egg_weights
    assert all(x<y for x, y in zip(egg_weights, egg_weights[1:]))
#    Note:The all () function is used to determine 
#         whether all elements in a given iterable parameter are TRUE. 
#         If it is True, it returns False. 

#     Initialize an array (list) dp of length (tar­get_weight + 1), fill in all 0. 
#     The value of dp [i] represents the minimum number of eggs needed for a weight of i.
    dp = [0 for i in range(target_weight+1)]
    for i in range(1, target_weight+1):
        dp[i] = 1 + min([dp[i-weight] for weight in egg_weights if weight<=i])
    return dp[target_weight]

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
#    ------OK
#    egg_weights = (1, 5, 10, 25)
#    n = 99
#    print("Egg weights = (1, 5, 10, 25)")
#    print("n = 99")
#    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
#    print("Actual output:", dp_make_weight(egg_weights, n))
#    print()
    
#    ------OK
#    egg_weights = (1, 5, 10, 20, 50)
#    n = 208
#    print("Expected ouput: 8 (4 * 50 + 1 * 5 + 3 * 1 = 208)")
#    print("Actual output:", dp_make_weight(egg_weights, n))
#    print()
 
#   ------OK/BUGGY for greedy algorithm
    egg_weights = (1, 9, 90, 91)
    n = 99
    print("Expected ouput: 2 (1 * 90 + 1 * 9 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

##   ------OK
#    egg_weights = (1,)
#    n = 13
#    print("Expected ouput: 13 (13 * 1 = 13)")
#    print("Actual output:", dp_make_weight(egg_weights, n))
#    print()

##   ------OK
#    egg_weights = (1, 2, 4, 8, 16, 32, 64)
#    n = 127
#    print("Expected ouput: 7")
#    print("Actual output:", dp_make_weight(egg_weights, n))
#    print()