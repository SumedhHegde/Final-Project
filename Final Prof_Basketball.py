import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

class BasketBallMC():

    def __init__(self):
        self.colors = [(31, 119, 180), (174, 199, 232), (255, 127,  14),
           (255, 187, 120), (44, 160, 44), (214,  39,  40), (148,103,189),
           (152, 223, 138), (255,152,150), (197, 176, 213), (140, 86, 75),
           (196, 156, 148), (227,119,194), (247, 182, 210), (127,127,127),
           (199, 199, 199),(188,189, 34),(219, 219, 141), (23, 190,207),
           (158, 218, 229),(217,217,217)]

        # Scale RGB values to the [0, 1] range, format matplotlib accepts.
        for i in range(len(self.colors)):
          r, g, b = self.colors[i]
          self.colors[i] = (r / 255., g / 255., b / 255.)

    def attemptThree(self):
      if np.random.randint(0, high=100) < self.threePtPercent:
        if np.random.randint(0, high=100) < self.overtimePercent:
          return True #We won!!
      return False #We either missed the 3 or lost in OT

    def attemptTwo(self):
      havePossession = True
      pointsDown = 3
      timeLeft = 30
      while (timeLeft > 0):
        #What to do if we have possession
        if (havePossession):
          #If we are down by 3 or more, we take the
          #2 quickly.  If we are down by 2 or less
          #We run down the clock first
          if (pointsDown >= 3):
            timeLeft -= self.timeToShoot2
          else:
            timeLeft = 0

          #Do we make the shot?
          if (np.random.randint(0, high=100) < self.twoPtPercent):
            pointsDown -= 2
            havePossession = False
        else:
          #Does the opponent team rebound?
          #If so, we lose possession.
          #This doesn't really matter when we run
          #the clock down
          if (np.random.randint(0, high=100) >= self.offenseReboundPercent):
            havePossession = False
          else:   #cases where we don't have possession
            if (pointsDown > 0):  #foul to get back possession

              #takes time to foul
              timeLeft -= self.timeToFoul

              #opponent takes 2 free throws
              if (np.random.randint(0, high=100) < random.choice(self.oppFtPercent)):
                pointsDown += 1

              if (np.random.randint(0, high=100) < random.choice(self.oppFtPercent)):
                pointsDown += 1
                havePossession = True
            else:
              if (np.random.randint(0, high=100) >= self.ftReboundPercent):
                #you were able to rebound the missed ft
                havePossession = True
              else:
                #tied or up so don't want to foul;
                #assume opponent to run out clock and take
                if (np.random.randint(0, high=100) < random.choice(self.oppTwoPtPercent)):
                  pointsDown += 2 #They made the 2
                timeLeft = 0


      if (pointsDown > 0):
        return False
      else:
        if (pointsDown < 0):
          return True
        else:
          if (np.random.randint(0, high=100) < self.overtimePercent):
            return True
          else:
            return False

    def main(self):
        data = pd.read_csv(r'C:\Users\hegde\Documents\Final-Project\Basketball.csv')
        plt.figure(figsize=(14,14))
        names=['Lebron James', 'Kyrie Irving', 'Steph Curry', 'Kyle Krover', 'Dirk Nowitzki']
        threePercents = [35.4,46.8,44.3,49.2, 38.0]
        twoPercents = [53.6,49.1,52.8, 47.0,48.6]
        oppNames = data['Name'].values.tolist()
        oppTwoPercentList = data['twoPercent'].values.tolist()
        colind=0
        #offrebound = data['Off_Rebound'].values.tolist()
        oppFtPercentList = data['FT%'].values.tolist()
        for i in range(5):  # can be run individually as well
          x=[]
          y1=[]
          y2=[]
          trials = 800 #Number of trials to run for simulation
          self.threePtPercent = threePercents[i] # % chance of making 3-pt shot
          self.twoPtPercent = twoPercents[i] # % chance of making a 2-pt shot
          self.oppTwoPtPercent = oppTwoPercentList #40 #Opponent % chance making 2-pter
          self.oppFtPercent = oppFtPercentList #Opponent's FT %
          self.timeToShoot2 = 5 #How many seconds elapse to shoot a 2
          self.timeToFoul = 5 #How many seconds elapse to foul opponent
          self.offenseReboundPercent = 25 #% of regular offense rebound
          self.ftReboundPercent = 15 #% of offense rebound after missed FT
          self.overtimePercent = 50 #% chance of winning in overtime

          winsTakingThree = 0
          lossTakingThree = 0
          winsTakingTwo = 0
          lossTakingTwo = 0
          curTrial = 1

          while curTrial < trials:
            #run a trial take the 3
            if (self.attemptThree()):
              winsTakingThree += 1
            else:
              lossTakingThree += 1
              #run a trial taking a 2
              if self.attemptTwo() == True :
                winsTakingTwo += 1
              else:
                lossTakingTwo += 1

              x.append(curTrial)
              if curTrial == 300:
                  var = 12
              y1.append(winsTakingThree)
              y2.append(winsTakingTwo)
              curTrial += 1


          plt.plot(x,y1, color=self.colors[colind], label=names[i]+" Wins Taking Three Point: " + str((winsTakingThree/trials)*100) + '%', linewidth=2)
          plt.plot(x,y2, color=self.colors[20], label=names[i]+" Wins Taking Two Point: " + str((winsTakingTwo/trials)*100) + '%', linewidth=1.2)
          colind += 2

        legend = plt.legend(loc='upper left', shadow=True,)
        for legobj in legend.legendHandles:
            legobj.set_linewidth(2.6)
        plt.show()

if __name__ == "__main__":
    mainobj = BasketBallMC()
    mainobj.main()
