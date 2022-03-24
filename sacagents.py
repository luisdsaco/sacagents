# -*- coding: utf-8 -*-
"""
Editor de Spyder

Module to develop an architecture of agents
"""

from threading import Thread, Condition, Timer, Event

   
class Agent(Thread):

    totalagents = 0
    def __init__(self,initialstate):
        Thread.__init__(self)
        self.id = Agent.totalagents
        Agent.totalagents += 1
        self.state = initialstate
        self.message = 0
        self.send = Condition()
        self.messagelist = []
        self.isRunning = False
        self.receive = Condition()
        self.start()
        self.action = Thread(target=self.runaction)
        self.ev = Event()
        self.action.start()

    def status(self):
        return self.state
    
    def ID(self):
        return self.id
       
    def mainop(self):
        print('Running ', self.ID(), ' with status:', self.status())
    
    def mainthreadop(self):
        thd = Thread(target=self.mainop)
        thd.start()
        
    def maintimerop(self,time=3):
        thd = Timer(time,self.mainop)
        thd.start()
                       
    def setstatus(self,st):
        self.state = st
        
    def totalAgents():
        return Agent.totalagents    

    def clone(self):
        cn = Agent(self.status())
        return cn
    
    def runaction(self):
        while self.isRunning:
            self.ev.wait()
            self.processmessagelist()
            self.ev.clear()

    def sendmessage(self,msg):
        with self.send:
            self.message = msg
            self.send.notify()
        with self.receive:
            self.receive.wait()
    
    def processmessage(self):
        messageop = {"Run": self.mainop,\
                     "Thread": self.mainthreadop,\
                     "Timer": self.maintimerop\
                     }
        
        cmd = self.messagelist.pop(0)
        try:
            messageop[cmd]()
        except KeyError:
            print("Command Error")
            
    def processmessagelist(self):
        while len(self.messagelist)>0:
            self.processmessage()

    def run(self):
        self.isRunning = True
        while (self.isRunning):
            with self.send:
                self.send.wait()
                if self.message == 'Stop':
                    self.isRunning = False
                else:
                    self.messagelist.append(self.message)
                self.ev.set()
            with self.receive:
                self.receive.notify()
        self.processmessagelist()
        self.action.join()

class SpyAgent(Agent):
    def __init__(self,initialstate):
        Agent.__init__(self,initialstate)

    def mainop(self):
        print ("Ich bin ein Amerikanischer Spion")
        
class CounterAgent(Agent):
    def __init__(self,initialstate=0):
        Agent.__init__(self,initialstate)
#        self.count = initialstate
    
    def mainop(self):
        self.state += 1
        Agent.mainop(self)

