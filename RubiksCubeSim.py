
import random

class RubiksCube(object):
    def __init__(self, cube = ""):
        
        #compressed:  'wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy'
        
        #uncompressed:
        self.goal = {'w00': 'w', 'w01': 'w', 'w02': 'w',
                     'w10': 'w', 'w11': 'w', 'w12': 'w',
                     'w20': 'w', 'w21': 'w', 'w22': 'w',

                     'o00': 'o', 'o01': 'o', 'o02': 'o',
                     'o10': 'o', 'o11': 'o', 'o12': 'o',
                     'o20': 'o', 'o21': 'o', 'o22': 'o',

                     'g00': 'g', 'g01': 'g', 'g02': 'g',
                     'g10': 'g', 'g11': 'g', 'g12': 'g',
                     'g20': 'g', 'g21': 'g', 'g22': 'g',
        
                     'r00': 'r', 'r01': 'r', 'r02': 'r',
                     'r10': 'r', 'r11': 'r', 'r12': 'r',
                     'r20': 'r', 'r21': 'r', 'r22': 'r',
                     
                     'b00': 'b', 'b01': 'b', 'b02': 'b',
                     'b10': 'b', 'b11': 'b', 'b12': 'b',
                     'b20': 'b', 'b21': 'b', 'b22': 'b',

                     'y00': 'y', 'y01': 'y', 'y02': 'y',
                     'y10': 'y', 'y11': 'y', 'y12': 'y',
                     'y20': 'y', 'y21': 'y', 'y22': 'y'
                    }
                    
        #side face ordering, to be concatenated with color in compressKey
        self.sideKey = ('00', '01', '02',
                        '10', '11', '12',
                        '20', '21', '22'
                        )

        self.compressKey = [x+y for x in 'wogrby'for y in self.sideKey]

        if cube == "":
            self.cube = self.goal.copy()
        else:
            self.cube = self.uncompress(cube)
        
        self.origCube = self.cube.copy()

        
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

        #create lookup table for cube spins
        #oriented with 00 top left, 22 bottom right, if looking at side 'key'
        #order of tuple matters
        self.sideTop      = {
                            'w': ('b00', 'b01', 'b02'),
                            'o': ('w00', 'w10', 'w20'),
                            'g': ('w20', 'w21', 'w22'),
                            'r': ('w22', 'w12', 'w02'),
                            'b': ('w00', 'w01', 'w02'),
                            'y': ('g20', 'g21', 'g22')
                            }

        self.sideBottom  = {
                            'w': ('g00', 'g01', 'g02'),
                            'o': ('y20', 'y10', 'y00'),
                            'g': ('y00', 'y01', 'y02'),
                            'r': ('y22', 'y12', 'y02'),
                            'b': ('y22', 'y21', 'y20'),
                            'y': ('b20', 'b21', 'b22')
                            }
                        
        self.sideLeft    = {
                            'w': ('o00', 'o01', 'o02'),
                            'o': ('b22', 'b12', 'b02'),
                            'g': ('o22', 'o12', 'o02'),
                            'r': ('g22', 'g12', 'g02'),
                            'b': ('r22', 'r12', 'r02'),
                            'y': ('o20', 'o21', 'o22')
                            }

        self.sideRight  = {
                            'w': ('r00', 'r01', 'r02'),
                            'o': ('g20', 'g10', 'g00'),
                            'g': ('r20', 'r10', 'r00'),
                            'r': ('b00', 'b10', 'b20'),
                            'b': ('o20', 'o10', 'o00'),
                            'y': ('r20', 'r21', 'r22')
                            }
        
        #Side arrangement, to be concatenated with colors in sideFront
        self.sideSpinKey    = {
                            '00': '20', '01': '10', '02': '00',
                            '10': '21', '11': '11', '12': '01',
                            '20': '22', '21': '12', '22': '02'
                            }
                            
        #pre-compute side spins based on sideSpinKey
        self.sideFront  = {y: {y + x : y + self.sideSpinKey[x]
                            for x in self.sideSpinKey} for y in 'wogrby'}
                            

    def compress(self):
        """returns self.cube as a String of len 54, index maps to below config
        uses 38 times less memory (76x if using 54 digit int)
        
        #               w
        #             o g r b
        #               y
        #
        #             0  1  2
        #             3  4  5
        #             6  7  8
        #  9 10 11   18 19 20   27 28 29   36 37 38
        # 12 13 14   21 22 23   30 31 32   39 40 41
        # 15 16 17   24 25 26   33 34 35   42 43 44
        #            45 46 47
        #            48 49 50
        #            51 52 53
        """
        
        compressed = ""
        for i in self.compressKey:
            compressed += self.cube[i] 

        return compressed
    
    def uncompress(self, cubeString):
        """converts a string to dict and returns cube dict
        uses scheme found in compress method
        """
        asDict = {}
        index = 0
        for i in self.compressKey:
            asDict[i] = cubeString[index]
            index += 1
        
        return asDict
        
    def spin(self, color):
        """updates self.cube by spinning side 'color' 90 degrees clockwise
        color: String - 'g', 'r', 'y', 'o', 'w', 'b'
        returns None
        perf: 100,000 spins per second
        """
        
        assert (color in 'gryowb')

        tempCube = {}
        
        def move_side(frm, to):
            """copies values from self.cube to tempCube's "to" side"""
            for x, y in zip(frm[color], to[color]):
                tempCube[y] = self.cube[x]

        # top -> right
        move_side(self.sideTop, self.sideRight)

        # right -> bottom
        move_side(self.sideRight, self.sideBottom)

        # bottom -> left
        move_side(self.sideBottom, self.sideLeft)

        # left -> top
        move_side(self.sideLeft, self.sideTop)

        # transform front side
        for square in self.sideFront[color]:
            updatedVal = self.sideFront[color][square]
            tempCube[square] = self.cube[updatedVal]
        
        self.cube.update(tempCube)

    def scramble(self):
        """scrables self.cube in place, no return, assumes random imported
        """
        keys = self.cube.keys()

        vals = self.cube.values()
        random.shuffle(vals)
        
        self.cube = dict(zip(keys, vals))
    
    def reset(self):
        self.cube = self.origCube.copy()

    def is_solved(self):
        return self.cube == self.goal
    
    def print_cube(self, side = "all"):
        """prints out unfolded cube, middle square capitalized
        side: string in 'wogrby' or 'all'
        """
        def print_side_indent(color):
            print '\t', self.cube[color+'00'],         \
                         self.cube[color+'01'],         \
                         self.cube[color+'02'], '\n',   \
                   '\t', self.cube[color+'10'],         \
                         self.cube[color+'11'].upper(), \
                         self.cube[color+'12'], '\n',   \
                   '\t', self.cube[color+'20'],         \
                         self.cube[color+'21'],         \
                         self.cube[color+'22'], '\n',
        
        if side == "all":
            
            #top
            print_side_indent('w')
            
            #middle four sides 'o', 'g', 'r', 'b'                      
            line = ""
            for i in 'ogrb':
                line += self.cube[i+'00']
                line += self.cube[i+'01']
                line += self.cube[i+'02']
            print " ", " ".join(line)
    
            line = ""
            for i in 'ogrb':
                line += self.cube[i+'10']
                line += self.cube[i+'11'].upper()
                line += self.cube[i+'12']
            print " ", " ".join(line)
    
            line = ""
            for i in 'ogrb':
                line += self.cube[i+'20']
                line += self.cube[i+'21']
                line += self.cube[i+'22']
            print " ", " ".join(line)
    
            #bottom
            print_side_indent('y')

        elif len(side) == 1 and side in 'wogrby':
            #print side and the 3 squares that are on top, bottom, left, right
            print_side_indent(side)
        else:
            return side + " is an invalid input!"

testCube = RubiksCube()


#scramble
testCube.spin('w')
testCube.spin('o')
testCube.spin('g')
testCube.spin('r')
testCube.spin('b')
testCube.spin('y')

#undo
def undo(x, cube):
    for i in range(3):
        cube.spin(x)

undo('y', testCube)
undo('b', testCube)
undo('r', testCube)
undo('g', testCube)
undo('o', testCube)
undo('w', testCube)

assert(testCube.is_solved())
