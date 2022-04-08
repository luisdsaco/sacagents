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

__all__ = ['AgentStoppedError', 'Agent', 'SpyAgent', 'CounterAgent']
__version__ = '0.0.1'
__author__ = 'luisdsaco'

from threading import Thread, Condition, Timer, Event, RLock
from queue import Queue

class AgentStoppedError(Exception):
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

    total_agents = 0
    io_lock = RLock()
    
    def __init__(self,initialstate):
        Thread.__init__(self)
        self.id = Agent.total_agents
        Agent.total_agents += 1
        self.state = initialstate
        self.message = 0
        self.send = Condition()
        self.message_list = Queue()
        self.is_Running = False
        self.receive = Condition()
        self.start()
        self.action = Thread(target=self.run_action)
        self.ev = Event()
        self.action.start()
        self.message_op={"Run": self.main_op,
                        "Thread": self.main_thread_op,
                        "Timer": self.main_timer_op,
                        "Stop": self.main_op_stop
                        }

    def status(self):
        return self.state
    
    def ID(self):
        return self.id
    
    def print_locked(self,*args,**kargs):
        Agent.io_lock.acquire()
        print(*args,**kargs)
        Agent.io_lock.release()
       
    def main_op(self):
        self.print_locked('Running', self.ID(), 'with status:',
                          self.status())
    
    def main_thread_op(self):
        thd = Thread(target=self.main_op)
        thd.start()
        
    def main_timer_op(self,time=3):
        thd = Timer(time,self.main_op)
        thd.start()
                       
    def main_op_stop(self):
        pass
    
    def set_status(self,st):
        self.state = st
        
    def total_num_agents():
        return Agent.total_agents    

    def clone(self):
        cn = Agent(self.status())
        return cn
    
    def run_action(self):
        while self.is_Running:
            self.ev.wait()
            self.process_message_list()
            self.ev.clear()

    def send_message(self,msg):
        if not self.is_Running:
            raise AgentStoppedError
            return
        with self.send:
            self.message = msg
            self.send.notify()
        with self.receive:
            self.receive.wait()
    
    def process_message(self):
        cmd = self.message_list.get()
        try:
            self.message_op[cmd]()
        except KeyError:
            print("Command Error")
        finally:
            self.message_list.task_done()
            
    def process_message_list(self):
        while not self.message_list.empty():
            self.process_message()

    def run(self):
        self.is_Running = True
        while self.is_Running:
            with self.send:
                self.send.wait()
                self.message_list.put(self.message)
                if self.message == 'Stop':
                    self.is_Running = False
                self.ev.set()
            with self.receive:
                self.receive.notify()
        self.message_list.join()


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
        
    def main_op(self):
        if self.ag.status() < 10 and self.status() == 'German':
            self.ag.send_message('Run')
            self.print_locked('Nein')
        else:
            self.fake_confession()
            
    def main_op_stop(self):
        self.ag.send_message('Stop')
        self.ag.join()
        Agent.main_op_stop(self)
            
    def add_confession(self,l,m):
        self.confession.update([(l,m)])
        
    def fake_confession(self):
        try:
            self.print_locked(self.confession[self.state])
        except KeyError:
            print("Language Error")
        
class CounterAgent(Agent):
    """
    Counter Agent: Increases the state when its operation is runned
    """
    def __init__(self,initialstate=0):
        Agent.__init__(self,initialstate)
    
    def main_op(self):
        self.state += 1
        Agent.main_op(self)
