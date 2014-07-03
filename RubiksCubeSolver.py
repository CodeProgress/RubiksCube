
from RubiksCubeSim import RubiksCube

test = RubiksCube()



# 2D visualization, if cube were unfolded with green facing up
#
#                w00 w01 w02
#
#                w10 w11 w12
#
#                w20 w21 w22
#
# 
# o00 o01 o02    g00 g01 g02    r00 r01 r02    b00 b01 b02
#
# o10 o11 o12    g10 g11 g12    r10 r11 r12    b10 b11 b12
#
# o20 o21 o22    g20 g21 g22    r20 r21 r22    b20 b21 b22
#
#              
#                y00 y01 y02
#
#                y10 y11 y12
#
#                y20 y21 y22


#             0  1  2
#             3  4  5
#             6  7  8
#  9 10 11   18 19 20   27 28 29   36 37 38
# 12 13 14   21 22 23   30 31 32   39 40 41
# 15 16 17   24 25 26   33 34 35   42 43 44
#            45 46 47
#            48 49 50
#            51 52 53

goal = 'wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy'

colors = 'wogrby'
#solve the cross
white = [1,3,4,5,7]
orange = [10, 13]
green = [19,22]
red = [28, 31]
blue = [37,40]

sliceCrossKey = white + orange + green + red + blue

def make_slice(string, key):
    slc = ""
    for i in key:
        slc += string[i]
    return slc


print make_slice(goal, sliceCrossKey)






#solve the white corners




#solve the middle layer




#solve the top layer




#position the yellow corners



















#using graph search

#precompute a hashtable of the 43239 position that are 4 moves away
#or 5 moves away is 574,908 positions
#use positions 4 away as the keys 
#if the algorithms arrives at one of these states, break and finish


## Solver - In progress... 
def successor_function(compressedCube):
    '''returns a list of possible cube states (as compressed strings)
    reachable in 1-3 spins from compressedCube
    a spin is a 90, 180 or 270 degree turn of a side
    cube: compressed string
    '''
    rubik = RubiksCube(compressedCube)
    posCubes = []
    for i in 'wogrby':
        for j in range(3):
            rubik.spin(i)
            posCubes.append(rubik.compress())
        rubik.reset()
    return posCubes  
               
def heuristic(cube):
    """returns a number, higher the closer to solution"""
    #possibilities:
    #number correct colors on each side
    
    #number of colors on each side (lower is better)
    
    #number of squares out of place
    #not really a good one... after 4 spins it gives 17 out of 56...
    count = 0
    for i in cube:
        if cube[i] == i[0]:
            count += 1
    return count

def priority_queue(self):
    #priority based on heuristic + num steps taken
    pass

def a_star_search(startState, goalState, successorFunction):
    #g(n) actual steps taken
    #h(n) heuristic
    pass

## End Solver
#-------------------------