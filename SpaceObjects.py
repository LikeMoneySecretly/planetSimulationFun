# -*- coding: utf-8 -*-
"""
"""
import random
class Objects:
    #All spacial objects must be recorded as an object here, hence the many potential variables.
    def __init__(self,name,xVel,yVel,xPos,yPos,radius,mass,orbitalRadius):
        self.name = name
        self.XVel = xVel
        self.YVel = yVel
        self.radius = radius
        self.mass = mass
        
        #Stores satellite data (can be used for other things as well)
        self.satellite=False
        self.target = []
        self.commands = []
        self.objectives=[]
        self.ratios=[]
        
        self.orbitalPeriod=0
        
        if orbitalRadius>0 and xPos==0:#Simple way of calculating initial conditions,
        #Designed to be relatively foolproof as well
            self.positionsX = orbitalRadius
            self.position = [orbitalRadius,yPos]
        else:
            self.positionsX = xPos
            self.position = [xPos,yPos]
        
        self.positionsY = yPos
        self.velocity = [xVel,yVel]
        self.oldPositions=[]#Used to plot everything out
        self.oldVelocities = []
        self.orbitalRadius = float(orbitalRadius)
        self.force = [0,0]
        self.acceleration=[0,0]
        self.oldAccel=[0,0]
        self.velCounter=0
        self.potentialEnergy=0.0
        self.magVelocity = 0.0
        
    #Not all of the below is necessary, however it can be easier to comprehend
    #If the code in other classes uses these methods
    def setOrbitalPeriod(self,newOrbitalPeriod):
        self.orbitalPeriod=newOrbitalPeriod
    def setObjective(self,objective):
        self.objectives.append(objective)
    def inputTarget(self,targets):#input a list of satellite targets
        self.target = targets
    def inputCommand(self,commands):#input a list of satellite commands
        self.commands = commands
    def isSatellite(self,boolean):
        self.satellite=boolean
    def setMagVel (self,newMagVel):
        self.magVelocity = newMagVel
    def addPotentialE(self,newPotential):
        self.potentialEnergy=newPotential
    def addOldVel (self,vel):
        self.oldVelocities.append(vel)
    def addOldPos (self,pos):
        self.oldPositions.append(pos)
    def setForce (self,newForce):
        self.force = newForce
        return self.force
    def setAccel (self, newAccel):
        self.acceleration = newAccel
        return self.acceleration
    def setName (self,newName):
        self.name=newName
        return self.name
    def setXVelocity(self,newXVel):
        self.objectXVel = newXVel
        return self.objectXVel
    def setYVelocity(self,newYVel):
        self.objectYVel = newYVel
        return self.objectYVel
    def setMass(self,newMass):
        self.mass = newMass
        return self.mass
    def setRadius (self,newRadius):
        self.radius = newRadius
        return self.radius
    def setOrbitalRadius (self,newOrbitRadius):
        self.orbitalRadius = newOrbitRadius 
        return self.orbitalRadius
    def setXpositions(self,newPositionsX):
        self.positionsX = newPositionsX
        return self.positionsX
    def setYpositions(self,newPositionsY):
        self.positionsY = newPositionsY
        return self.positionsY
    def setPosition(self,newPosition):
        self.position = newPosition
        self.positionsX = newPosition[0]
        self.positionsY = newPosition[1]
    def setVelocity (self,newVelocity):
        try:
            newVelocity =  newVelocity()
        except:
            oops="If this triggers I've accidentally let a Pos object into the velocity"
        self.velocity = newVelocity
        self.XVel = newVelocity[0]
        self.YVel = newVelocity[1]
    def setOldAccel (self,oldAccel):
        self.oldAccel=oldAccel
    def incVelCounter(self):
        self.velCounter=self.velCounter+1
    
