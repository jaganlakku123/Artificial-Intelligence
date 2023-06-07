#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Durga Sai Sailesh Chodabattula (dchodaba), Manideep Varma Penumatsa (mpenumat), and Lakku Sai Jagan (slakku)
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time

import random
import math
def costFn(input, teamList):
        
        cost = 0
        
        #teams
        for i in range(0,len(teamList)):cost += 5

        #unwanted cases
        for l in input:
            check = l.split(" ")[0]
            not_list = l.split(" ")[-1].split(",")
            for t in teamList:
                t = t.split("-")
                if check in t:
                    for user in not_list:
                        if user in t:cost += 10
                    break

        #redunduncy check condition
        for l in input:
            check = l.split(" ")[0]
            yes_list = l.split(" ")[1].split("-")
            for t in teamList:
                t = t.split("-")
                if check in t:
                    teamChk = t
                    break
            for user in yes_list:
                if user != 'xxx':
                    if user not in teamChk:cost += 3


        #Wrong group assignment
        for l in input:
            check = l.split(" ")[0]
            for t in teamList:
                t = t.split("-")
                if check in t:
                    teamChk = t
                    if len(teamChk) != len(l.split(" ")[1].split("-")):
                        cost += 2
                        break        
        return cost

def genFn(userList):
        team = []
        while userList:
            teamSize = min(len(userList),random.randint(1,3))
            pop_list = random.sample(userList, teamSize)
            team.append("-".join(pop_list))
            userList = list(set(userList)-set(pop_list))
        return team

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    # Input File
    with open(input_file,'r') as f:lines = [line.rstrip() for line in f]
        
    #userList
    userList = []
    for l in lines:userList.append(l.split(" ")[0])
    
    min_c = math.inf
    minTeamCost = []
    for i in range(0,202110):
        team = genFn(userList)
        temp = costFn(lines,team)
        if temp < min_c:
            min_c = temp
            minTeamCost = team
    
    res = {"assigned-groups": minTeamCost,
               "total-cost" : min_c}
    yield(res)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))
    
    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])