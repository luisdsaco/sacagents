#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:08:39 2022

@author: luisdsaco

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
from sacagents import AgentStopped, Agent, SpyAgent, CounterAgent

def testmessage(ag):
    print ('The current status of created agent ', ag.ID(), ' is ',
           ag.status())
    print ("The total number of agents is ", Agent.totalAgents())

if __name__ == "__main__":
    
    print ("Sacagents 0.0.1: (C) 2022 Luis Díaz Saco")
    
    # Testing Creation and Cloning
    
    ag1 = Agent(0)
    testmessage(ag1)
    ag2 = Agent(5)
    testmessage(ag2)
    ag3 = ag1.clone()
    testmessage(ag3)
    ag4 = SpyAgent('English')
    testmessage(ag4)
    ag5 = CounterAgent()
    testmessage(ag5)
    
    # Testing direct execution
    
    aglist = [ag1,ag2,ag3,ag4]
    
    for ag in aglist:
        ag.sendmessage('Run')

    for ag in aglist:
        ag.sendmessage('Stop')
        
    for ag in aglist:
        if ag.is_alive():
            ag.join()
    
    # Testing threded operations
    
    for i in range(5):
        print("Send message ",i)
        ag5.sendmessage('Thread')
    
    ag5.sendmessage('Stop')
    if ag5.is_alive():
        ag5.join()

    # Testing delayed operations
    # German agents only confess after 10 attempts
    # There is programmed a delayed confession
    
    ag4 = SpyAgent('German')
    for i in range(10):
        ag4.sendmessage('Run')
    testmessage(ag4)
    ag4.sendmessage('Timer')
    ag4.sendmessage('Stop')
    ag4.join()

    # Testing erroneous commands
    
    ag5 = SpyAgent('Spanish')
    testmessage(ag5)
    ag5.sendmessage('Err')
    ag5.sendmessage('Stop')
    ag5.join()

    # Testing invalid data and exception handling

    ag3 = SpyAgent('French')
    testmessage(ag3)
    ag3.sendmessage('Run')
    ag3.sendmessage('Stop')
    ag3.join()
    ag3.addconfession('French','Je suis un espion américain')
    try:
        ag3.sendmessage('Run')
        ag3.sendmessage('Stop')
        ag3.join()
    except AgentStopped:
        print('Cannot receive messages again')

   # Testing the modificacion of the status

    ag3 = SpyAgent('French')
    ag3.addconfession('French','Je suis un espion américain')
    try:
        ag3.sendmessage('Run')
        ag3.sendmessage('Stop')
        ag3.join()
    except AgentStopped:
        print('Cannot execute it again')
    
    print ("End of program before")
    
    # Delayed messages will appear after the last print command
