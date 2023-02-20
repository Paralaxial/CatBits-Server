def placeholder():
  with open("log.txt", "r+") as file:
    print(len(file.readlines()))
    print(type(file.readlines()))
    """while True:
      if file.readlines() >= 5:
        file.write() # Empties the logs I guess?"""

placeholder()