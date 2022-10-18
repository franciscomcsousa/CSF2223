## What has been done?

### Day 1

- Firstly, we inspected Prof. Seagal workstation's disk image **carl_disk.img**. After running tools like ```mmls``` and ```fstat```, we were able to find Seagal's linux partition (formatted in Ext4).

- The same thing was done to his backup disk **backup_disk.img**. The working partition was formatted in Ext4 aswell.

- First thing we did after gaining access to the linux partition of the disk was to analyze the file **bashhistory** in Prof Seagal's home directory (workstation), this gave us some insight of the last commands that were ran on the terminal before the workstation was recovered by the authorities.

- In the bash history we encountered some references to Seagal's backups, which were created using a script called **backup.sh**. When analyzing this file, it referenced another file named **pass_gen.sh**.  

NOTE: In order to extract files, first we search for the file's inode using ```fls -o 1054720 carl_disk.img -r carl_disk.img | grep FILENAME```.  

After finding the inode, we extract the file using ```icat -o 1054720 carl_disk.img INODENUMBER > FILEDESTINATION```.

- **pass_gen.sh** referenced a file named **obfuscator**.

- We were able to retrieve **obfuscator**. After running ```file obfuscator``` we found out this was a compiled python script.

- After decompiling this file, we were able to see that it used a filed named **seeds.txt** (also found on Seagal's workstation) as seeds to generate a password to the backup zip file.

- **seeds.txt** had numerous lines, each one containing one seed, everytime obscurator was executed, the first seed from **seeds.txt** was pushed to the bottom, and the top seed was used in **obscurator**.

- We came to the conclusion that in order to get the passwords generated at a given time from **obscurator** we would need the **seed** that it used at that execution and the **timestamp** of that moment.

- **Timestamps** were easy to obtain, as they were in each backup's file name. As the seeds were reordered in a simple manner each time **obfuscator** was executed, they were also easy to obtain. The last 4 backups would have the last 4 seeds in **seeds.txt**.

- This way we were able to get the passwords to unzip the **backup zip files**, which we were able to do with success.

### Day 2

- After analyzing Seagal's **_firefox** directory, we inspected Seagal's web history in the file  **places.sqlite**. Running ```sqlite3 places.sqlite``` and afterwards ```.dump```, we were able to see that Seagal visited an online python decompiler (probability to decompile **tool**) and visited [**hexed.it**](https://hexed.it/) (an online hex editor, probably used to removed the header of the file named **Golf**).

- In Seagal's web history there were also some visits to websites that provided information on how to safely delete linux files (in order to totally hide their existance).

- Still in regards to the previous point, in Seagal's **bash_history** we saw him running the command ```srm -vz -r  moon/*```. Uppon further inspection, we came to the conclusion that **srm** is used to safely delete files and possibly hide them from authorities (as it is explained in this tool's manual, which also was present in one of Seagal's backups)

- The first command that is present in Seagal's **bash_history** was ```irssi```. **irssi** is a terminal based text chat client with IRC support. After googling if this program recorded chat logs, we came to the conclusion that if they were enabled, they would be stored in ```/home/USERNAME/irclogs```. After running ```fls -o 1054720 carl_disk.img -r carl_disk.img | grep irclogs```, we were able to find the inode that correponded to the **irclogs** directory. Inside, we were able to find some **chat logs** of Prof.Seagal with a suspect named **Megan Polanski**, who claims to be President Nixon's grandson's wife.

- (Todo - Explain what Seagal and Megan Polanski discuss about in the irc log)