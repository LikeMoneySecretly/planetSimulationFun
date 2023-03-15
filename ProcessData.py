# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:50:16 2022

@author: Lucas

Ok so calculate the first position
"""
import math
import SpaceObjects as so

class Backend:#Here be monsters, designed to

    def timeStepPosition (self,objects,stepTime):
        
        oldObjects =objects#to stop messess occuring
        c=0
        for o in range(len(objects)): ## r^2 moment, unavoidable however
            name = objects[o].name
            sys = Backend()
            objects[o]=self.totalForce(objects[o],oldObjects,True)
            accel1 = sys.calculateAccel(objects[o].force, objects[o].mass) 
            #accel1=a(t), objects[o].acceleration = a(t-deltaT),objects[o].oldAccel = a(t-2*deltaT)
            #vel1 = v(t) i.e. the current velocity of the object
            if objects[o].velCounter>0:
                #Velocity requires three different accelerations to be calculated
                #On the first go round there is only access to a maximum of two 
                #The current accel and the accel before (initial accel), as a result velocity must wait a turn
                #before being calculated. This doesn't leave a gap in the velocities as the initial velocity
                #Fills this gap and this equation only calculates the CURRENT velocity not the next velocity.
                vel1 = sys.incrementVelocity(stepTime, accel1,objects[o].acceleration,objects[o].oldAccel,objects[o].velocity)
                objects[o].addOldVel(Pos(objects[o].XVel,objects[o].YVel,objects[o].name))
                objects[o].setVelocity(vel1)

            #pos1= r(t+deltaT) (i.e. the next position)
            pos1 = sys.incrementPosition(stepTime,objects[o].velocity,objects[o].position,accel1,objects[o].acceleration)
            #print(name+" who gets here")
            objects[o].addOldPos(Pos(objects[o].positionsX,objects[o].positionsY,objects[o].name))
            objects[o].setPosition(pos1) 
            objects[o].setOldAccel(objects[o].acceleration)
            #Storing previous values in order to calculate future velocities and positions.
            objects[o].setAccel(accel1)
            objects[o].incVelCounter()#increment vel counter, redundant after it's above 0
            
        return objects
    
    def totalForce (self,targetObject,otherObjects,calcPotential):
        targetObject.setForce([0,0])
        totalPotEnergy = 0
        for p in range(len(otherObjects)):##Calculates the current unbalanced force acting on objects[o]
            if otherObjects[p].name==targetObject.name:
                continue
            else:
                #Calculates the current force on the chosen object from the old positions of the objects
                if calcPotential:
                    totalPotEnergy = totalPotEnergy+self.calculatePotentialEnergy(targetObject, otherObjects[p])
                    #print("totalPotEnergy "+str(totalPotEnergy))
                calcForce = self.calculateForce(targetObject,otherObjects[p])
                oldForce = targetObject.force
                #Sum of all forces acting on the chosen object
                force= [float(oldForce[0]+calcForce[0]),float(oldForce[1]+calcForce[1])]
                
                targetObject.setForce(force)
        if calcPotential:
            targetObject.addPotentialE(totalPotEnergy)
        return targetObject
    #Generally speaking this is all very literal class names i.e. they do what the class says
    def totalPotentialEnergy (self,objects):
        total =0
        for planet in objects:
            total=total+planet.potentialEnergy
        total= total/2
        return total
                
    def incrementVelocity(self,timeStep,newAccel,accel,accelBefore,velocityBefore):
        velX = velocityBefore[0]+(1/6)*(2*newAccel[0]+5*accel[0]-accelBefore[0])*timeStep
        
        velY = velocityBefore[1]+(1/6)*(2*newAccel[1]+5*accel[1]-accelBefore[1])*timeStep
        
        newVelocity = [velX,velY]
        return newVelocity
    
    def incrementPosition(self,stepTime,oldVelocity,oldPosition,oldAccel,TurboOldAccel):
        
        newPositionX = oldPosition[0]+oldVelocity[0]*stepTime+(1/6)*(4*oldAccel[0]-TurboOldAccel[0])*stepTime*stepTime
        newPositionY = oldPosition[1]+oldVelocity[1]*stepTime+(1/6)*(4*oldAccel[1]-TurboOldAccel[1])*stepTime*stepTime
        
        newPosition = [newPositionX,newPositionY]
        return newPosition
    
    def calculateUnitVector(self,posVector):#x first y second in list
        ## Input position vector into method
        posVector[0]= float(posVector[0])
        posVector[1]= float(posVector[1])
        magnitude = math.sqrt(posVector[0]*posVector[0]+ posVector[1]*posVector[1])
        x=(1/magnitude)*posVector[0]
        y=(1/magnitude)*posVector[1]
        unitVector = [x,y]
        return unitVector
    
    def calculatePositionVector (self,position1,position2):
        x= float(position2[0])-float(position1[0])
        y= float(position2[1])-float(position1[1])
        positionVector = [x,y]
        return positionVector
    def calculatePotentialEnergy (self,targetObject,otherObject):
        g=6.67430e-11
        pos1=targetObject.position
        pos2=otherObject.position
        diff=pos1[0]-pos2[0]
        diff2=pos1[1]-pos2[1]
        distance = math.sqrt(diff*diff+diff2*diff2)
        potentialEnergy = (targetObject.mass*g*otherObject.mass)/distance
        return potentialEnergy
    def calculateForce (self,targetObject,otherObject):
        g=6.67430e-11
        
        prodMass = targetObject.mass*otherObject.mass
        sys = Backend()
        positionVector = sys.calculatePositionVector(targetObject.position, otherObject.position)
        unitVector = sys.calculateUnitVector(positionVector)
        denominator = positionVector[0]*positionVector[0]+ positionVector[1]*positionVector[1]
        
             
        forceX = (g*prodMass*unitVector[0])/denominator
        forceY = (g*prodMass*unitVector[1])/denominator
        
        force = [forceX,forceY]
        return force
        
    def calculateAccel (self,force,mass): #Force must be list
        accelX = force[0]/mass
        accelY= force[1]/mass
        accel = [accelX,accelY]
        return accel
    def stringToList (self,string):
        positions = string.split(" ")
        positions[0]=float(positions[0])
        positions[1]=float(positions[1])
        return positions
    
    def initialValues (self,focalObject,targetObject):
        g=6.67430e-11
        velY = math.sqrt(g*focalObject.mass/targetObject.orbitalRadius)
        #Y velocity is perpendicular to orbital radius
        force = (targetObject.mass*velY*velY)/targetObject.orbitalRadius
        
        targetObject.setVelocity([0,velY])
        targetObject.setAccel([0,force/targetObject.mass])
        targetObject.setForce([0,force])
        return targetObject
        
    def totalKineticEnergy(self,objects,timeStep):
        totalkinetic = 0
        for planet in objects:#Trying to keep everything nice and understandable
            velocity=planet.velocity
            magnitude1= math.sqrt(velocity[0]*velocity[0]+velocity[1]*velocity[1])
            
            kinetic1 = planet.mass*0.5*timeStep*timeStep*magnitude1
            
            totalkinetic =totalkinetic+ kinetic1
        return totalkinetic
class Pos:#Simpler to copy and paste class here rather than risk python errors by cross calling it.
    def __init__(self,xValue,yValue,identifier):
        self.xVal = float(xValue)
        self.yVal = float(yValue)
        self.ident = identifier #Identifier is used for debugging purposes mainly
    def __call__(self,*args,**kwargs):##Returns the float position with no identifier
        return [self.xVal,self.yVal]