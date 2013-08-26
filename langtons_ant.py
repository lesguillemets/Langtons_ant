#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import sys,time

VOID_COLOUR = 0
ANT_COLOUR = 255


class Ant(object):
        
    
    def __init__(self, location, direction, colour = ANT_COLOUR):
        self.location = location
            # location : [x,y] for the ant's current location.
        self.direction = direction
            # direction : 0 (up), 1 (right), 2 (down), 3 (left) for now.
        self.colour = colour
        self.isalive = True
            # not sure it's going to be used
        
        self.v = {
            0 : ( 0, 1),
            1 : ( 1, 0),
            2 : ( 0,-1),
            3 : (-1, 0),
        } 
            #self.v[self.direction] gives the velocity of the ant.
    
    def turn(self, degs):
        '''
        the ant turns right, around, or left.
        degs should be given as number 0-3. 
            0 : keep its direction (0)
            1 : turn right         (1/2 pi)
            2 : turn around        (pi)
            3 : turn left          (3/2 pi)
        '''
        self.direction += degs
        self.direction = self.direction % 4
    
    def turn_right(self):
        self.turn(1)
        
    
    def turn_left(self):
        self.turn(3)
    
    def move(self):
        self.location = map(sum, zip(self.location, self.v[self.direction]) )
    
    def die(self):
        self.isalive = False 


class Field(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = np.zeros((width,height))
    
    def __call__(self):
        return self.field
    
    def getcolour(self,loc):
        # loc : (x,y)
        return self.field[ loc[0] ][ loc[1] ] 

    def putcolour_at(self,loc,colour):
        self.field[ loc[0] ][ loc[1] ] = colour
    
    def has_colour_at(self,loc):
        return self.field[ loc[0] ][ loc[1] ] != VOID_COLOUR
    
    def flip(self, loc, colour = ANT_COLOUR):
        if self.has_colour_at(loc):
            self.putcolour_at(loc, VOID_COLOUR)
        else:
            self.putcolour_at(loc, colour)

class Langton(object):
    def __init__(self, width, height, number_of_ants=1):
        # set field
        self.Field = Field(width,height)
        
        # put ants
        self.ants = []
        for i in range(number_of_ants):
            loc = random_location(width, height)
            direction = random.randint(0,3)
            self.ants.append( Ant(loc, direction, i+1) )
    
    def step(self):
        
        for ant in [ant for ant in self.ants if ant.isalive] :
            
            loc = ant.location
            loc_colour = self.Field.getcolour(loc)
            
            # at a white square, turn right,
            if loc_colour == VOID_COLOUR:
                ant.turn_right()
            # at a black square, turn left.
            else:
                ant.turn_left()
            
            # flip the colour of the square
            self.Field.flip(loc, ant.colour)
            
            # step forward
            ant.move()   
            
            # dies if out of range
            if not (0 <= ant.location[0] < self.Field.width 
                        and 0 <= ant.location[1] < self.Field.height ):
                ant.die()



    
def random_location(width, height):
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)
    return [x,y]


def main():
# game setup
    myLangton = Langton(*( map(int,sys.argv[1:]) ))
    for i in range(15000):
        myLangton.step()
        if not any( [ant.isalive for ant in myLangton.ants]):
            print 'All dead!'
            break
    """
    # animation setup
        def animator(frame_number, langton =myLangton):
            langton.step()
            print langton.Field()
            mat.set_data( langton.Field() )
            return [mat]
        
    """
    fig, ax = plt.subplots()
    mat = ax.matshow(myLangton.Field())
  #  ani = animation.FuncAnimation(fig, animator,
  #                          interval = 50, save_count=50)
    plt.show()


if __name__ == '__main__':
    main()
