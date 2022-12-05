import random 
import time
import csv
import os.path
import pandas as pd


## Table Setup
def tabSetUp():
  with open('choices.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
      ["pl_choices", "prob_rock", "prob_paper", "prob_scissors", "prob_total"])

  rps = ["r", "p", "s"]
  for x in rps:
    for y in rps:
      for z in rps:
        with open('choices.csv', 'a', encoding='UTF8', newline='') as f:
          writer = csv.writer(f)
          writer.writerow([x + "-" + y + "-" + z, 0, 0, 0, 0])

# def indOf(x: int, y: int, z: int):
#   return (9 * x) + (3 * y) + z
def indOf():
  return (9 * lastHPlays[0]) + (3 * lastHPlays[1]) + lastHPlays[2]
  
## Game Setup / Functions
gAr = ['r', 'p', 's']
lastHPlays = []

def rpsN(huCh, caMo):
  ## caMo: 0-Rand, 1-Most Likely Play, 2-Weighted Rand, 3-Cheats
  
  ## Set table
  # Set last 4 plays
  if len(lastHPlays) == 4:
      lastHPlays.pop(0)
  lastHPlays.append(huCh)
  # Put into table
  if len(lastHPlays) == 4:
    df.iloc[indOf(),(huCh + 1)] += 1
    df.iloc[indOf(),4] += 1
  df.to_csv('choices.csv', mode='w', index=False)
  
  ## Set car choice
  caCh = random.randint(0,2)
  if caMo == 1 and len(lastHPlays) == 4:
    # Most likely
    lis = [df.iat[indOf(),1],df.iat[indOf(),2],df.iat[indOf(),3]]
    caCh = (lis.index(max(lis)) + 1) % 3
  elif caMo == 2 and len(lastHPlays) == 4:
    # Weighted random
    lis = random.choices(gAr, weights = [df.iat[indOf(),1], df.iat[indOf(),2], df.iat[indOf(),3]], k = 1)
    caCh = (gAr.index(lis[0]) + 1) % 3
  elif caMo == 3:
    caCh = (huCh + 1) % 3
    
    ## Game stuff
  print("---\nHuman played [" + gAr[huCh] + "] and Car played [" + gAr[caCh] + "]")
  if huCh == caCh:
    print("Tie!")
    return [0,0]
  elif huCh == ((caCh + 1) % 3):
    print("Human Won!")
    return [1,0]
  else:
    print("Car Won!")
    return [0,1]

      
## Gameplay Loop
if not (os.path.exists("choices.csv")):
  tabSetUp()
df = pd.read_table('choices.csv', delimiter=",")

while True:
    inp = input("Do you choose rock(r), paper(p) or scissors(s)?\nInput \"stop\" to stop\n").strip()
    if inp.find("stop") != -1:
        break
      
    if len(inp) > 1:
      print("= = = Invalid = = =")
      continue
    else:
      i = rpsN(gAr.index(inp), 1)

    time.sleep(0.75)
    print("= = = = = = = =")
