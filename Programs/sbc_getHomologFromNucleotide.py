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
# 
# This program reads the sequences in the FASTA format for the 
# entered file and prints the header nad the sequence as desired
# by the user in the monitor or in a file.

import MySQLdb
import sys
import getopt
import os, sys
from Bio import Entrez
from Bio.KEGG.REST import *

def main():
    Entrez.email = "sbc@unomaha.edu"

# Open database connection and prepare a cursor object using cursor() method
    
    print "If you don't enter the right db Name and password the program will crash"
    dbUser = raw_input ("Please enter an existing MYSQLdb username: ")
    dbPass = raw_input ("Please enter the password for the user: ")
    dbName = raw_input ("Please enter the database Name: ")
    db = MySQLdb.connect("localhost", dbUser, dbPass, dbName)
    cursor = db.cursor()
# read the command in the command line and put it in an array
#Display error if the option is not recognized
    try:
          opts, args = getopt.getopt(sys.argv[1:], "i:o")
    except getopt.GetoptError,err:
          print str(err)
          usage()
          sys.exit(2)
# Go through commands line and perform the corresponding tasks
    for (opt, arg) in opts:
#read from the input file if there is "-i" present in the command line    
        if opt == "-i":
            inFile = open(arg, "r")
            lines = inFile.readlines();
            inFile.close()
    tableChoice = raw_input ("Create tables (y/n) : ")
    if (tableChoice == "y"):
        createTable(db, cursor)
    for line in lines:
        accession = line[0:-1]
        nucleotide_id = accession
        which_db = "protein"
        getProtein(which_db, nucleotide_id, db, cursor)
    db.close()

#create table in mysql
def createTable(db, cursor):
# Create table to store mitochondria nucleotide and its respective protein id
    command = """CREATE TABLE humanMtProtein (
            ID int NOT NULL AUTO_INCREMENT,
            mtNucleotide_id varchar(26) NOT NULL, 
            mtProtein_id varchar(26),
	    PRIMARY KEY (ID)
            )"""
    dbExecute(db, cursor, command)
# Create table to store human mtProtein and its homolog
    command = """CREATE TABLE humanMtHomolog (
            ID int NOT NULL AUTO_INCREMENT,
            mtHumanProtein varchar(26) NOT NULL, 
            mtHomolog_id varchar(50) NOT NULL,
            gi varchar(26) NOT NULL,
	    keggID varchar(26) NOT NULL,
            org varchar(26) NOT NULL,
            PRIMARY KEY (ID)
            )"""
    dbExecute(db, cursor, command)

#get the respective protein
def getProtein(which_db,search_term, db, cursor):
    search_handle = Entrez.esearch(db=which_db, term=search_term)
    record = Entrez.read(search_handle)
    search_handle.close()
    tmpFileName = search_term + "." + which_db + ".tmp"
    f=open(tmpFileName,"w")
    for id in record["IdList"]:
        fetch_handle = Entrez.efetch(db=which_db, id= id, rettype="fasta", retmode="text")
        data=fetch_handle.read()
        fetch_handle.close()
        f.write(data)
    f.close()
    parser(tmpFileName, search_term, which_db, db, cursor)

# FASTA PARSER
def parser(tmpFileName, search_term, which_db ,db, cursor):
    tmpFile = open(tmpFileName,"r")
    tmpLines = tmpFile.readlines();
    tmpFile.close()
    none = "NONE"
    gi = "NONE"
    org = "NONE"
    protein_id = "NONE"
    kegg_id = "NONE"
    tmpSize = os.stat(tmpFileName).st_size
    data = ""
    if ((which_db == "homologene") and (tmpSize == 0)):
        search_handle = Entrez.esearch(db="protein", term=search_term)
        record = Entrez.read(search_handle)
        search_handle.close()
        tFile = search_term + ".tmp"
        f=open(tFile,"w")
        for id in record["IdList"]:
	    fetch_handle = Entrez.efetch(db="protein",id=id, rettype="fasta", retmode="text")
            data = fetch_handle.read()
            fetch_handle.close()
            f.write(data)
        f.close
        os.remove(tFile)
        datas = data.split("|")
        gi = datas[1]
        kegg_ids = keggConvert(gi)
        keggSplit = kegg_ids.split("+")
        org = keggSplit[0]
        kegg_id = keggSplit[1]
        sendDatabase(search_term, gi, protein_id, which_db, db, cursor, org, kegg_id)
    else:
        for tmpLine in tmpLines:
	    if (tmpLine[0] == ">"):
	        sentid = parse(tmpLine, search_term, db, cursor)
		ids = sentid.split("+")
		gi = ids[0]
		protein_id = ids[1]
		kegg_ids = keggConvert(gi)
		keggSplit = kegg_ids.split("+")
		org = keggSplit[0]
		kegg_id = keggSplit[1] 
                sendDatabase(search_term, gi, protein_id, which_db, db, cursor, org, kegg_id)
                if (which_db == "protein"):
                    getProtein("homologene", protein_id, db, cursor) 
    os.remove(tmpFileName)

def parse(inLine, search_term, db, cursor):
# Parse the FASTA data
#Get rid of the last space in the line, split the line at "|" take
    inLine = inLine[0:-1]
    fields = inLine.split("|")
    gi = fields[1]
    protein_id = fields[3]
    name = fields[4]
    send = gi + "+" + protein_id
    return send

def sendDatabase(search_term, gi, protein_id, which_db, db, cursor, org, kegg_id):
    command = ""
    if (which_db == "protein"):
        command = "INSERT INTO humanMtProtein (mtNucleotide_id, mtProtein_id) VALUES ('%s','%s')" % (search_term, protein_id)
    elif (which_db == "homologene"):
        command = "INSERT INTO humanMtHomolog (mtHumanProtein, mtHomolog_id, gi, keggID, org) VALUES ('%s','%s','%s','%s','%s')" % (search_term, protein_id, gi, kegg_id, org)
#    elif (which_db == "cdd"):
#        command = "INSERT INTO humanMtCdd (mtNucleotide_id, mtCdd_id) VALUES ('%s', '%s')" % (search_term, protein_id)
    else:
        print "\nNo database table provided!! :(\n"
    print command
#    dbExecute(db, cursor, command)

def dbExecute(db, cursor, command):
# insert values in database
    print command
    try:
        cursor.execute(command)
    except:
        db.rollback()
    db.commit()
    
def keggConvert(gi):
#convert to kegg
    ncbi_gi = "ncbi-gi:"+gi
    listIT = kegg_conv("genes",ncbi_gi)
    reading = listIT.read()
    f=open("kegg.tmp","w")
    f.write(reading)
    f.close
    f=open("kegg.tmp","r")
    readd = f.read();
    f.close()
    fSize = os.stat("kegg.tmp").st_size
    os.remove("kegg.tmp")
    send = "NONE+NONE"
    if (fSize > 1):
    	datas1 = readd.split(":")
    	datas2 = datas1[1].split()
    	send = datas2[1] + "+" + datas1[2]
    return send

#usage function to print out the command line option error
def usage():
     print "usage:" + sys.argv[0] + " [-i FILE] [-o FILE]"
     print "-i: input file (FASTA-formatted); STIN if not used."
#     print "-o: output file (tab-delimited); STDOUT if not used."
#     print "-s sequence display option"
#End of usage
main()
