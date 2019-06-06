# This is the PyPoll main program - HW#3 
# Author: Murali Calambur 
# Rutgers Data Science Bootcamp

# Import the os module
import os

# Module for reading CSV files
import csv

#Navigate to the Resources folder in RUTSOM201905DATA2 to open the CSV file
csvpath = os.path.join(os.path.expanduser('~'),'Desktop', 'GIT_WS', 'python-challenge', 'PyPoll','Resources','election_data.csv')

#Initialize variables 
totalVotes = 0
candVotes = 0
candidate = set()
voteCount =[]
voteCandidate = []
winBool = False
Tally = []
WinnerPct = {}
WinnerCnt = {}
w = 0

#Header 
firstRow = "Election Results" + "\n" +  "-----------------------------------"

# Specify the file to write to
output_path = os.path.join(os.path.expanduser('~'),'Desktop', 'GIT_WS', 'python-challenge', 'PyPoll','Resources', 'poll_output.txt')

#If the file exists already, delete it
if os.path.exists(output_path):
    os.remove(output_path)

# Open the file using "append" mode
output_file = open(output_path, 'a+')
output_file.writelines(firstRow + "\n")
print(firstRow)

# Start reading the CSV file
with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)
    
# Read each row of data after the header (skip the header)
# Add the total votes and inset into a set (get unique candidate names -- avoid hard coding)
# Add each row, add the candidate names in an array 
    for row in csvreader:  
        totalVotes += 1
        candidate.add(row[2])
        voteCandidate.append(row[2])

print("Total Votes: " + str(totalVotes) + "\n" + "-----------------------------------" )
output_file.writelines("Total Votes: " + str(totalVotes) + "\n" + "-----------------------------------" + "\n")

#Iterate through the candidate set and get their respective vote counts 
for j in range(len(candidate)):
    candName = list(candidate)[j]
    for n in range(len(voteCandidate)):
        if voteCandidate[n] == candName:
            candVotes +=1
    #get the rounded percentage        
    pct = round(100*(candVotes/totalVotes))
    #Tally is an array of winning percentages 
    Tally.append(pct)
    #Create two dicts - hold candidate name & winning pct + candidate name & vote tally
    WinnerPct[candName] = pct
    WinnerCnt[candName] = candVotes
    candVotes =0

# find the highest tally this is the winner that goes in the final line 
w = max(Tally)
absWinner = list(WinnerPct.keys())[list(WinnerPct.values()).index(w)]
absWinPct = WinnerPct[absWinner]
absWinCnt = WinnerCnt[absWinner]

# Print the Winner line in the appropriate format 
print(absWinner + ": " + "%.3f%%" % (absWinPct)   + " (" + str(absWinCnt) + ")")
output_file.writelines(absWinner + ": " + "%.3f%%" % (absWinPct)   + " (" + str(absWinCnt) + ")" +"\n")

# Remove the highest and loop through the rest [this is to sort the votes in the decreasing order]
Tally.remove(w)

# Now simply iterate through, print the next winner, remove it from Tally[] 
for n in range(len(Tally)):
    w = max(Tally)
    nextWinner = list(WinnerPct.keys())[list(WinnerPct.values()).index(w)]
    nextWinPct = WinnerPct[nextWinner]
    nextWinCnt = WinnerCnt[nextWinner]
    print(nextWinner + ": " + "%.3f%%" % (nextWinPct)   + " (" + str(nextWinCnt) + ")")
    output_file.writelines(nextWinner + ": " + "%.3f%%" % (nextWinPct)   + " (" + str(nextWinCnt) + ")" + "\n")
    Tally.remove(w)


# Print the final winner 
print("-----------------------------------" + "\n" + "Winner: " + absWinner + "\n" + "-----------------------------------")
output_file.writelines("-----------------------------------" + "\n" + "Winner: " + absWinner + "\n" + "-----------------------------------")

output_file.close()