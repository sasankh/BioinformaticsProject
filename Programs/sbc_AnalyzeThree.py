# Name: Sasankh B.C.
# Class: BIOI4980 
# 
# Honor Pledge: On my honor as a student of the University
#               of Nebraska at Omaha, I have neither given nor
#               received unauthorized help on this homework
#               assignment.
# 
# NAME: Sasankh B.C.
# NUID: 52829961
# EMAIL: sbc@unomaha.edu
# 
# Partners: NONE

# The program analyzes the table organize and gives the summary based on user input criteria.
import MySQLdb
import sys
import getopt
import os, sys
import time

g1 = ""
c1 = 0
g2 = ""
c2 = 0
g3 = ""
c3 = 0
g4 = ""
c4 = 0
g5 = ""
c5 = 0
g6 = ""
c6 = 0
g7 = ""
c7 = 0
g8 = ""
c8 = 0
g9 = ""
c9 = 0
g10 = ""
c10 =0
g11 = ""
c11 = 0

def main():

# Open database connection and prepare a cursor object using cursor() method
    print "If you don't enter the right db Name and password the program will crash"
    dbUser = raw_input ("Please enter an existing MYSQLdb username: ")
    dbPass = raw_input ("Please enter the password for the username: ")
    dbName = raw_input ("Please enter the database Name: ")
    db = MySQLdb.connect("localhost", dbUser, dbPass, dbName)
    cursor1 = db.cursor()
    cursor2 = db.cursor()
    cursor3 = db.cursor()
    cursor4 = db.cursor()
    cursor5 = db.cursor()
    menuData(db, cursor4)
    data = ""
    tableName = "finalTable"
    pathOptionOne = ""
    pathOptionTwo = ""
    pathOptionOne = raw_input ("What is the first pathway?")
    choice = raw_input ("Do you want to do another option too? (y/n)")
    if (choice  == "y"):
        pathOptionTwo = raw_input ("What is the second option?")
        data = ProcessTwo(db, cursor1, cursor2, cursor3, cursor4, cursor5, pathOptionOne, pathOptionTwo, tableName)
    else:
    	data = ProcessOne(db, cursor1, cursor2, cursor3, cursor4, cursor5, pathOptionOne, tableName)
    print data
    writeIt = raw_input ("Write in file?(y/n)")
    if (writeIt == "y"):
       fileName = raw_input ("Enter file name : ")
       outFile = open(fileName, "w")
       outFile.write(data)
       outFile.close()
       print "Done writing to file %s.:)\n" % (fileName)
    cursor1.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    sumIt = raw_input ("Do you want the list of proteins by groups ?(y/n)")
    if (sumIt == 'y'):
       global g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11
       summary = "\nProteins by group:\n\nGroup 1 --> %d\n%s\n\nGroup 2 --> %d\n%s\n\nGroup 3 --> %d\n%s\n\nGroup 4 --> %d\n%s\n\nGroup 5 --> %d\n%s\n\nGroup 6 --> %d\n%s\n\nGroup 7 --> %d\n%s\n\nGroup 8 --> %d\n%s\n\nGroup 9 --> %d\n%s\n\nGroup 10 --> %d\n%s\n\nGroup 11 --> %d\n%s\n\n" % (c1, g1, c2, g2, c3, g3, c4, g4, c5, g5, c6, g6, c7, g7, c8, g8, c9, g9, c10, g10, c11, g11)
       print summary
       ask = raw_input ("Write the group summary in file?(y/n)")
       if (ask == "y"):
          fileName2 = raw_input ("Enter group summary file name : ")
          outFile2 = open(fileName2, "w")
          outFile2.write(summary)
          outFile2.close()
          print "Done writing to file %s. Have a good rest of the day. :)" % (fileName2)
    else:
       print "OK. Have a good rest of the day. :)\n"

def menuData(db, cursor4):
    print "----------Group Division----------"
    print "group1 = bta"
    print "group2 = hsa,ptr"
    print "group3 = mcc"
    print "group4 = cfa"
    print "group5 = gga"
    print "group6 = mmu,rno"
    print "group7 = xtr"
    print "group8 = dre"
    print "group9 = aga, dme"
    print "group10 = spo,mgr,ncr,kla,ago,sce"
    print "group11 = ath,osa"
    print "---------------------------------\n"
    listPathway = raw_input ("Want to see all the pathways in the table? (y/n)")
    if (listPathway == "y"):
       commandList = "Select distinct pathwayName from organize;"
       cursor4.execute(commandList)
       for path in cursor4:
           print path[0]
    print "----------------------------------\n"
    print "Ok, you will be able to search one or union of two pathways. And if the program CRASH in MIDDLE we will troubleshoot then. Lets BEGIN :)\n\n"


def ProcessTwo(db, cursor1, cursor2, cursor3, cursor4, cursor5, pathOptionOne, pathOptionTwo, tableName):
    command = "CREATE VIEW fpath AS select mtHumanProtein, mtHomolog_id, org FROM organize where pathwayName = '%s';CREATE VIEW spath AS select mtHumanProtein, mtHomolog_id, org from organize where pathwayName = '%s';CREATE VIEW %s AS select fpath.mtHumanProtein, fpath.mtHomolog_id, fpath.org from fpath INNER JOIN spath ON fpath.mtHomolog_id = spath.mtHomolog_id;" % (pathOptionOne, pathOptionTwo, tableName)
    cursor1.execute(command)
    cursor1.close()
    cursor1 = db.cursor()
    data = startProcess(db, cursor1, cursor2, cursor3, cursor4, cursor5, tableName)
    closeCommand = "drop view fpath;drop view spath;drop view %s;" % (tableName)
    cursor1.execute(closeCommand)
    return data

def ProcessOne(db, cursor1, cursor2, cursor3, cursor4, cursor5, pathOptionOne, tableName):
    command = "CREATE VIEW %s AS select mtHumanProtein, mtHomolog_id, org from organize where pathwayName = '%s';" % (tableName, pathOptionOne)
    cursor1.execute(command)
    cursor1.close()
    cursor1 = db.cursor()
    data = startProcess(db, cursor1, cursor2, cursor3, cursor4, cursor5, tableName)
    closeCommand1 = "DROP VIEW %s;" % (tableName)
    cursor1.execute(closeCommand1)
    return data
    
     
def startProcess(db, cursor1, cursor2, cursor3, cursor4, cursor5, tableName):
# retrieve the data from the database and start the new table entry
    answer = "Summary of Analysis\n\n\n"
    command2 = "SELECT distinct mtHumanProtein FROM %s;" % (tableName)
    cursor1.execute(command2)
    count = 0
    for row in cursor1:
        mtHumanProtein = row[0]
        command3 = "SELECT distinct mtHomolog_id, org FROM %s where mtHumanProtein = '%s';" % (tableName, mtHumanProtein)
        command4 = "SELECT count(distinct org) FROM %s where mtHumanProtein = '%s';" % (tableName, mtHumanProtein)
        cursor3.execute(command4)
        cursor2.execute(command3)
        otherHomolog = butHomo(db, cursor5, mtHumanProtein, tableName)
        orgNo = 0
        for coun in cursor3:
            orgNo = coun[0]
            break
        infoOrg = notInOrg(db, cursor3, tableName, mtHumanProtein)
        count = count + 1
        add = "____________________________________\n\nProtein No. %d\nHuman counterpart : %s\n____________________________________\n" % (count, mtHumanProtein) 
        answer = answer + add
        countIn = 0 
        for row1 in cursor2: 
            mtHomolog_id = row1[0]
            org = row1[1]
            addSub = mtHomolog_id + " -> " + org + "\n"
            answer = answer + addSub
            countIn = countIn + 1
        totalHomo = "\nTotal homolog = %d\nTotal distinct organism = %d\n%s\n" % (countIn, orgNo, infoOrg)
        answer = answer + totalHomo + otherHomolog + "\n\n"
    return answer
            
def butHomo(db, cursor5, mtHumanProtein, tableName):
    command7 = "CREATE VIEW allHomo AS select mtHomolog_id, org, pathwayName FROM organize where mtHumanProtein = '%s';CREATE VIEW qHomo AS select mtHomolog_id, org FROM %s where mtHumanProtein = '%s';CREATE VIEW ans AS select distinct mtHomolog_id, org, pathwayName from allHomo where not exists (select mtHomolog_id from qHomo where qHomo.mtHomolog_id = allHomo.mtHomolog_id);" % (mtHumanProtein, tableName, mtHumanProtein)
    cursor6 = db.cursor()
    cursor6.execute(command7)
    cursor6.close()
    cursor6 = db.cursor()
    command8 = "select mtHomolog_id, org, pathwayName from ans"
    cursor6.execute(command8)
    otherHomolog = ""
    for x in cursor6:
        otherHomolog = otherHomolog + x[0] + " -> " + x[1] + " -> " + x[2] + "\n"
    if (otherHomolog == ""):
       otherHomolog = "NONE"
    otherHomolog = "Other Homolog Not in search:\n" + otherHomolog
    command9 = "DROP VIEW allHomo; DROP VIEW qHomo;DROP VIEW ans;"
    cursor6.execute(command9)
    return otherHomolog

def notInOrg(db, cursor3, tableName, mtHumanProtein):
    command4 = "CREATE VIEW orgTemp AS select distinct org from %s where mtHumanProtein = '%s';" % (tableName, mtHumanProtein)
    command5 = "select distinct org from orgTemp;"
    command6 = "select distinct org from organize where not exists (select distinct org from orgTemp where organize.org = orgTemp.org);"
    cursor3.execute(command4)
    cursor3.execute(command5)
    presentIn = ""
    count = 0
    for orIn in cursor3:
        presentIn = orIn[0] + ", " + presentIn
        count = count + 1
    if (count == 0):
       presentIn = "NONE"
    groupInfo = groupCheck(db, cursor3, mtHumanProtein)
    cursor3.execute(command6)
    notOrg = ""
    count = 0
    for orNo in cursor3:
        notOrg = orNo[0] + ", " + notOrg
        count = count + 1
    if (count == 0):
       notOrg = "NONE"
    replySum = "Protein present in : %s\nProtein not present in : %s\n%s" % (presentIn, notOrg, groupInfo)
    closeOrgTemp = "DROP VIEW orgTemp;"
    cursor3.execute(closeOrgTemp)
    return replySum

def groupCheck(db, cursor3, mtHumanProtein):
    group1 = ['bta']
    group2 = ['hsa','ptr']
    group3 = ['mcc']
    group4 = ['cfa']
    group5 = ['gga']
    group6 = ['mmu','rno']
    group7 = ['xtr']
    group8 = ['dre']
    group9 = ['aga','dme']
    group10 = ['spo','mgr','ncr','kla','ago','sce']
    group11 = ['ath','osa']
    groups = [0,0,0,0,0,0,0,0,0,0,0,0]
    inGroup = ""
    notInGroup = ""
    for orIn in cursor3:
        if orIn[0] in group1:
           groups[1] = 1
        elif orIn[0] in group2:
           groups[2] = 1
        elif orIn[0] in group3:
           groups[3] = 1
        elif orIn[0] in group4:
           groups[4] = 1
        elif orIn[0] in group5:
           groups[5] = 1
        elif orIn[0] in group6:
           groups[6] = 1
        elif orIn[0] in group7:
           groups[7] = 1
        elif orIn[0] in group8:
           groups[8] = 1
        elif orIn[0] in group9:
           groups[9] = 1
        elif orIn[0] in group10:
           groups[10] = 1
        elif orIn[0] in group11:
           groups[11] = 1
        else:
           y = "NONE"
    for x in range(1,12):
        g = "Group%d" % (x)
        if (groups[x] == 1):
           inGroup = inGroup + g + ", "
        else:
           notInGroup = notInGroup + g + ", "
        x = x + 1
    if (notInGroup == ""):
       notInGroup = "NONE"
    if (inGroup == ""):
       inGroup = "NONE"
    reply = "Present in Groups : %s\nNot present in Groups : %s" % (inGroup, notInGroup)
    totalSum(groups, mtHumanProtein)
    return reply    

def totalSum(groups, mtHumanProtein):
    global g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 
    if (groups[1] == 1):
       g1 = g1 + mtHumanProtein + ", "
       c1 = c1 + 1
    if (groups[2] == 1):
       g2 = g2 + mtHumanProtein + ", "
       c2 = c2 + 1
    if (groups[3] == 1):
       g3 = g3 + mtHumanProtein + ", "
       c3 = c3 + 1
    if (groups[4] == 1):
       g4 = g4 + mtHumanProtein + ", "
       c4 = c4 + 1
    if (groups[5] == 1):
       g5 = g5 + mtHumanProtein + ", "
       c5 = c5 + 1
    if (groups[6] == 1):
       g6 = g6 + mtHumanProtein + ", "
       c6 = c6 + 1
    if (groups[7] == 1):
       g7 = g7 + mtHumanProtein + ", "
       c7 = c7 + 1
    if (groups[8] == 1):
       g8 = g8 + mtHumanProtein + ", "
       c8 = c8 + 1
    if (groups[9] == 1):
       g9 = g9 + mtHumanProtein + ", "
       c9 = c9 + 1
    if (groups[10] == 1):
       g10 = g10 + mtHumanProtein + ", "
       c10 = c10 + 1
    if (groups[11] == 1):
       g11 = g11 + mtHumanProtein + ", "
       c11 = c11 + 1
main()
