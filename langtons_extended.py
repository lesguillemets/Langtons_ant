#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import sys,time

VOID_COLOUR = 0

class Ant(object):
        
    
    def __init__(self, location, direction):
        self.location = location
            # location : [x,y] for the ant's current location.
        self.direction = direction
            # direction : 0 (up), 1 (right), 2 (down), 3 (left) for now.
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
    
    def __init__(self, width, height, number_of_states):
        self.width = width
        self.height = height
        self.field = np.zeros((width,height))
        self.number_of_states = number_of_states
    
    def __call__(self):
        return self.field
    
    def getstate(self,loc):
        # loc : (x,y)
        return int(self.field[ loc[0] ][ loc[1] ])
    
    def proceed_state(self,loc):
        self.field[ loc[0] ][ loc[1] ] = \
                (self.field[ loc[0] ][ loc[1] ] + 1) % self.number_of_states
    
    def forcestate_at(self, loc, state):
        self.field[ loc[0] ][ loc[1] ] = state


class Langton(object):
    def __init__(self, width, height, number_of_ants=1, every_n_steps=10, rule='LR'):
        # set field
        self.Field = Field(width,height,len(rule))
        
        # put ants
        self.ants = []
        for i in xrange(number_of_ants):
            loc = random_location(width, height)
            direction = random.randint(0,3)
            self.ants.append( Ant(loc, direction) )
        
        # set rule
        self.rule = rule.upper()
        # animation
        self.every_n_steps = every_n_steps
    
    def step(self):
        
        for ant in [ant for ant in self.ants if ant.isalive] :
            
            loc = ant.location
            loc_state = self.Field.getstate(loc)
            
            # at a white square, turn right,
            if self.rule[ loc_state ] == 'R':
                ant.turn_right()
            # at a black square, turn left.
            elif self.rule[ loc_state ] == 'L':
                ant.turn_left()
            else:
                pass 
            
            # flip the colour of the square
            self.Field.proceed_state(loc)
            
            # step forward
            ant.move()   
            
            # dies if out of range
            if not (0 <= ant.location[0] < self.Field.width 
                        and 0 <= ant.location[1] < self.Field.height ):
                ant.die()
    
    def mainloop(self):
        fig, ax = plt.subplots()
        self.step()
        mat = ax.matshow( self.Field() )
        def animator(n):
                for i in xrange(self.every_n_steps):
                    self.step()
                mat.set_data( self.Field() )
                return [mat]
        ani = animation.FuncAnimation(fig, animator,
                            interval=2,blit=True) 
        try:
            plt.show()
        except:
            print "Catch!"



def random_location(width, height):
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)
    return [x,y]


def main():
    num_args = []
    str_args = []
    for arg in sys.argv[1:]:
        try:
            num_args.append(int(arg))
        except:
            str_args.append(arg)
    if str_args == []:
        myLangton = Langton(*num_args)
    else:
        myLangton = Langton(*num_args, rule=str_args[0])
    
    myLangton.mainloop()


if __name__ == '__main__':
    main()
