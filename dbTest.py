from replit import db



def getLeaderBored():
  bits = [] # Declare a empty array
  for user in db.keys():
    include = int(db[user])
    bits.append(include) # Add the amount of bits to the array
  bits.sort() # sort it
  rem = bits[::-1] # reverse list
  return [rem[0], rem[1], rem[2]] # give back
