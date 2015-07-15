# BioinformaticsProject
Correlation study program
Reports, analysis, summary, etc not included only the code so that it can be used for other correlation studies.

Correlation Study of Proteins involved in both Mitochondria and Metabolism with Size of Organism steps available for example.

Other correlation studies can be done by selecting different proteins or organules.

:)OK this can be done in two ways. You can either import the database that has been provided or do everything from the beginning. The later may take more than a day.

Steps for 'Correlation Study of Proteins involved in both Mitochondria and Metabolism with Size of Organism'

Option 1: Quick and easy (If you only want to test the end result table “organize” and get summary)

1. Copy the Programs folder to a linux machine with mysql and biopython.

2. Make sure you have a mysql username and password with authority to create database.

3. In the terminal “mysql -u username -p” and login to your mysql.

4. Create a database by typing the command “CREATE DATABASE databaseName;”

5. Exit the mysql

6. Navigate to the Program file.

7. Import the tables to the database you just created “mysql -u username -p databaseName < BIOISubmit.sql”

8. Redo step 3

9. In mysql type “use databaseName;”

10. Type “show tables;”. There should be 5 tables. Make sure that the “organize” table is present. Its the normalized and optimized table.

11. exit mysql

12. Type “python sbc_AnalyzeThree.py” and then enter the mysql username, password and the databaseName.

13. Follow the rest of the program instruction. I suggest not to interrupt the program in the middle.

14. In case you stop the program in the middle. Then when you run the second time it might not run. Because virtual tables were created they have to be removed which is written in the end of the program. To remove the in the database you created in mysql type
“drop view  fpath; drop view spath; drop view finalTable; drop view allHomo; drop view ans; drop view orgTemp;”

15. Then start the “sbc_AnalyzeThree.py”

Note:

The “results” folder has the Individual and Group summary for
“metabolic pathways : metabolicGroup, metabolicIndividual”,
“oxidative phosphorylation : oxidativeGroup, oxidativeIndividual”, and
“metabolic pathways and oxidative phosphorylation: metabolicAndOxidativeIndividual, metabolicAndOxidativeGroup”

Option 2: Hard (If you only want to start from the beginning, will take a day or so to finish)

1. Copy the “Programs” folder and the “Modified KEGG REST” folder to a linux machine with mysql and biopython.

2. Make sure you have a mysql username and password with authority to create database.

3. Copy the “REST.py” file from the “Modified KEGG REST” to the newly downloaded biopython folder and replace with the “REST.py” at “biopython-1.65\Bio\KEGG\”. Reinstall biopython. OR if you can find where biopython is installed in your computer, Find the Kegg folder and replace the “REST.py” with the one that I have provided.

4. Navigate to the Program folder

5. In the terminal “mysql -u username -p” and login to your mysql.

6. Create a database by typing the command “CREATE DATABASE databaseName;”

5. Exit the mysql

6. Navigate to the Program file.

7. run “python sbc_getHomologFromNucleotide.py -i uniprot.refseq.prot.list”. If running for the first time say “y” to create table.

8. Once the program finish running run “python sbc_getPathwayMt.py”. If running for the first time say “y” to table creation.

10. Once that program is done run “python sbc_organize.py”

11. Once this program is done running follow “Option 1” from step 12.
