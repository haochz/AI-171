# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from enum import Enum

class direc(Enum):
    RIGHT=3
    UP=2
    LEFT=1 
    DOWN=0

class MyAI ( Agent ):



    def __init__(self):
        self.curr_direction = direc.RIGHT
        self.rows=1
        self.cols=1
    #      other necessary paramters
        self.visited= set({(1,1)})
        self.go_back_route=[]
   
        self.stack = []
        self.goal=True
        self.gold = False
        self.father_node_dict = {(1,1):(0,0)}
        self.action = None
        self.allsafe=set({(1,1)})
        self.top_bound=None
        self.right_bound=None
        self.notpit=set()
        self.notwum=set()
        self.wum_alive=True
        self.shoot=False
        self.last=True
        self.wum_space=[]
        self.return_path=[]

    def safe(self,stench,breeze,glitter):
       
        if(breeze==False):
            if(self.rows>1):
                self.notpit.add((self.rows-1,self.cols))
            if(self.cols>1):
                self.notpit.add((self.rows-1,self.cols))
            if(self.top_bound==None or self.rows<self.top_bound):
                self.notpit.add((self.rows+1,self.cols))
            if(self.right_bound==None or self.cols<self.right_bound):
                self.notpit.add((self.rows,self.cols+1))

            
        if(stench==False or self.wum_alive==False):
            if(self.rows>1):
                self.notwum.add((self.rows-1,self.cols))
            if(self.cols>1):
                self.notwum.add((self.rows-1,self.cols))
            if(self.top_bound==None or self.rows<self.top_bound):
                self.notwum.add((self.rows+1,self.cols))
            if(self.right_bound==None or self.cols<self.right_bound):
                self.notwum.add((self.rows,self.cols+1))
                
        for each_pit in self.notpit:
            if(each_pit in self.notwum):
                self.allsafe.add(each_pit)

                
    

    def get_around_room(self):
        around_room_list=[]
        if(self.right_bound==None or self.cols<self.right_bound):
            around_room_list.append((self.rows,self.cols+1))
        if(self.top_bound==None or self.rows<self.top_bound):
            around_room_list.append((self.rows+1,self.cols))
        if(self.cols>1):
            around_room_list.append((self.rows,self.cols-1))
        if(self.rows>1):
            around_room_list.append((self.rows-1,self.cols))


        father_node=self.father_node_dict[(self.rows,self.cols)]
        if(father_node in around_room_list):
            around_room_list.remove(father_node)
        return around_room_list

    def move_to_next(self,next_rows,next_cols):
        if(self.rows+1==next_rows):
            if(self.curr_direction==direc.UP):
                self.rows=self.rows+1
                self.visited.add((self.rows,self.cols))
                return Agent.Action.FORWARD
            if(self.curr_direction==direc.LEFT):
                self.curr_direction=direc.UP
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.RIGHT):
                self.curr_direction=direc.UP
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.DOWN):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_LEFT
                        
        if(self.rows-1==next_rows):
            if(self.curr_direction==direc.RIGHT):
                self.curr_direction=direc.DOWN
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.LEFT):
                self.curr_direction=direc.DOWN
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.DOWN):
                self.rows=self.rows-1
                self.visited.add((self.rows,self.cols))
                return Agent.Action.FORWARD
            if(self.curr_direction==direc.UP):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_RIGHT
        if(self.cols+1==next_cols):
                    
            if(self.curr_direction==direc.RIGHT):
                self.cols=self.cols+1
                self.visited.add((self.rows,self.cols))
                return Agent.Action.FORWARD
            if(self.curr_direction==direc.UP):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.DOWN):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.LEFT):
                self.curr_direction=direc.UP
                return Agent.Action.TURN_RIGHT
        if(self.cols-1==next_cols):
            if(self.curr_direction==direc.LEFT):
                self.cols=self.cols-1
                self.visited.add((self.rows,self.cols))
                return Agent.Action.FORWARD
            if(self.curr_direction==direc.UP):
                self.curr_direction=direc.LEFT
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.DOWN):
                self.curr_direction=direc.LEFT
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.RIGHT):
                self.curr_direction=direc.DOWN
                return Agent.Action.TURN_RIGHT
    def kill_wum(self,coord):
        if(self.rows+1==coord[0]):
            if(self.curr_direction==direc.UP):
                self.shoot=True
                return Agent.Action.SHOOT
            if(self.curr_direction==direc.LEFT):
                self.curr_direction=direc.UP
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.RIGHT):
                self.curr_direction=direc.UP
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.DOWN):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_LEFT

    
        if(self.rows-1==coord[0]):
            if(self.curr_direction==direc.RIGHT):
                self.curr_direction=direc.DOWN
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.LEFT):
                self.curr_direction=direc.DOWN
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.DOWN):
                self.shoot=True
                return Agent.Action.SHOOT
            if(self.curr_direction==direc.UP):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_RIGHT

        if(self.cols+1==coord[1]):
            if(self.curr_direction==direc.RIGHT):
                self.shoot=True
                return Agent.Action.SHOOT
            if(self.curr_direction==direc.UP):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.DOWN):
                self.curr_direction=direc.RIGHT
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.LEFT):
                self.curr_direction=direc.UP
                return Agent.Action.TURN_RIGHT


        if(self.cols-1==coord[1]):
            if(self.curr_direction==direc.LEFT):
                self.shoot=True
                return Agent.Action.SHOOT
            if(self.curr_direction==direc.UP):
                self.curr_direction=direc.LEFT
                return Agent.Action.TURN_LEFT
            if(self.curr_direction==direc.DOWN):
                self.curr_direction=direc.LEFT
                return Agent.Action.TURN_RIGHT
            if(self.curr_direction==direc.RIGHT):
                self.curr_direction=direc.DOWN
                return Agent.Action.TURN_RIGHT




    def getAction( self, stench, breeze, glitter, bump, scream ):
        current = (self.rows,self.cols)
        if (scream==True):
            self.wum_alive=False
        if(self.rows==1 and self.cols==1):
            if(breeze==True):
                return Agent.Action.CLIMB
            if(stench==True and self.wum_alive==True and self.shoot==False):
                self.shoot=True
                return Agent.Action.SHOOT
            if(stench==True and self.wum_alive==True and self.shoot==True):
                if(breeze==False):
                    self.notwum.add((1,2))
                    self.allsafe.add((1,2))
                    self.notwum.add((2,3))
                    self.notwum.add((4,1))
                    self.notwum.add((3,2))
                    self.wum_space.append((2,1))
                else:
                    return Agent.Action.CLIMB

            
        
        if(glitter==True):
            self.gold=True
            return Agent.Action.GRAB
        if(self.gold==False):   #gold is not found yet
            if (bump==True):
                if(self.curr_direction==direc.RIGHT):
                    self.right_bound==self.cols
                    self.cols=self.cols-1
                if(self.curr_direction==direc.UP):
                    self.top_bound=self.rows
                    self.rows=self.rows-1
                current=(self.rows,self.cols)
        #               return self.move_to_next(self.father_node_dict[current][0],self.father_node_dict[current][1])
            
            self.safe(stench,breeze,glitter)
            if(stench==True and self.wum_alive==True and self.shoot==False):
            
                if(len(self.wum_space)==0):
                    for each in self.get_around_room():
                        self.wum_space.append(each)
                else:
                    for each in self.wum_space:
                        if (each not in self.get_around_room()):
                            self.wum_space.remove(each)
                    if(len(self.wum_space)==1):
                        return self.kill_wum(self.wum_space[0])
    
            for possible_choice in self.get_around_room():
                if((possible_choice in self.allsafe) and (possible_choice not in self.visited) ):
                    self.father_node_dict[possible_choice]=(self.rows,self.cols)
                    return self.move_to_next(possible_choice[0],possible_choice[1])


            if(current==(1,1)):
                return Agent.Action.CLIMB
                        
            return self.move_to_next(self.father_node_dict[current][0],self.father_node_dict[current][1])
                


        if(self.gold==True):
            if(current==(1,1)):
               return Agent.Action.CLIMB

            if (current[0]-1,current[1]) in self.visited and self.last==True:
                return self.move_to_next(current[0]-1,current[1])
            elif (current[0],current[1]-1) in self.visited and self.last==True:
                return self.move_to_next(current[0],current[1]-1)
            else:
                self.last=False
                return self.move_to_next(self.father_node_dict[current][0],self.father_node_dict[current][1])



 

                                        







     
