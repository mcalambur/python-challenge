# This is the PyBank main program 
# Author: Murali Calambur 
# Rutgers Data Science Bootcamp

# Import the os module
import os

# Module for reading CSV files
import csv

# Printing currency
import locale 

# US Currency
locale.setlocale( locale.LC_ALL, '' )

#Navigate to the Resources folder in RUTSOM201905DATA2 to open the CSV file
csvpath = os.path.join(os.path.expanduser('~'),'Desktop', 'GIT_WS', 'RUTSOM201905DATA2', 'Homework', '03-Python', 'PyBank','Resources','budget_data.csv')

#Initialize Total Months 
totalMonths = 0
totalAmount = 0
budgetDate = []
profLoss = []
avgLoss = 0
monthlyChange = 0
monthlyChangeArray= []
sumChange = 0

print("Financial Analysis" + "\n" +  "-----------------------------------" )

with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)
    
# Read each row of data after the header (skip the header)
    for row in csvreader:  
        totalMonths += 1
        totalAmount += int(row[1])
        budgetDate.append(row[0])
        profLoss.append(int(row[1]))
    
    
print(f"Total Months:  {totalMonths}")
print("Total: " + locale.currency(totalAmount, grouping=True))

for i in range(len(profLoss) - 1):
    monthlyChange = profLoss[i+1] - profLoss[i]
    sumChange += monthlyChange
    monthlyChangeArray.append(monthlyChange)


avgLoss = sumChange/(len(profLoss) - 1)
print("Average Loss: " + locale.currency(avgLoss, grouping=True))

x = max(monthlyChangeArray)
q = min(monthlyChangeArray)

print("x: " + str(x)  + " and q = " + str(q))