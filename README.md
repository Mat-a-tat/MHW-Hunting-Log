# Monster Hunter World Iceborne Hunting Log 
 
In a connected Google Sheets document using [Pygsheets](https://github.com/nithinmurali/pygsheets) , search by weapon to determine what monsters you have yet to fill out for in relation to that weapon, with an optional region being selected. Writes directly to individual cells of a monster and weapon. Generates base formating for a fresh document. 

The game features 14 weapon, all with (usually) distinct playstyles, and 65 differnet monsters all with (usually) distinct movesets. This tool was created assist with catalouging my journey in fighting every monster, with every weapon in the game, and recording my experiance of the fight afterwards. It became rather cumbersome to lookup individual cells within exell for every fight, and while it was possible to generate logs using sheets; I found that process to be even more cumbersome. As such, I designated this as my capstone project for my completion of CS50P. 

This project, however, is still rather unwealdy. It requires the prior generation and authenitcation of security keys through Google, and passing of those keys through the program itself. As such it presents a **security risk** to any unfamilair with using service acocunts or your the method of authentication, thus caution is advised. 

## Usage

1) Setup Pygsheets following thier instruction. Follow PyObtain OAuth2 credentials from Google Developers Console for google spreadsheet api and drive api and save the file as client_secret.json in same directory as project. [Detailed Explanation](https://pygsheets.readthedocs.io/en/latest/authorization.html)
2) Run this program at the command line using various commands. Each command is shown in usgae below. 
```
python project.py
```
From there, you will be taken to the home page:
```
Welcome! Please type a command below using one of the following keywords.
Generate New Sheet / Modify Sheet / Log, open / Quit
Ex: 'gen','mod','log', or 'quit'

Task:
```
# Generate New Sheet
*Requires to have authentication setup, and a (preferably) blank exell sheet.*
```
Task: gen

Generating a new sheet can mess up an old one. Still generate a new sheet? (y/n):y
Theres some values in these cells! Overwrite them? (y/n):y
Base cells have been populated!
Formating Updated!
```
# Modify Sheet
```
Task:mod
Example Entry: "ls alatreon s+ example text"
Or, type "log" to see your log.

Mod:bow savage This is an example.

Weapon: Bow
Monster: Savage Deviljho
Entry: This is an example. (2024-02-07)
Cell to be modified: M15. Continue? (y/n):y
Cell modified: M15
Update made!
```
# Log, see
```
Task:log
Please type your weapon followed by 'world' to see the log for that weapon.
 Or type your weapon of choice, followed by hunting region.
Ex: 'sns world'
Ex: 'ls tundra'
Log Request:hbg coral 
Weapon: Heavy Bowgun
Area: Coral Highlands

Missing Log for Heavy Bowgun: Legiana, Paolumu, Coral Pukei-Pukei, Namielle, Savage Deviljho, Ruiner Nergigante, Rajang, Tzitzi-Ya-Ku, Kirin, Velkhana, Zinogre, Pink Rathian, Banbaro, Silver Rathian, Ebony Odogaron, Fulgur Anjanath, Nargacuga, and Odogaron
```
