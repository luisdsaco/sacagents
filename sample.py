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

from sacagents import AgentStoppedError, Agent, SpyAgent, CounterAgent
from sacagents import __version__ as sac_ver, __author__ as sac_auth

def test_message(ag):
    ag.print_locked('The current status of created agent', ag.ID(), 'is',
           ag.status())
    ag.print_locked("The total number of agents is", Agent.total_num_agents())

if __name__ == "__main__":
    
    print("Using Sacagents ", sac_ver, ": (C) 2022 ", sac_auth)
    
    # Testing Creation and Cloning
    
    ag1 = Agent(0)
    test_message(ag1)
    ag2 = Agent(5)
    test_message(ag2)
    ag3 = ag1.clone()
    test_message(ag3)
    ag4 = SpyAgent('English')
    test_message(ag4)
    ag5 = CounterAgent()
    test_message(ag5)
    
    # Testing direct execution
    
    aglist = [ag1,ag2,ag3,ag4]
    
    for ag in aglist:
        ag.send_message('Run')

    for ag in aglist:
        ag.send_message('Stop')
        
    for ag in aglist:
        if ag.is_alive():
            ag.join()
        
    # Testing threded operations
    
    for i in range(5):
        ag5.print_locked("Send message",i)
        ag5.send_message('Thread')
    
    ag5.send_message('Stop')
    if ag5.is_alive():
        ag5.join()

    # Testing delayed operations
    # German agents only confess after 10 attempts
    # There is programmed a delayed confession
    
    ag4 = SpyAgent('German')
    for i in range(10):
        ag4.send_message('Run')
    test_message(ag4)
    ag4.send_message('Timer')
    ag4.send_message('Stop')
    ag4.join()

    # Testing erroneous commands
    
    ag5 = SpyAgent('Spanish')
    test_message(ag5)
    ag5.send_message('Err')
    ag5.send_message('Stop')
    ag5.join()

    # Testing invalid data and exception handling

    ag3 = SpyAgent('French')
    test_message(ag3)
    ag3.send_message('Run')
    ag3.send_message('Stop')
    ag3.join()
    ag3.add_confession('French','Je suis un espion américain')
    try:
        ag3.send_message('Run')
        ag3.send_message('Stop')
        ag3.join()
    except AgentStoppedError:
        print('Cannot receive messages again')

   # Testing the modificacion of the status

    ag3 = SpyAgent('French')
    ag3.add_confession('French','Je suis un espion américain')
    try:
        ag3.send_message('Run')
        ag3.send_message('Stop')
        ag3.join()
    except AgentStoppedError:
        print('Cannot execute it again')
    
    print("End of program before")
    
    # Delayed messages will appear after the last print command
