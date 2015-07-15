
import MySQLdb
import sys
import getopt
import os, sys
from Bio import Entrez
from Bio.KEGG.REST import *
#from Bio.KEGG.KGML.KGML_parser import *
def main():

# Open database connection and prepare a cursor object using cursor() method
    print "If you don't enter the right db Name and password the program will crash"
    dbUser = raw_input ("Please enter an existing MYSQLdb username: ")
    dbPass = raw_input ("Please enter the password for the user: ")
    dbName = raw_input ("Please enter the database Name: ")
    db = MySQLdb.connect("localhost", dbUser, dbPass, dbName)
    cursor = db.cursor()
    command = "SELECT keggID, org, mtHomolog_id FROM humanMtHomolog WHERE keggID NOT LIKE 'NONE';"
    tableChoice = raw_input ("Create tables (y/n) : ")
    if (tableChoice == "y"):
        createTable(db, cursor)
    startProcess(db, cursor, command)

def createTable(db, cursor):
# Create table to store pathways from KEGG
    command = """CREATE TABLE keggPathwayMt (
            ID int NOT NULL AUTO_INCREMENT,
            protein varchar(26) NOT NULL,
            org varchar(50) NOT NULL,
            keggID varchar(50) NOT NULL,
            pathway varchar(50) NOT NULL,
            pathwayName varchar(50) NOT NULL,
            mtChecker varchar(700),
            PRIMARY KEY (ID)
            )"""
    dbExecute(db, cursor, command)

def startProcess(db, cursor, command):
# retrieve the data from the database and start the new table entry
    cursor.execute(command)
    count = 0
    for row in cursor:
        keggID = row[0]
        org = row[1]
        mtHomolog_id = row[2]
        print "protein : " + mtHomolog_id
        sendToKegg = org + ":" + keggID
        received = findPathway(sendToKegg)
        rSplit = received.split("+++")
        pathways = rSplit[0]
        mtChecker = rSplit[1]
        readyDbEntry(org, keggID, sendToKegg, pathways, mtHomolog_id, db, cursor, mtChecker)
    print count

def readyDbEntry(org, keggID, sendToKegg, pathways, protein, db, cursor, mtChecker):
    pathwaysSplit = str(pathways)
    mtChecker = str(mtChecker)
    if (pathwaysSplit == "NONE"):
        command = "INSERT INTO keggPathwayMt (protein, org, keggID, pathway, pathwayName, mtChecker) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (protein ,org, sendToKegg, "NONE", "NONE", mtChecker)
        dbExecute(db, cursor, command)
    else:
        pathwaysSplit = pathwaysSplit.split("\n")
        for path in pathwaysSplit:
            if (path != ""):
                pathCode = ""
                pathName = ""
                pathSplit = path.split()
                pathCode = pathSplit[0]
                for x in range(1, len(pathSplit)):
                    pathName = pathName + pathSplit[x] + " "
                command = "INSERT INTO keggPathwayMt (protein, org, keggID, pathway, pathwayName, mtChecker) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (protein, org, sendToKegg, pathCode, pathName, mtChecker)
                dbExecute(db, cursor, command)

def findPathway(sendToKegg):
    dbKegg = "pathway"
    data = kegg_get(sendToKegg)
    keggData = data.read()
    pathways = getPathway(keggData)
    mtCheck = getMtCheck(keggData)
    if (pathways == ""):
        pathways = "NONE"
    send = pathways + "+++" + mtCheck
    return send

def getPathway(keggData):
    pathways = ""
    check = 0
    datas = keggData.split("\n")
    for data in datas:
        fpathway = data.split()
        if (fpathway[0] == "///"):
	    break
        if ((fpathway[0] == "DISEASE") | (fpathway[0] == "BRITE") | (fpathway[0] == "MODULE")):
	    check = 0
            break
        if ((fpathway[0] == "PATHWAY") | (check == 1)):
	    if (fpathway[0] == "PATHWAY"):
               data = data.split('PATHWAY')[1]
            pathways = pathways + data + "\n"
	    check = 1
    return pathways

def getMtCheck(keggData):
    mtCheck = ""
    datas = keggData.split("\n")
    for data in datas:
        mtDatas = data.split()
        if (mtDatas[0] == "///"):
            break
        for mtData in mtDatas:
	    if ((mtData == "mitochondria") | (mtData == "Mitochondrial") | (mtData == "Mitochondria") | (mtData == "mitochondrial")):
                dataConvert = mtConvert(mtDatas)
                mtCheck = mtCheck + dataConvert + " | "
                print dataConvert
    if (mtCheck == ""):
        mtCheck = "NONE"
    return mtCheck

def mtConvert(mtDatas):
    goodSend = ""
    for mtData in mtDatas:
        goodSend = goodSend + " " + mtData
    return goodSend

def dbExecute(db, cursor, command):
# insert values in database
    print command
    try:
        cursor.execute(command)
    except:
        db.rollback()
    db.commit()
main()
