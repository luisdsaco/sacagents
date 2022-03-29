# -*- coding: utf-8 -*-
"""
Editor de Spyder

Module to develop an architecture of agents

(C) 2017-2022 Luis Díaz Saco

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from threading import Thread, Condition, Timer, Event
from queue import Queue

class AgentStopped(Exception):
    """
    AgentStopped: Exception raised when someone tries to run an operation on
        an agent that has been stopped.
    """
    
    def __init__(self):
        Exception.__init__(self)
        print('Agent is Stopped')
   
class Agent(Thread):
    """
    Agent: Base Class to process messages between agents and to run operations
    """

    totalagents = 0
    def __init__(self,initialstate):
        Thread.__init__(self)
        self.id = Agent.totalagents
        Agent.totalagents += 1
        self.state = initialstate
        self.message = 0
        self.send = Condition()
        self.messagelist = Queue()
        self.isRunning = False
        self.receive = Condition()
        self.start()
        self.action = Thread(target=self.runaction)
        self.ev = Event()
        self.action.start()
        self.messageop={"Run": self.mainop,\
                        "Thread": self.mainthreadop,\
                        "Timer": self.maintimerop,\
                        "Stop": self.mainopstop\
                        }

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
                       
    def mainopstop(self):
        pass
    
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
        if self.isRunning == False:
            raise AgentStopped
            return
        with self.send:
            self.message = msg
            self.send.notify()
        with self.receive:
            self.receive.wait()
    
    def processmessage(self):
        cmd = self.messagelist.get()
        try:
            self.messageop[cmd]()
        except KeyError:
            print("Command Error")
        finally:
            self.messagelist.task_done()
            
    def processmessagelist(self):
        while not self.messagelist.empty():
            self.processmessage()

    def run(self):
        self.isRunning = True
        while (self.isRunning):
            with self.send:
                self.send.wait()
                self.messagelist.put(self.message)
                if self.message == 'Stop':
                    self.isRunning = False
                self.ev.set()
            with self.receive:
                self.receive.notify()
        self.messagelist.join()


class SpyAgent(Agent):
    """
    SpyAgent: Demostration class inspired in the movie One, two, three
    """
    
    def __init__(self,initialstate):
        Agent.__init__(self,initialstate)
        self.confession = {'English': 'I am an American Spy',
                           'Spanish': 'Soy un espía americano',
                           'German': 'Ich bin ein Americanisher Spion'
                           }
        self.ag=CounterAgent()
        
    def mainop(self):
        if self.ag.status() < 10 and self.status() == 'German':
            self.ag.sendmessage('Run')
            print('Nein')
        else:
            self.fakeconfession()
            
    def mainopstop(self):
        self.ag.sendmessage('Stop')
        self.ag.join()
        Agent.mainopstop(self)
            
    def addconfession(self,l,m):
        self.confession.update([(l,m)])
        
    def fakeconfession(self):
        try:
            print (self.confession[self.state])
        except KeyError:
            print("Language Error")
        
class CounterAgent(Agent):
    """
    Counter Agent: Increases the state when its operation is runned
    """
    def __init__(self,initialstate=0):
        Agent.__init__(self,initialstate)
    
    def mainop(self):
        self.state += 1
        Agent.mainop(self)
