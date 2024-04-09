import sys
from hashSet import HashSet

def getColumn(matrix, colIndex):
  col = []
  for rowIndex in range(9):
    col.append(matrix[rowIndex][colIndex])
    
  return col

def getSquare(matrix, rowIndex, colIndex):
  square = []
  for i in range(rowIndex, rowIndex+3): 
    for j in range(colIndex,colIndex+3):
        square.append(matrix[i][j])
        
  return square

def getGroups(matrix):
  groups = []
  # get rows
  for i in range(9):
    groups.append(list(matrix[i]))
  # get columns
  for i in range(9):
    groups.append(getColumn(matrix,i))
  # get squares
  # squares are processed left-right, up-down
  for i in range(0,9,3): 
    for j in range(0,9,3):
      groups.append(getSquare(matrix,i,j))     

  return groups

def cardinality(x):
  return len(x)


def rule1(group):
  ### IMPLEMENT THIS FUNCTION ###

  changed = False
  
  # RULE 1 - You have to look for duplicate sets (i.e. set([1,6])). If you 
  # have same number of duplicate sets in a group (row, column, square) as 
  # the cardinality of the duplicate set size, then they must each get one 
  # value from the duplicate set. In this case the values of the duplicate 
  # set may be removed from all the other sets in the group. 

  # used calrification on rules template: chatGPT("clarify these rules <rules from pdf/template>")
  # loop through the current looking group for each set/cell in the group
  for set in group:
    dupCount = 0 # a duplicate set counter. Keeps track of how many times a set is duplicated in a group
    # loop through the group again to check the orginal/dup/selected set with the other sets for duplicates
    for otherSet in group:
      # Check if the selected set/dup set is duplicated in the group and add to the counter.
      if set.issuperset(otherSet):
        dupCount += 1

    # check cardinality of the dup set
    card = cardinality(set)

    # check if cardinality of the dup set is the same as the amount of times it is duplicated
    if card == dupCount:
      # if above check is true loop through the sets in the group
      for otherSet in group:
        # for each set in group check if the dup set is not a duplicate (this makes sure that you don't delete elements from dup sets)
        if (set.issuperset(otherSet)) == False:
          # remove the items of the dup set from these non duplicate sets
          otherSet.difference_update(set)
          changed = True # sets were changed

    # # used idea from: copilot("Said that there was a mistake in logic for if a cell was solved in Rule 1 causing an infinite loop")
    # This is a check to see if the set is solved/puzzle is solved at this step
    card = cardinality(set)
    if card == 1:
      changed = False # no changes were made as this is a check for solved anyways

  return changed
  
def rule2(group):
  ### IMPLEMENT THIS FUNCTION ###

  changed = False
  # RULE 2 - Reduce set size by throwing away elements that appear in other
  # sets in the group
  # used calrification on rules template: chatGPT("clarify these rules <rules from pdf/template>")

  # loop through the group to select a set/cell
  for set in group:
    # Create a placeholder set for future case checks and tracebacks
    placeholder = HashSet()
    placeholder.update(set)
    
    # loop through the group again to get a second set
    for otherSet in group:
      # loop through this chosen set for the items inside
      for item in otherSet:
        # if the current item is in the first selected set then remove it from the first selected set
        if item in set:
          set.remove(item)
          changed = True # Changes were made

    # find the cardinality of the selected set
    card = cardinality(set)
    # Using the cardinality of the selected set check different cases for if the cell is solved
    if card == 1: # if cell is solved then break from rule 2 as a cell has been solved
      break
    elif card == 0: # if a cell has been emptied then use the placeholder to traceback to original set
      set.update(placeholder)
      changed = False # changes were reversed therefore not made
    else: # if the set is not solved then continue to next cell/set 
      continue 

  return changed

def reduceGroup(group):
  changed = False 
  # this sorts the sets from smallest to largest based cardinality
  # all commented out coude lines were test lines to watch/check the rules being implemented
  group.sort(key=cardinality)
  #print("Base")
  #test(group)
  #print()
  changed = rule2(group)
  #print("Rule 2")
  #test(group)
  #print()
  changed = rule1(group)
  #print("Rule 1")
  #test(group)
  #print()
  
  return changed

def reduceGroups(groups):
  changed = False
  for group in groups:
    if reduceGroup(group):
      changed = True
      
  return changed

def reduce(matrix):
    changed = True
    groups = getGroups(matrix)
    
    while changed:
        changed = reduceGroups(groups)

def printMatrix(matrix):
  for i in range(9):
    for j in range(9):
      if len(matrix[i][j]) != 1:
        sys.stdout.write("x ")
      else:
        for k in matrix[i][j]:
          sys.stdout.write(str(k) + " ")

    sys.stdout.write("\n")

# A self created function to test/find the results of the set after changes (used in the spot where rules were called)
# def test(group):
  # print()
  # for elem in group:
    # set = []
    # for val in elem:
      # set.append(val)
    # print()
    # print(set)

def main():
  file = open(sys.argv[1], "r")
  matrix = []

  for line in file:
    lst = line.split()
    row = []

    for val in lst:
      if val == 'x':
        s = HashSet(range(1,10))
      else:
        s = HashSet([eval(val)])
      row.append(s)

    matrix.append(row)

  print("Solving this puzzle:")
  printMatrix(matrix)

  reduce(matrix)  

  print()
  print("Solution:")
  printMatrix(matrix)

# chatGPT was used to check the giving test puzzle to the final solution puzzle 
# to make sure the algorithms worked and gave correct solution
main()
