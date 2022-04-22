#Be able to have sliders and check boxes for parameters
#Move towards/with mouse movement
#!Connect with line of different strength depending on distance
#When bump into eachother reflect
#When bump into eachother change colors and mix colors (both become average of two colors)
#When bump into eachother merge to become bigger
#!Control size of particles
#Control directions particles come from
#Control acceleration of particles
#Multi Dimension
#!Bounce off walls
#Trail Time

# import os
# os.system("pip install numpy")
# os.system("pip install pygame")

import numpy as np
import pygame
import time
import random
import math
import treeset
#Is is worth deleting line from list after drawn so no duplicates or is it worse to remove it?
#make transparent not use whole screen as surface only size of thing for alpha(i.e. a line or a box around the line (surface))
#Transparency is not working
#Add transperency for particles

#default = True
particleCount = 500
screenDimension = 800,500
staringRange = 0,screenDimension[0],0,screenDimension[1]
infinteTrail = False
integerCord = False
minVelocity = 1.25
maxVelocity = 5
# screenFill = True
reflect = True
verbose = True
partilceSize = 1
lineSize = 1
tickRate =10000
lineDist = 100
dynamicLineBrightness = True
variableLineColor = True
transparent = False
staticColor = 0,255,0

partilceSizeH = partilceSize//2
staticColor = np.array(staticColor,dtype=np.uint8)

#screenDimension = 1920,1080

if integerCord:
    minVelocity = int(math.ceil(minVelocity))
    maxVelocity = int(math.floor(maxVelocity))

particlesX = np.random.uniform(staringRange[0],staringRange[1],size=particleCount)
particlesY = np.random.uniform(staringRange[2],staringRange[3],size=particleCount)
particlesPos = np.stack((particlesX, particlesY), axis = -1)
particlesVelocity = np.random.uniform(minVelocity,maxVelocity,size=(particleCount,2))
particles = np.hstack((particlesPos, particlesVelocity))
#print(particles)
particles = particles.T
#print(particles)
particles = np.vstack((particles,np.arange(particleCount)))
print(particles.shape)
particleColors = np.random.randint(0,255,size=(particleCount,3))
if variableLineColor:
    particleColorsBright = np.empty((particleCount,3),dtype=np.uint8)
    for i in range(particleCount):
        increase = np.max(particleColors[i][:])
        particleColorsBright[i] = (particleColors[i][:]+255-increase)
    #print(particleColorsBright)
    particleColorsBright = particleColorsBright//2
    #print(particleColorsBright)
    particleColorAverages = np.empty((particleCount,particleCount,3),dtype=np.uint8)
    #print(particleColorAverages.nbytes)
    for i in range(particleCount):
        particleColorAverages[i] = np.add(particleColorsBright,particleColorsBright[i])

#print(particleColorsBright)
#particles = np.concatenate((particles, particlesColors), axis = -1)
if integerCord:
    particles = particles.astype("int16")

# print(particles,particleColors)

black = (0,0,0)
white = (255,255,255)
pygame.init()
#pygame.font.init()
screen = pygame.display.set_mode(screenDimension)
if transparent:
    surface = pygame.Surface(screenDimension, pygame.SRCALPHA)
else:
    surface = screen
screen.fill(black)
#pixAr = pygame.PixelArray(screen)
clock = pygame.time.Clock()
#myfont = pygame.font.SysFont('Comic Sans MS', 30)
#def inRange(x):
r = np.arange(particleCount)
if verbose:
    count = 0
    it = -10

def line(a,b):
    #print(a.shape,b.shape,b)
    b = b.T
    for i in b:
        #i.shape = 5
        #print(a[4],i[0:2])
        pygame.draw.line(screen,particleColorAverages[int(a[4])][int(i[4])],(int(a[0]),int(a[1])),(int(i[0]),int(i[1])),lineSize)
    #pygame.draw.line(screen,particleColorAverages[a[4]][b[4]],a[0:2],b[0:2],lineSize)
def calculate(x):
    if int(x[0]) < 0 or int(x[1]) < 0 or int(x[0]) > screenDimension[0]-1 or int(x[1]) > screenDimension[1]-1:
        if not reflect:
            tmp = random.choice([(0,random.random()*(screenDimension[1]-2)+1),
            (screenDimension[0]-1,random.random()*(screenDimension[1]-2)+1),
            (random.random()*(screenDimension[0]-2)+1,0),
            (random.random()*(screenDimension[0]-2)+1,screenDimension[1]-1)])
            x[0] = tmp[0]
            x[1] = tmp[1]

        if x[0] <= 0:
            x[2] = abs(x[2])
            x[0]  = 0
        elif x[0]  >= screenDimension[0]-1:
            x[2] = -abs(x[2])
            x[0]  = screenDimension[0]-1
        if x[1]  <= 0:
            x[3] = abs(x[3])
            x[1] = 0
        elif x[1] >= screenDimension[1]-1:
            x[3] = -abs(x[3])
            x[1] = screenDimension[1]-1
    return x
calculateV = np.vectorize(calculate)

#inRange = lambda x: np.intersect1d([sortX[x[0]:x[1]],sortY[x[2]:x[3]]])

# def inRange(x):
#     print(np.intersect1d(np.array(sortX[x[0]:x[1]]),np.array(sortY[x[2]:x[3]])))
#     return np.intersect1d(np.array(sortX[x[0]:x[1]]),np.array(sortY[x[2]:x[3]]))
# vInRange = np.vectorize(inRange)
print(particles)
while True:
    start = time.time()
    ind = np.lexsort((particles[:,3],particles[:,2]))
    ts = treeset
    for i in ind:
        ts[paricles[i,2]] = paricles[i,3];


    surface.fill((0,0,0,255))
    screen.fill(black)

    sortedX = np.sort(particles[0])
    sortedY = np.sort(particles[1])
    sortX = np.argsort(particles[0])
    sortY = np.argsort(particles[1])

    neighbors = np.array([(np.searchsorted(sortedX,(i[0]-lineDist)),np.searchsorted(sortedX,i[0]+lineDist),np.searchsorted(sortedY,i[1]-lineDist),np.searchsorted(sortedY,i[1]+lineDist)) for i in particles.T],dtype=np.int16)


    neighbors = np.array([np.intersect1d(sortX[x[0]:x[1]],sortY[x[2]:x[3]]) for x in neighbors])
    #neighbors = np.array([np.intersect1d(sortX[a:b],sortY[c:d]) for a,b,c,d in neighbors])


    #neighbors = np.array([ (i,j) for j in neighbors[i] for i,v in enumerate(neighbors) if j>i])
    # print({array.tostring(): array for array in neighbors}.values())
    # neighbors = np.array({array.tostring(): array for array in neighbors}.values())


    #print(neighbors)
    #neighbors = vInRange(neighbors.T)
    #new = np.apply_along_axis(inRange,1,neighbors)

    #print(neighbors.shape)
    #print(neighbors.shape)
    #neighbors = np.array(neighbors,dtype=np.int16)

    #neighbors = neighbors.astype("int16")
    #print(neighbors)

    # [line(particles[:,i],particles[:,v]) for i,v in enumerate(neighbors)]
    # print(neighbors)

    particles[0] = np.add(particles[0],particles[2])
    particles[1] = np.add(particles[1],particles[3])

    #print(particles)
    # calculate(particles.T)
    #print(particles)
    #particles = calculate(particles.T)
    #print(particles)
    particles = np.apply_along_axis(calculate,1,particles.T).T


    for i in range(particleCount):
        # if not screenFill:
        #     if integerCord:
        #         pixAr[particles[i,0]][particles[i,1]] = black
        #     else:
        #         pixAr[int(particles[i,0])][int(particles[i,1])] = black

        # particles[0][i]+=particles[2][i]
        # particles[1][i]+=particles[3][i]


        # if int(particles[0][i]) < 0 or int(particles[1][i]) < 0 or int(particles[0][i]) > screenDimension[0]-1 or int(particles[1][i]) > screenDimension[1]-1:
        #     if not reflect:
        #         tmp = random.choice([(0,random.random()*(screenDimension[1]-2)+1),
        #         (screenDimension[0]-1,random.random()*(screenDimension[1]-2)+1),
        #         (random.random()*(screenDimension[0]-2)+1,0),
        #         (random.random()*(screenDimension[0]-2)+1,screenDimension[1]-1)])
        #         particles[0][i] = tmp[0]
        #         particles[1][i] = tmp[1]
        #
        #     if particles[0][i] <= 0:
        #         particles[2][i] = abs(particles[2][i])
        #         particles[0][i] = 0
        #     elif particles[0][i] >= screenDimension[0]-1:
        #         particles[2][i] = -abs(particles[2][i])
        #         particles[0][i] = screenDimension[0]-1
        #     if particles[1][i] <= 0:
        #         particles[3][i] = abs(particles[3][i])
        #         particles[1][i] = 0
        #     elif particles[1][i] >= screenDimension[1]-1:
        #         particles[3][i] = -abs(particles[3][i])
        #         particles[1][i] = screenDimension[1]-1


        #print(particles[i][0],particles[i][1])
        #print(list(particleColors[i]))
        #pixAr[int(particles[i][0])][int(particles[i][1])] = (particleColors[i][0],particleColors[i][1],particleColors[i][2])
        if lineDist > 0:
            for j in neighbors[i]:
                if j<=i:
                    continue
                #print(particles[0][i])5
                # if neighbors[i][j] == i:
                #     continue
                if variableLineColor:
                    color = particleColorAverages[i][j]
                else:
                    color = staticColor
                    #print([*particleColorAverages[i][neighbors[i][j]],alpha])
                if lineSize == 0:
                    if dynamicLineBrightness:
                        # dist = abs(particles[0][i]-particles[0][j])+abs(particles[1][i]-particles[1][j])
                        # percentage = min(1.0,1-(dist/lineDist))
                        #does not work because points within "radius" are calculated(with the sorting method) differently from this abs method
                        #print(dist)
                        # dist = (particles[0][i]-particles[0][j])**2+(particles[1][i]-particles[1][j])**2
                        # percentage = min(1.0,1-(dist/lineDist**2))
                        dist = abs(particles[0][i]-particles[0][j])+abs(particles[1][i]-particles[1][j])


                        if dist < lineDist and dist > 0 : #*(2**1/2)
                            percentage = min(1.0,1-(dist/(lineDist)))
                        elif dist < 0:
                            percentage = 0
                            #print(1-(dist/(lineDist)))
                        else:
                            percentage = 1
                            #print(1-(dist/(lineDist)))
                        if transparent:
                            pygame.draw.aaline(surface,[*color,255*percentage],(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])))
                        else:
                            pygame.draw.aaline(surface,color*percentage,(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])))
                    else:
                        pygame.draw.aaline(surface,color,(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])))
                else:
                    if dynamicLineBrightness:
                        dist = abs(particles[0][i]-particles[0][j])+abs(particles[1][i]-particles[1][j])
                        percentage = 1
                        if dist < lineDist and dist > 0 :
                            percentage = min(1.0,1-(dist/lineDist))
                        if transparent:
                            #print([*color,255*percentage])
                            pygame.draw.line(surface,[*color,255*percentage],(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])),lineSize)
                        else:
                            pygame.draw.line(surface,color*percentage,(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])),lineSize)
                    else:
                        pygame.draw.line(surface,color,(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])),lineSize)




                if transparent:
                    screen.blit(surface,(0,0))
                    surface.fill((0,0,0,0))
                    #surface = pygame.Surface(screenDimension, pygame.SRCALPHA)


            # for j in range(particleCount):
            #     dist = abs(particles[0][i]-particles[0][j])+abs(particles[1][i]-particles[1][j])
            #     if dist < lineDist and dist > 0:
            #         pygame.draw.line(surface,particleColorAverages[i][j]*min(1.0,1-(dist/lineDist)),(int(particles[0][i]),int(particles[1][i])),(int(particles[0][j]),int(particles[1][j])),lineSize)




            # for j in range(len(particles)):
            #     if i == j:
            #         continue
            #     dist = abs(particles[0][i]-particles[0][j])+abs(particles[1][i]-particles[1][j])
            #     #dist = math.hypot(particles[i][0]-particles[j][0], particles[i][1]-particles[j][1])
            #     if dist < lineDist and dist > 0:
            #         #print(val)
            #         #avgColor = (np.add(particleColorsBright[i],particleColorsBright[j])//2)*val
            #         if variableLineColor and dynamicLineBrightness:
            #             color = particleColorAverages[i,j]*min(1.0,1-(dist/lineDist))
            #         elif variableLineColor:
            #             color = particleColorAverages[i,j]
            #         elif dynamicLineBrightness:
            #             color = staticColor*min((1.0,1-(dist/lineDist)))
            #         else:
            #             color = staticColor
            #         #print(avgColor/val)
            #         #val = int(val*255)
            #         #avgColor = (val,val,val)
            #         if lineSize == 1:
            #             pygame.draw.aaline(screen,color,(particles[0:2][i]),(particles[0][j],particles[1][j]))
            #         else:
            #             pygame.draw.line(screen,color,(particles[0:2][i]),(particles[0][j],particles[1][j]),lineSize)

        if integerCord:
            pygame.draw.rect(surface,particleColors[:][i],(particles[0][i]-partilceSizeH,particles[1][i]-partilceSizeH,partilceSize,partilceSize))
        else:
            pygame.draw.rect(surface,(*particleColors[:][i],120),(int(particles[0][i]-partilceSizeH),int(particles[1][i]-partilceSizeH),partilceSize,partilceSize))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    #textsurface = myfont.render("FPS: "+str(1/(time.time()-start)), False, (0, 0, 0))
    # print(textsurface)
    # screen.blit(textsurface,(0,0))
    pygame.display.update()
    clock.tick(tickRate)

    if verbose:
        tmp = time.time()-start
        if tmp > 0:
            print(1/tmp)
        # it+=1
        # if it > 0:
        #     tmp = time.time()-start
        #     if tmp > 0:
        #         #print(1/tmp)
        #         count+= 1/tmp
        #         print(count/it)
        #     else:
        #         print("FPS TO HIGH TO COUNT")
        #         it-=1

    # print(time.time()-start)
    # if time.time()-start != 0:
    #     print("FPS: ",(1/(time.time()-start)))



# root = tk.Tk()
# #root.title = "ParticleSystem"
# canvas = tk.Canvas(root,width = screenDimension[0],height = screenDimension[1],bg="black")
# canvas.grid(row=0,column=0)
# while True:
#     #root.mainloop()
#     start = time.time()
#     for i in range(len(particles)):
#             canvas.create_line(int(particles[i][0]),int(particles[i][1]),int(particles[i][0])+1,int(particles[i][1])+1,fill="black")
#             #print(particles[i])
#             particles[i][0]+=particles[i][2]
#             particles[i][1]+=particles[i][3]
#             if int(particles[i][0]) < 0 or int(particles[i][1]) < 0 or int(particles[i][0]) > screenDimension[0]-1 or int(particles[i][1]) > screenDimension[1]-1:
#                 tmp = random.choice([(0,random.random()*(screenDimension[1]-2)+1),(screenDimension[0]-1,random.random()*(screenDimension[1]-2)+1),(random.random()*(screenDimension[0]-2)+1,0),(random.random()*(screenDimension[0]-2)+1,screenDimension[1]-1)])
#                 #tmp = (0,random.random()*(screenDimension[1]-2)+1)
#                 if random.randint(0,1):
#                     particles[i][2]*=-1
#                 if random.randint(0,1):
#                     particles[i][3]*=-1
#                 particles[i][0] = tmp[0]
#                 particles[i][1] = tmp[1]
#             #print(particles[i][0],particles[i][1])
#             #print(list(particleColors[i]))
#             canvas.create_line(int(particles[i][0]),int(particles[i][1]),int(particles[i][0])+1,int(particles[i][1])+1,fill="white")
#             #(particleColors[i][0],particleColors[i][1],particleColors[i][2])
#             canvas.update()
#     if time.time()-start != 0:
#         print("FPS: ",(1/(time.time()-start)))
