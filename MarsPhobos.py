import ProcessData as pp#Code was split into three sections for neatness
import SpaceObjects as so
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class mainClass:   
    numTimeStep=0
    calculateOrbitalPeriods=False
    displayEnergyGraph=False
    spaceObjects = []
    satellites = []#includes asteroids
    patches=[]
    sizeTimeStep=0
    focalPoint =0 #Basically the place holder for the sun. Called focal point as this code works
    #With no hard coded values, so naturally assumes any object without a specified orbital radius
    #is a focal point.
    def process(self):
        halt =0
        sys = mainClass()
        #Just some general file processing below (Completely useless in terms of maths)
        fileread = open("ProjectTextFile.txt","r")
        lines = fileread.readlines()
        
    
        self.sizeTimeStep = 0.0
        self.numTimeStep = 0.0
        for b in range (len(lines)):
            value= str(lines[b])
            if value.__contains__("Object"):
                #Text processing gang rise up
            
                lines[b+1]=float(lines[b+1].replace("mass = ",""))
                
                lines[b+2]=lines[b+2].replace("initial position = ","")
                position = sys.processPositions(lines[b+2])
                xPos = position[0]
                Ypos = position[1]
                xVel = 0
                yVel = 0
                magVel=0
                if (str(lines[b+3])).__contains__("initial velocity"):
                    lines[b+3]=lines[b+3].replace("initial velocity = ","")
                    position = sys.processPositions(lines[b+3])
                    xVel = position[0]
                    yVel = position[1]
                if (str(lines[b+3])).__contains__("magnitude velocity"):
                    lines[b+3]=lines[b+3].replace("magnitude velocity = ","")
                    magVel = float(lines[b+3])
                lines[b+4]=lines[b+4].replace("radius = ","")
                radius = float(lines[b+4])
                pd = pp.Backend() 
                
            
                mass = lines[b+1]
                name = lines[b].replace("Object"," ")
                name = name.replace(" ","")
                name = name.replace(":","")
                
                if (str(lines[b+5])).__contains__("orbital radius"):
                    print("Who has a big radius "+name)
                    lines[b+5]=lines[b+5].replace("orbital radius = ","")
                    orbitalRadius = float(lines[b+5])
                    lines[b+6]=lines[b+6].replace("orbital period = ","")
                    orbitalPeriod = float(lines[b+6])
                    planet=so.Objects(name, xVel,yVel,xPos,Ypos, radius,mass,orbitalRadius)
                    planet.setOrbitalPeriod(orbitalPeriod)
                    b=b+6
                elif str(lines[b+5]).__contains__("focal point"):
                    self.focalPoint=so.Objects(name, xVel,yVel,xPos,Ypos, radius,mass,0.0)
                    planet=self.focalPoint    
                    b=b+5
                #------Satellite Targeting info-----
                #Only works for Mars and Earth, fly by for Mars and landing for Earth
                
                elif str(lines[b+5]).__contains__("satellite"): 
                    #Was too complicated to expand this out
                    planet=so.Objects(name, xVel,yVel,xPos,Ypos, radius,mass,0.0) 
                    planet.isSatellite(True)
                    lines[b+6]=lines[b+6].replace("target = ","")
                    words = lines[b+6].split(",")
                    targets = []
                    commands = []
                    for word in words: #Commands come at the end of the string,
                        if word.__contains__("fly by"):
                            commands.append(word)
                        elif word.__contains__("land"): 
                            commands.append(word)
                        else:
                            targets.append(word)
                            
                    planet.inputCommand(commands)
                    planet.inputTarget(targets)
                    self.spaceObjects.append(planet)
                    self.satellites.append(planet)
                    b=b+6
                if magVel>0:
                    planet.setMagVel(magVel)
                if planet.satellite==False:
                    self.spaceObjects.append(planet)
                
            elif value.__contains__("Simulation Details"):
                self.sizeTimeStep=float(lines[b+1].replace("timestep(s)= ",""))
                self.numTimeStep = float(lines[b+2].replace("number of timesteps = ",""))
                #calculateOrbitalPeriods is functionally useless
                self.calculateOrbitalPeriods = bool(lines[b+3].replace("orbital period = ",""))
                lines[b+4]=lines[b+4].replace("display energies = ","")
                lines[b+4]=lines[b+4].replace(" ","")
                if lines[b+4].__contains__("True"):
                    self.displayEnergyGraph = True
                print("Fuck "+str(self.displayEnergyGraph)+" "+str(bool(lines[b+4])))
                break
        
        for planet in self.spaceObjects:# Create inital velocity, acceleration and force
            boole= planet.name.__contains__(self.focalPoint.name)
            if boole==False and planet.satellite==False:
                planet= pd.initialValues(self.focalPoint, planet)
            
        pd = pp.Backend() ## makes reaching ProcessData easier
        p =0
        writeFile = open("Outputs.txt","w")
        satVel=[]
        angles=[]
        for satellite in self.satellites:
            if satellite.magVelocity>0:
                angles = np.arange(0,100,10)
                velo=satellite.magVelocity
                for angle in angles:
                    
                    xVelocity = math.cos(math.radians(angle))*velo
                    yVelocity = math.sqrt((velo*velo)-(xVelocity*xVelocity))
                    satVel.append(Pos(xVelocity,yVelocity,satellite.name))
                value = satVel[0]()
                satellite.setVelocity(value)
        satVelCounter=0#Satellite velocity counter
        self.energyList=[]
        self.timeList=[]
        progress=True
        ratioList=[]
        oldSpaceObjects=self.spaceObjects
        V=1
        while satVelCounter<V:
            print("FFS"+str(satVelCounter))
            v=0
            self.energyList = []
            self.timeList=[]
            initialPositions=[]
            self.spaceObjects=oldSpaceObjects
            
            
            for planet in self.spaceObjects:
                #Update the satellite velocity inside the spaceObjects list.
                #With the new iterated initial velocity
                
                initPos=Pos(planet.position[0],planet.position[1],planet.name)
                initialPositions.append(initPos)
                
                
                for satellite in self.satellites:
                    if satellite.name in planet.name:
                        self.spaceObjects[v]=satellite
                v=v+1
                

            p=0
            closestDistances=[]
            firstTime=True
            while p<=self.numTimeStep:
                totalEnergy = pd.totalKineticEnergy(self.spaceObjects, self.sizeTimeStep)-pd.totalPotentialEnergy(self.spaceObjects)
                self.energyList.append(totalEnergy)
                self.timeList.append(self.sizeTimeStep*p)
                writeFile.write(str(totalEnergy)) 
                writeFile.write('\n')
                objects = pd.timeStepPosition(self.spaceObjects, self.sizeTimeStep)
                self.spaceObjects = objects
                if p!=0:
                    planetNum=0
                    for planet in self.spaceObjects:
                        for initPos in initialPositions:
                            currentPos=planet.position
                            initialPos = initPos()
                            diffX = currentPos[0]-initialPos[0]
                            diffY = currentPos[1]-initialPos[1]
                            distance= math.sqrt(diffX*diffX+diffY*diffY)
                            if firstTime:
                                dist=Distance(distance,currentPos,planet.name)
                                dist.setTime(self.sizeTimeStep*p)
                                closestDistances.append(dist)
                
                            else:
                                if closestDistances[planetNum]()>distance:
                                    dist=Distance(distance,currentPos,planet.name)
                                    dist.setTime(self.sizeTimeStep*p)
                                    closestDistances[planetNum]=dist
                    
                
                        planetNum=planetNum+1
                        firstTime=False
                p=p+1
                
            print("OML"+str(len(closestDistances)))
            #-------------Orbital Period calculater below----
            for distance in closestDistances:
                
                orbitalPeriod=distance.time
                
                difference=0
                for planet in self.spaceObjects:
                    try:
                        if planet.name in distance.name:
                            if planet.orbitalPeriod>0:
                                difference=orbitalPeriod/planet.orbitalPeriod
                    except:
                        haha="go away errors"
                
                print(distance.name+"'s orbital Period is "+str(orbitalPeriod))  
                #Take difference in meters 
                print(distance.name+"'s period has a difference of roughly, "+str(difference)+"% from what is expected")
                
            
            
            if len(self.satellites)==0:#Exits out instantly if theres no satellites
                break
            g=0
            for satellite in self.satellites:
                #Satellite code doesn't work right
                targets = satellite.target
                t=0
                ratios=[]
                for target in targets:
                    flyBy=False
                    land = False
                    if "fly by"in satellite.commands[t]:
                        flyBy=True
                    elif "land" in satellite.commands[t]:
                        land = True
                    t=t+1
                    counter=0.0
                    
                    for planet in self.spaceObjects:
                        
                        if target in planet.name:
                            velocity=0
                            looper=0
                            smallestDist=0
                            for oldPos in satellite.oldPositions:
                                satPos=oldPos()
                                velocity = satellite.velocity
                                #Calc velocity magnitude
                                velocity = math.sqrt(velocity[0]*velocity[0]+velocity[1]*velocity[1])
                                pos =planet.oldPositions[looper]()
                                ground = [planet.radius +pos[0],planet.radius+pos[1]]
                                
                                diffX = satPos[0]-ground[0]
                                diffY = satPos[1]-ground[1]
                                distance= math.sqrt(diffX*diffX+diffY*diffY)
                                if smallestDist==0:
                                    smallestDist=distance
                                elif smallestDist>distance:
                                    smallestDist=distance
                                looper = looper+1

            satVelCounter=satVelCounter+1
        
                    
        # Diff1=1-rat2
        # Diff2=1-comRat
        # Diff1=Diff1*Diff1
        # Diff2=Diff2*Diff2
        
        writeFile.close()
        
        fileread.close()
        return False
    def updateObjectives(self,satellite,newObjective):
        count=0
        for objective in satellite.objectives:
            if objective.target in newObjective.target:
                if objective.distance>newObjective.distance:
                    satellite.objectives[count]=newObjective
                
            count = count+1
    def animate(self,i):##Animates the planets every timestep i
        for p in range(len(self.patches)):
            position=self.spaceObjects[p].oldPositions[i]
            position = position()##Should call the callable in the Pos class
            # if self.spaceObjects[p].name.__contains__("Perseverance"):
            #     print("Satellite="+str(position))
            self.patches[p].center = (position[0],position[1])
            
        return self.patches
        
    
    def processPositions(self,line): ##Process' the brackets in the file for storing positions
        line = line.replace(" ","")
        line = line.replace("(","")
        line = line.replace(")","")
        sides = line.split(",")
        firstOne = sides[0]
        xPos=0
        yPos = 0
        pd = pp.Backend()
        try: ##Exception handling cuz i chose the lazy way
            xPos = float(firstOne)
            try:
                secondNum = sides[1]
                yPos = float(secondNum)
            except:
                yPos =0
        except:
            xPos =0
        coords = [xPos,yPos]
        return coords
    
    def bigAnimation(self):##Where all the animation gets drawn up
    
        if self.displayEnergyGraph==True:
            plt.plot(self.timeList,self.energyList,"g-")
            plt.xlabel("Time(s)")
            plt.ylabel("Energy (J)")
            plt.title("Energy vs Time")
            plt.show()
        else:
            fig = plt.figure()
            ax = plt.axes()
            ax.set_xlim(-1e12,+3e12)
            ax.set_ylim(-1e12,+3e12)
            ax.set_xlabel("meters")
            ax.set_ylabel("meters as well")
            pd = pp.Backend()
            colors = ["r","y","g","b","c","m"]#So all the other planets can have fun colours
            a=0
            for planet in self.spaceObjects:
                if a==7:
                    a=0
                pos = planet.oldPositions[0]()
                colour = colors[a]
                radius = 69600000e3/5#Multiplied out the sun a few times so that it was fully visible
                #Then
                if planet.name.__contains__("Sun"):#People complain if you don't have the right colours
                    colour = "y"
                    radius = 69600000e3/3
                elif planet.name.__contains__("Earth"):
                    colour="b"
                elif planet.name.__contains__("Mars"):
                    colour="r"
                elif planet.name.__contains__("Mercury"):
                    colour="m"
                elif planet.name.__contains__("Perseverance"):
                    colour="m"      
                patch = plt.Circle((pos[0],pos[1]),radius,color=colour,animated=True)
                self.patches.append(patch)
                ax.add_patch(patch)
                print("a="+str(a))#Breaks occasionally if this line isn't in
                a=a+1
            
            self.anim = FuncAnimation(fig, self.animate, frames = int(self.numTimeStep),repeat = False, interval = 200, blit = True)
            plt.show()
def main():
    mainShite = mainClass()#Initialising the class
    broken = mainShite.process()#Where all the maths happens
    if broken == True:
        print ("Follow the above instructions")
        return
    mainShite.bigAnimation() #The animation stuff

class Pos:#Holds position values
    def __init__(self,xValue,yValue,identifier):
        self.xVal = float(xValue)
        self.yVal = float(yValue)
        self.ident = identifier ##Attach identifier to each position so historical Pos' are easier
    def __call__(self,*args,**kwargs):##Returns the float position with no identifier
        return [self.xVal,self.yVal]

class Distance:
    def  __init__(self,distance,position,name):
        self.distance=distance
        self.position=position
        self.name=name
        self.time=0
        self.target=""
    def setTime(self,newTime):
        self.time=newTime
    def setTarget(self,newTarget):
        self.target=newTarget
    def calcDist(self,ground,currentPos):#Ground should be the ground of the planet
    
        diffX = currentPos[0]-ground[0]
        diffY = currentPos[1]-ground[1]
        self.distance= math.sqrt(diffX*diffX+diffY*diffY)
        return self.distance
    def __call__(self, *args,**kwargs):
        return self.distance

class Objective: #Makes processing of satellite objectives easier
    def __init__(self,distance,target,satellite_name,velocity,angle):#Angle in degrees
        self.distance=float(distance)
        self.target = target
        self.velocity = velocity
        self.name = satellite_name
        self.angle=angle
    def setNewVeloAndDist (self,distance,velocity):
        self.distance=distance
        self.velocity=velocity
    def __call__(self, *args,**kwargs):#Returns the distance achieved
        return self.distance
    def inform(self):
        print(self.name+" passed within "+str(self.distance)+" of "+self.target+" With velocity "+str(self.velocity))
main()