# Monster Hunter World Iceborne Hunting Log 
 
In a connected Google Sheets document using [Pygsheets](https://github.com/nithinmurali/pygsheets) , search by weapon to determine what monsters you have yet to fill out for in relation to that weapon, with an optional region being selected. Writes directly to individual cells of a monster and weapon. Generates base formating for a fresh document. This project is a capstone project for [CS50P](https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python).

The game features 14 weapon, all with (usually) distinct playstyles, and 65 differnet monsters all with (usually) distinct movesets. This tool was created assist with catalouging my journey in fighting every monster, with every weapon in the game, and recording my experiance of the fight afterwards. It became rather cumbersome to lookup individual cells within exell for every fight, and while it was possible to generate logs using sheets; I found that process to be even more cumbersome. As such, I designated this as my capstone project for my completion of CS50P. 

This project, however, is still rather unwealdy. It requires the prior generation and authenitcation of security keys through Google, and passing of those keys through the program itself. As such it presents a **security risk** to any unfamilair with using service acocunts or your the method of authentication, thus caution is advised. 

## Usage

1) Setup Pygsheets following thier instruction. Follow PyObtain OAuth2 credentials from Google Developers Console for google spreadsheet api and drive api and save the file as client_secret.json in same directory as project. [Detailed Explanation](https://pygsheets.readthedocs.io/en/latest/authorization.html)
2) Run this program at the command line using various commands. Each command is shown in usage below. 
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
### Generate New Sheet
*Requires to have authentication setup (by proxy, a JSON file loaded in the same directory) and a blank exell sheet linked to the project.*
```
Task: gen

Generating a new sheet can mess up an old one. Still generate a new sheet? (y/n):y
Theres some values in these cells! Overwrite them? (y/n):y
Base cells have been populated!
Formating Updated!
```
### Modify Sheet
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
### Log, see
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

## Methodology

Howdy! The rest of this is a more casual examination of the program as a whole, and decision decisions I made along the way. I include this ostiensibly as a requirment for the submission of my project into CS50P, but I do regardless find value in reflecting on this project. I created it to help me with a task, and it does! But not the way I inteded. The core conciet of the program arose from my combing through an exell file trying to find specific cells to input journal entries for each monster. While this program does help with that bit; I find the user experiance of that to be less than ideal. It is likely a sign of my amatour nature, but I don't enjoy navigating applicatoins via the command line, as useful as that might be. As such, I find myself not using that core function nearly as much as I do the log function; an addition I made almost as an afterthought. While I occassionally use this application to write to an Exell file, I much, much more frequently use it for the log function. It saves me such a great deal of a headache. 

Now, why sheets specificly? Because I don't own google office, and have no intention of buying it. Sheets its readily available, and importantly, widley used. I liked working with an applicatoin that has the scaleability and portability of sheets, over an exell doc. That goes both for myself (I enjoy hunting down my thoughts on a specific monster on my phone to prove myself wrong) and for others, I think. I wanted the experiance of working on a piece of software that other people use, and use frequently, and sheets does this in spades. However, the reliance on API / security keys does signifigently drop the accebility of this program, something I lament that I did not fully grasp until roughly halfway through. I was, regretably, commited at that point. I considered switching to makeing the entire thing text based and processed at the local level, but I decided against that for two reasons. The first was my desire to get experiance working with exell and sheets programaticly, something I was able to tinker with prior to this project, but never do more than simple relational formulas. The second is that im stuborn; I had already started a project, and I ascribe strongly to the Cult of Done. I figured finishing it with sheets was both easier (it wasent) and more rewarding (it was) than if I had switched to simple text processing. 

The biggest realization I had while working on this project, was how easy it was to continue to add features and robustness once a core program was properly established. Giving users the ability to use nicknames and shortened versions of different things to look them up? Easy. Adding a timestamp to every entry? Two lines of code. This is a rookie realization; that the modular nature of coding a program, when does correctly, allows for customization and upgrading to be done blazingly fast. I thoughly enjoyed this project, and want to thank all the people at CS50P for putting together their course. Its free! Go check it out! The bot checker is the most singularly rude piece of software I will ever work with, but it has helped me become the medicore coder I am now. I look forward to this being the (one of) the first pieces of software I write to do odd and wonderful things. 

*Thanks for reading <3*
