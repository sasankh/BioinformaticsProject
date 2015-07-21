
import MySQLdb
import sys
import getopt
import os, sys

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
    tableChoice = raw_input ("Create tables (y/n) : ")
    if (tableChoice == "y"):
        createTable(db, cursor3)
    startProcess(db, cursor1, cursor2, cursor3)

def createTable(db, cursor3):
# Create new table
    command = """CREATE TABLE organize (
            ID int NOT NULL AUTO_INCREMENT,
            mtHumanProtein varchar(26) NOT NULL,
            mtHomolog_id varchar(26) NOT NULL,
            gi varchar(26) NOT NULL,
            org varchar(50) NOT NULL,
            keggID varchar(50) NOT NULL,
            pathway varchar(50) NOT NULL,
            pathwayName varchar(50) NOT NULL,
            mtChecker varchar(700),
            PRIMARY KEY (ID)
            )"""
    dbExecute(db, cursor3, command)

def startProcess(db, cursor1, cursor2, cursor3):
# retrieve the data from the database and start the new table entry
    command1 = "SELECT mtHumanProtein, mtHomolog_id, keggID, org, gi FROM humanMtHomolog WHERE keggID NOT LIKE 'NONE';"
    cursor1.execute(command1)
    for row in cursor1:
        mtHumanProtein = row[0]
        mtHomolog_id = row[1]
        keggID = row[2]
        org = row[3]
        gi = row[4]
        if (mtHomolog_id == "NONE"):
            mtHomolog_id = mtHumanProtein;
        trueKeggID = org + ":" + keggID
#        print mtHumanProtein+" : "+mtHomolog_id+" : "+keggID+" : "+trueKeggID+" : "+gi
        pathways = getPathways(trueKeggID, db, cursor2, mtHumanProtein, mtHomolog_id, org, gi, cursor3)

def getPathways(trueKeggID, db, cursor2, mtHumanProtein, mtHomolog_id, org, gi, cursor3):
     command2 = "SELECT keggID, pathway, pathwayName, mtChecker FROM keggPathwayMt WHERE keggID = '%s';" % (trueKeggID)
     cursor2.execute(command2)
     for row1 in cursor2:
	keggID = row1[0]
	pathway = row1[1]
	pathwayName = row1[2]
        mtChecker = row1[3]
        command3 = "INSERT INTO organize (mtHumanProtein, mtHomolog_id, gi, org, keggID, pathway, pathwayName, mtChecker) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s');" % (mtHumanProtein, mtHomolog_id, gi, org, keggID, pathway, pathwayName, mtChecker)
        dbExecute(db, cursor3, command3)

def dbExecute(db, cursor, command):
# insert values in database
    print command
    try:
        cursor.execute(command)
    except:
        db.rollback()
    db.commit()
main()
