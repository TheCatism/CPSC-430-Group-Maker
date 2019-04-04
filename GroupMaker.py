# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 09:26:05 2019
@author: phimm_000
"""

#Group Maker
#Anthony Phimmasone
#Denzel Saraka
#Igor Asipenka
#James Donahue

import os
import random
import math
import csv
import datetime
import pandas as pd

def ansToBool(answer):
    if(answer == "Y" or answer == "y"):
        return True

    else:
        return False

#Ask the user to enter in a CSV filename
#filename = input("Enter a filename (include the .csv): ")
#User can enter in a filename with or without the .csv
print("Enter in a filename with or with the .csv")
filename = input("Enter a filename: ")
#If a filename is not shorter than 5 character and does not end with .csv
#Then concatenate the .csv to the end of the filename
if len(filename) < 5 or not filename.strip().endswith(".csv"):
    filename = filename + ".csv"
print(filename)

#While the file does not exist
#Ask the user to re-enter filename
#The path of the file
while not os.path.exists('./' + filename):
    print("File does not exist or incorrect spelling")
    filename = input("Enter a filename (include the .csv): ")

#total csv file
totalDF = pd.read_csv(filename)

print(totalDF)
'''
students = []
with open(filename, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        students.append(row)
'''
#copy first header row to headers list
headers = list(totalDF.columns.values)
#totalDF.drop(totalDF.index[0])

#print("headers\n")
#print(headers)

#shuffle rows
randStudents= totalDF.sample(frac=1)
#print("Student List:\n")
#print(randStudents)

#create list of names
nameList = randStudents['Name'].values

#TODO: Check if file has extra headers
                       
#Get all the information in the column based on the Header name
#for i in range(3, len (headers))
categoryOne = headers[2]
categoryTwo = headers[3]
categoryThree = headers[4]
#print(categoryOne)
#print(categoryTwo)
#print(categoryThree)

#Creates lists for each row and puts it into a list (AKA lists of lists)
#listOflists = df.values.tolist()

print("\n\n\n")


#TODO: Check if the number of students in each group is maximum (exceeds number in CSV file)
#Or if the user only wants one group then ignore options and export random list
#Check if user types zero groups

numStud = " "
numGroup = " "
groupInput = " "
while(1):
    groupInput = input("How would you like to have your groups created?\nBy number of students per group[N]?:\nOr\nBy how many groups will be made[G]:\n")
    if(groupInput == "G" or groupInput == "N"):
        break

#Check if students in group is excedes maximum

if(groupInput == "N"):
    while True:
        numStud = input("How many students per group?")
        #If the input entered is not a number or is longer than the amount of students
        #Then it is invalid
        if not numStud.isdigit() or int(numStud) > len(nameList):
            print("Invalid Input!")
        else:
            numStud = int(numStud)
            break
    
#if number of groups is zero print invalid
#State prompt

if(groupInput == "G"):
    while True:
        numGroup = input("How many groups will be made?")
        #numStud = int(math.floor(len(nameList) / int(numGroup)))
        if not numGroup.isdigit() or int(numGroup) == 0:
            print("Invalid Input!")
        else:
            numGroup = int(numGroup)
            numStud = int(math.floor(len(nameList) / numGroup))
            break


#Menu:
blackBool = False
#random bool
randBool = ansToBool(input("Would you like the groups to be completely randomized? [Y/N]: "))

if(randBool):
    #creating totally randomized groups
    result = []
    remainder = len(nameList) % int(numStud)
    if not remainder == 0:
        print("Groups may have extra students")
    i = -1
    for j in range(len(nameList) - remainder):
        #creates a list
        if j % int(numStud) == 0:
            i = i + 1
            result.append([i])
        result[i].append(nameList[j])
    leftOver = nameList[len(nameList) - remainder:]
    for i in range(len(leftOver)):
        result[i].append(leftOver[i])


#if the user wants options
if(not randBool):
    #blacklist bool
    blackBool = ansToBool(input("Would you like to use the blacklist? [Y/N]: "))

#user selected blacklist option
if(blackBool):
    #creating groups based on blacklist
    result = []
    remainder = len(nameList) % int(numStud)
    if not remainder == 0:
        print("Groups may have extra students")

    i = -1
    for j in range(len(nameList) - remainder):
        if j % int(numStud) == 0:
            i = i + 1
            result.append([])
        result[i].append(nameList[j])

    leftOver = nameList[len(nameList) - remainder:]
    for i in range(len(leftOver)):
        result[i].append(leftOver[i])

    readyBool = False
    #print("Result: ",result)
    while(not readyBool):
        #check that students are not in a group with their blacklistee
        for groupnum in range(len(result)):
            group = result[groupnum]
            for studentnum in range(len(group)):
                student = group[studentnum]
                index = randStudents[randStudents['Name']==student].index.values.astype(int)[0]
                #print(index)
                blackValue = randStudents.at[index,"Blacklist"]
                #print(student ," does not want to pair with: ",blackValue)
                if(str(blackValue) == 'nan'):
                    continue
                else:
                    #check if blacklistee in students group
                    if blackValue in group:
                        nextGroup = groupnum +1
                        #check if last group
                        if(groupnum == len(result)-1):
                            nextGroup = 0
                        #move student to next group
                        result[nextGroup].append(student)
                        #print("moved: ",student," to ",nextGroup)
                        del group[studentnum]
                        #move nextGroups first student to this gorup
                        result[groupnum].append(result[nextGroup][0])
                        #print("removed: ",result[nextGroup][0])
                        del result[nextGroup][0]
                        #print("Result: ",result)
                        
        #check if groups are complete
        for groupnum in range(len(result)):
            group = result[groupnum]
            for student in group:
                index = randStudents[randStudents['Name']==student].index.values.astype(int)[0]
                blackValue = randStudents.at[index,"Blacklist"]
                if str(blackValue) not in group:
                    if(groupnum == len(result) -1):
                            readyBool = True
                            break

    #add numbers to beginning of groups
    for i in range(len(result)):    
        result[i].insert(0,i)
#print("Result: ",result)

categoryOneBool = False
categoryOneText = "Would you like to create groups based on " + categoryOne + "? [Y/N]: "
categoryOneBool = ansToBool(input(categoryOneText))
categoryTwoBool = False
categoryTwoText = "Would you like to create groups based on " + categoryTwo + "? [Y/N]: "
categoryTwoBool = ansToBool(input(categoryTwoText))
categoryThreeBool = False
categoryThreeText = "Would you like to create groups based on " + categoryThree + "? [Y/N]: "
categoryThreeBool = ansToBool(input(categoryThreeText))
print("\n\n\n")


#df = pd.DataFrame.from_records(result)
#print(df)
#Write to the CSV
#df.to_csv('GroupMakerOutput.csv')
#if client wants list to be completely randomized

for i in range(len(result)):
    print("Group", i, ": ", end = "", sep = "")
    for j in range(1, len(result[i])):
        if (not j == len(result[i]) - 1):
            print(result[i][j], ", ", sep = "", end="")
        else:
            print(result[i][j])
timestamp = datetime.datetime.now().strftime("%B-%d-%Y-%I:%M")
outputFile = "GroupMakerOutput"+timestamp+".csv"
with open(outputFile, mode='w') as output_file:
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in result:
        csv_writer.writerow(row)
print("Successfully wrote to output file!")