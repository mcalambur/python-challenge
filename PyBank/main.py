# This is the PyBank main program - HW#3 
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

#Initialize variables 
#Total Months and Total Amount that need to be calculated
totalMonths = 0
totalAmount = 0
# Arrays to track date and the differences per month
budgetDate = []
profLoss = []
#Track average of the changes month over month
avgChange = 0
#Monthly Change 
monthlyChange = 0
monthlyChangeArray= []
#Track sum of the changes for the mean
sumChange = 0
#Max and Min changes
maxChange = 0
minChange = 0

firstRow = "Financial Analysis" + "\n" +  "-----------------------------------"
print(firstRow)

with open(csvpath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)
    
# Read each row of data after the header (skip the header)
    for row in csvreader:  
        totalMonths += 1
        totalAmount += int(row[1])
        #Add each record in the respective arrays
        budgetDate.append(row[0])
        profLoss.append(int(row[1]))

# Specify the file to write to
output_path = os.path.join(os.path.expanduser('~'),'Desktop', 'GIT_WS', 'RUTSOM201905DATA2', 'Homework', '03-Python', 'PyBank','Resources', 'budget_output.txt')

# Open the file using "write" mode. Specify the variable to hold the contents
output_file = open(output_path, 'a+')
output_file.writelines(firstRow + "\n")

#Total Months     
print(f"Total Months:  {totalMonths}")
output_file.writelines("Total Months: " + str(totalMonths) + "\n")

#Total amount with currency formatting 
print("Total: " + locale.currency(totalAmount, grouping=True))
output_file.writelines("Total: " + locale.currency(totalAmount, grouping=True) + "\n")

# Calaculate month difference and store in an array
for i in range(len(profLoss) - 1):
    monthlyChange = profLoss[i+1] - profLoss[i]
    sumChange += monthlyChange
    monthlyChangeArray.append(monthlyChange)


# Average Change, print with currency formatting
avgChange = sumChange/(len(profLoss) - 1)
print("Average Loss: " + locale.currency(avgChange, grouping=True))
output_file.writelines("Average Loss: " + locale.currency(avgChange, grouping=True) + "\r\n")

maxChange = max(monthlyChangeArray)
minChange = min(monthlyChangeArray)

print("Greatest Increase in Profits: " + budgetDate[(monthlyChangeArray.index(maxChange)+1)] + "  " +  locale.currency(maxChange, grouping=True))
print("Greatest Decrease in Profits: " + budgetDate[(monthlyChangeArray.index(minChange)+1)] + "  " +  locale.currency(minChange, grouping=True))

output_file.writelines("Greatest Increase in Profits: " + budgetDate[(monthlyChangeArray.index(maxChange)+1)] + "  " +  locale.currency(maxChange, grouping=True) + "\n")
output_file.writelines("Greatest Decrease in Profits: " + budgetDate[(monthlyChangeArray.index(minChange)+1)] + "  " +  locale.currency(minChange, grouping=True) + "\n")

output_file.close()


