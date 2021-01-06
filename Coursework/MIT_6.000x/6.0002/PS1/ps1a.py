"""
Problem Set 1a: Space Cows 
The aliens have succeeded in breeding cows that jump over the moon! 
Now they want to take home their mutant cows. 
The aliens want to take all chosen cows back, but their spaceship has
a weight limit and they want to minimize the number of trips they have 
to take across the universe. 
Somehow, the aliens have developed breeding technology to make cows with only
integer weights.
"""
from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here

    # cow_dict: dictiorany cow_name(key):weight_tons(value)
    cow_dict = {}
    with open(filename, 'r') as inFile:
        for line in inFile:
            param = line.split(',')
            cow_dict[param[0]] = int(param[1].rstrip()) #.rstrip() to remove trailing newline on file
    return cow_dict
    
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here 
    cows_name = cows.keys()
    cows_name = sorted(cows_name, key=cows.__getitem__) #sorted by value(weight)
    cows_name.reverse()
    all_trips = []

    while cows_name != []:
        passangers = []
        weight_in = 0
        cows_name_copy = cows_name[:]
        for cow in cows_name_copy:
            weight_in += cows[cow]
            if weight_in <= limit and cow not in passangers:
                passangers.append(cow)
                cows_name.remove(cow)
            else:
                weight_in -= cows[cow]
        all_trips.append(passangers)
    return all_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cows_name = cows.keys()
    ways = []
    for partition in get_partitions(cows_name):
#        filter partitions that have lists within the limit weight
        counter = 0
        for trip in partition:
            tripweight = 0
#            counter = 0
            for cow in trip:
                tripweight += cows[cow]
            if tripweight <= limit:#trip weights <= 10 tons
                counter += 1
        if len(partition) == counter: #partition is a possible way
            ways.append(partition)

#    find minimized way
    bestway = len(cows.keys()) #initially with the worst scenario (worst decision)
    for way in ways:
        if len(way) <= bestway: #adjust decision
            bestway = len(way)
            bestway_list = way
    
    return bestway_list

# Problem 4
def compare_cow_transport_algorithms(filename):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows(filename)
    start_greedy = time.perf_counter() #perf_counter() more accurate than time()
    greedy = greedy_cow_transport(cows)
    end_greedy = time.perf_counter()
    print('                    ##### GREEDY ALGO #####')
    print('Result:', greedy)
    print('Algo process time:', '{:.2f} ms'.format((end_greedy-start_greedy)*1000))
    print('Greedy no.trips:', len(greedy))
    print()
    print()
    start_brute = time.perf_counter()
    brute = brute_force_cow_transport(cows)
    end_brute = time.perf_counter()
    print('                    ##### BRUTE ALGO #####')
    print('Result:', brute)
    print('Algo process time:', '{:.2f} ms'.format((end_brute-start_brute)*1000))
    print('Brute no.trips:', len(brute))
    
if __name__ == '__main__':

#    print(load_cows('ps1_cow_data.txt'))
#    print(load_cows('ps1_cow_data_2.txt'))
    
#    cows = {'Jesse': 6, 'Maybel': 3, 'Callie': 2, 'Maggie': 5}
#    cows = {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 'Moo Moo': 3, 'Milkshake': 2, 'Millie': 5, 'Lola': 2, 'Florence': 2, 'Henrietta': 9}

#    print(greedy_cow_transport(cows,limit=10))
#    print(brute_force_cow_transport(cows,limit=10))
    
#    load_cows('ps1_cow_data.txt')
    compare_cow_transport_algorithms('ps1_cow_data.txt')
#    compare_cow_transport_algorithms('ps1_cow_data_2.txt')
