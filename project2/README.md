## What has been done?

### Day 1

- Firstly, we inspected Prof. Seagal workstation's disk image **carl_disk.img** after running tools like ```mmls``` and ```fstat``` and were able to find Seagal's linux partition, which was formatted in Ext4

- The same thing was done to his backup disk **backup_disk.img** in which the working partition was formatted in Ext4 aswell

- First thing we've done after gaining acess to the linux partition of the disk was analyzing the file **bash_history** in Prof Seagal's home directory (workstation). This gave us some insight on the last commands that were ran on the terminal before the workstation was confiscated by the authorities

- In the bash history we've encountered some references to Seagal's backups, which were done using a script called **backup.sh**, and when analyzing this file, it referenced another file named **pass_gen.sh**  

NOTE: In order to extract files, first we search for the file's inode using ```fls -o 1054720 carl_disk.img -r carl_disk.img | grep FILENAME```  

After finding the inode, we extract the file using ```icat -o 1054720 carl_disk.img INODENUMBER > FILEDESTINATION```

- **pass_gen.sh** referenced a file called **obfuscator** 

- We were able to retrieve **obfuscator** after running ```file obfuscator``` and found out this was a compiled python script

- After decompiling this file, we were able to see that it used the content of a file named **seeds.txt** (also found on Seagal's workstation) as seeds to generate a password for the backup zip file

- **seeds.txt** had a lot of lines, each one containing one seed, everytime obscurator ran, the first seed from **seeds.txt** was pushed to the bottom and used in **obfuscator**

- We came to the conclusion that in order to get the passwords generated at a given time from **obfuscator**, we would need the seed that it used at that moment and the **timestamp** of that moment

- **Timestamps** were easy to obtain, as they were in each backup's file name, and since the seeds were reordered in a simple manner each time **obfuscator** was used, they were also easy to obtain, as the last 4 backups would have the last 4 seeds in **seeds.txt**

- This way allowed us to get the passwords to unzip the **backup zip files**, which we were able to do with success
