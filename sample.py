#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:08:39 2022

@author: luis
"""
from sacagents import Agent, SpyAgent, CounterAgent

if __name__ == "__main__":
    
    print ("Sacagents 0.0.1: (C) Saconsulting Servicios Avanzados de"
           " Consultoría SLU")
    ag1 = Agent(0)
    print ('El estado actual del agente creado ', ag1.ID(), ' es ',
           ag1.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    ag2 = Agent(5)
    print ("El estado actual del agente creado ", ag2.ID(), "es ",
           ag2.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    ag3 = ag1.clone()
    print ("El estado actual del agente creado ", ag3.ID(), "es ",
           ag3.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    ag4 = SpyAgent(-1)
    print ("El estado actual del agente creado ", ag4.ID(), "es ",
           ag4.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    ag5 = CounterAgent()
    print ("El estado actual del agente creado ", ag5.ID(), "es ",
           ag5.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    aglist = [ag1,ag2,ag3,ag4]
    
    for ag in aglist:
        ag.sendmessage('Run')

    for ag in aglist:
        ag.sendmessage('Stop')
        
    for ag in aglist:
        if ag.is_alive():
            ag.join()
    
    for i in range(5):
        print("Send message ",i)
        ag5.sendmessage('Thread')
    
    ag5.sendmessage('Stop')
    if ag5.is_alive():
        ag5.join()
    
    ag4 = SpyAgent(-1)
    print ("El estado actual del agente creado ", ag4.ID(), "es ",
           ag4.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    ag4.sendmessage('Timer')
    ag4.sendmessage('Stop')
    ag4.join()
    ag5 = SpyAgent(-1)
    print ("El estado actual del agente creado ", ag4.ID(), "es ",
           ag4.status())
    print ("El número total de agentes es ", Agent.totalAgents())
    ag5.sendmessage('Err')
    ag5.sendmessage('Stop')
    ag5.join()
    print ("End of program before")
    
