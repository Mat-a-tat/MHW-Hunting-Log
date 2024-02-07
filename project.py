import pygsheets
import pandas as pd
import re
import fnmatch
from datetime import date

#to do, setup two sheet generation; one for just ratings and the other including comments

#authorization
gc = pygsheets.authorize(service_file=r'C:\Users\mathe\project\MHW_Sheets_Rater\mhw-rating-tracker.json')

# Create empty dataframe
df = pd.DataFrame()

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('MHW Ratings Export')

#select the first sheet 
wks = sh[0]

monsters = [
"Alatreon", "Ancient Leshen", "Anjanath", "Fulgur Anjanath",
"Banbaro", "Barioth", "Frostfang Barioth", "Barroth",
"Seething Bazelgeuse", "Behemoth", "Beotodus", "Brachydios",
"Raging Brachydios", "Savage Deviljho", "Diablos", "Black Diablos",
"Dodogama", "Fatalis", "Glavenus", "Acidic Glavenus",
"Great Girros", "Great Jagras", "Jyuratodus", "Kirin",
"Kulu-Ya-Ku", "Kulve Taroth", "Kushala Daora", "Lavasioth",
"Legiana", "Shrieking Legiana", "Leshen", "Lunastra",
"Namielle", "Nargacuga", "Ruiner Nergigante", "Odogaron",
"Ebony Odogaron", "Paolumu", "Nightshade Paolumu", 
"Pukei-Pukei", "Coral Pukei-Pukei", "Radobaan", "Rajang",
"Furious Rajang", "Rathalos", "Azure Rathalos", "Gold Rathalos",
"Rathian", "Pink Rathian", "Silver Rathian", "Safi'jiiva",
"Shara Ishvalda", "Teostra", "Tigrex", "Brute Tigrex",
"Tobi-Kadachi", "Viper Tobi-Kadachi", "Tzitzi-Ya-Ku", "Uragaan",
"Blackveil Vaal Hazak", "Velkhana", "Yian Garuga", "Scarred Yian Garuga",
"Zinogre", "Stygian Zinogre"
]
#to do, replace with full names
weapons = [
    "Great Sword", "Long Sword", "Sword and Shield", "Dual Blades", 
    "Hammer", "Hunting Horn", "Lance", "Gunlance", "Switch Axe", 
    "Charge Blade", "Insect Glaive", "Light Bowgun", "Heavy Bowgun", "Bow"
]


def main():

    try:
        opening_question = "\nWelcome! Please type a command below using one of the following keywords. \nGenerate New Sheet / Modify Sheet / Log, open / Quit\nEx: 'gen','mod','log', or 'quit'\n\nTask:"
        s = input(f"{opening_question}")
        s = s.replace(' ','')
        answer = s.lower()
        if answer == 'generatenewsheet' or answer == 'gen' or answer == 'g':
            gen_sheet = input("Generating a new sheet can mess up an old one. Still generate a new sheet? (y/n):")
            if gen_sheet.lower() == 'y': 
                make_sheet()
        if answer == 'modifysheet' or answer == 'mod' or answer == 'm':
            mod_sheet()
        if answer == 'seelog' or answer == 'log' or answer == 'l':
            check_log()
        if answer == 'quit' or answer == 'q' or answer == 'exit':
            quit()
        if answer == 'test weapon':
            weapon = input("Weapon:")
            return(weapon_cleaner(weapon))
        if answer == 'test monster':
            monster = input("Monster:")
            return(monster_cleaner(monster))
    except:
        print("Invalid. Please type a command from below, or the first letter in the command.")
        s = input(f"{opening_question}")

def make_sheet():
    # to do, conditional formating
    # to do, do NOT overwrtite cells that have values in them. 

    #update the first sheet with df, starting at cell B2. 
    weapon_test_cell = str(wks.cell((1,2)))
    monster_test_cell = str(wks.cell((2,1)))

    if weapon_test_cell[-3:] != "''>" or monster_test_cell[-3:] != "''>":
        s = input("Theres some values in these cells! Overwrite them? (y/n):")
        if s.lower() == 'y':
            df[' '] = monsters
            wks.update_row(1, weapons, col_offset=1)
            wks.set_dataframe(df,(1,1))
            print("Base cells have been populated!")
        else: 
            print("No text inside cells modified.")  

    cell_range = 'A1:O66'
    wks.adjust_column_width(1, end=15, pixel_size=230)
    #we leave rows with default autoscalling, as setting the column does the bulk of the work.
    format_info = {
        "wrapStrategy": "WRAP",
    }
    wks.apply_format(cell_range, format_info)
    #to do, apply alternating colors. bit tricky to get right.
    #to do, apply additional optional conditianl colors onto cells themselves based on their rating / first few letters.
    print("Formating Updated!")
    


def mod_sheet():

    try:
        s = input('Example Entry: "ls alatreon s+ example text"\nOr, type "log" to see your log. \nMod:')
        if s.lower() == 'log': check_log()
        s_split = s.split(' ')
        weapon = weapon_cleaner(s_split[0])
        monster = monster_cleaner(s_split[1])
        text = ' '.join(s_split[2:])  
        entry_date = str(date.today())
        text += ' (' + entry_date + ')'

        print(f"Weapon: {weapon}")
        print(f"Monster: {monster}")
        print(f"Entry: {text}")

        monster_cell = str(wks.find(monster))
        weapon_cell = str(wks.find(weapon))
        
        monster_cell = monster_cell.split(' ')
        weapon_cell = weapon_cell.split(' ')

        weapon_collum = weapon_cell[1]
        weapon_collum = weapon_collum[0]
        monster_row = monster_cell[1]
        monster_row = monster_row[1:]

        cell =  weapon_collum + monster_row
        test_cell = str(wks.cell((cell)))

        if test_cell[-3:] != "''>":
            #to do, regex to get just the text of the cell
            print(f"Current Entry:{test_cell}")
            s = input("Cell not empty. Overwrite? (y/n):")
            if s.upper() != 'Y':
                print("Returning to mod menu.")
                mod_sheet()

        # Update the cell in the worksheet
        check = input(f'Cell to be modified: {cell}. Continue? (y/n):')
    
        if len(text) > 0 and check.lower != 'n':
            wks.update_value(cell,text)
            print(f'Cell modified: {cell}')
            print("Update made!")
        else: 
            print("No text changed.")

        main()
        '''
        s = input("Would you like to make an another entry? (y/n):")
        if s.capitalize() == 'Y':mod_sheet()
        '''
    

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Booting you back to startup")
        main()


    
def check_log():
    try:
        # to do, allow searching via monster 

        #list index out of range errors are likely 
        world = [
            "Alatreon", "Ancient Leshen", "Anjanath", "Fulgur Anjanath",
            "Banbaro", "Barioth", "Frostfang Barioth", "Barroth",
            "Seething Bazelgeuse", "Behemoth", "Beotodus", "Brachydios",
            "Raging Brachydios", "Savage Deviljho", "Diablos", "Black Diablos",
            "Dodogama", "Fatalis", "Glavenus", "Acidic Glavenus",
            "Great Girros", "Great Jagras", "Jyuratodus", "Kirin",
            "Kulu-Ya-Ku", "Kulve Taroth", "Kushala Daora", "Lavasioth",
            "Legiana", "Shrieking Legiana", "Leshen", "Lunastra",
            "Namielle", "Nargacuga", "Ruiner Nergigante", "Odogaron",
            "Ebony Odogaron", "Paolumu", "Nightshade Paolumu", 
            "Pukei-Pukei", "Coral Pukei-Pukei", "Radobaan", "Rajang",
            "Furious Rajang", "Rathalos", "Azure Rathalos", "Gold Rathalos",
            "Rathian", "Pink Rathian", "Silver Rathian", "Safi'jiiva",
            "Shara Ishvalda", "Teostra", "Tigrex", "Brute Tigrex",
            "Tobi-Kadachi", "Viper Tobi-Kadachi", "Tzitzi-Ya-Ku", "Uragaan",
            "Blackveil Vaal Hazak", "Velkhana", "Yian Garuga", "Scarred Yian Garuga",
            "Zinogre", "Stygian Zinogre"
        ]
        #having world like this is kind of hacky. I dont like having this list poping up in two places.
        #However, easier and more consistent than loops and text cleaning below. (this is copoium) 
        invaders = [
            'Savage Deviljho', 'Ruiner Nergigante','Rajang', 'Banbaro', 'Fulgur Anjanath', 'Ebony Odogaren',
        ]
        #invaders currenty does nothing, but might be useful later.
        forest = [
            'Nargacuga', 'Nightshade Paolumu', 'Rathalos', 'Azure Rathalos', 'Rathian', 'Great Jagras',
            'Tigrex', 'Anjanath', 'Fulgur Anjanath', 'Yian Garuga', 'Scarred Yian Garuga', 'Pukei-Pukei',
            'Banbaro', 'Brachydios', 'Savage Deviljho', 'Glavenus', 'Ruiner Nergigante', 'Kushala Daora',
            'Velkhana'
        ]

        wildspire = [
            'Diablos', 'Black Diablos', 'Odogaron', 'Ebony Odogaron', 'Rajang', 'Tobi-Kadachi',
            'Viper Tobi-Kadachi', 'Kulu-Ya-Ku', 'Pink Rathian', 'Pukei-Pukei', 'Banbaro', 'Great Jagras',
            'Anjanath', 'Fulgur Anjanath', 'Savage Deviljho', 'Lunastra', 'Teostra', 'Glavenus', 'Ruiner Nergigante', 'Velkhana'
        ]

        coral = [
            'Legiana', 'Paolumu', 'Coral Pukei-Pukei', 'Namielle', 'Savage Deviljho','Ruiner Nergigante', 'Rajang', 'Tzitzi-Ya-Ku', 'Kirin', 'Velkhana', 'Zinogre', 
            'Pink Rathian', 'Banbaro', 'Silver Rathian', 'Ebony Odogaron', 'Fulgur Anjanath', 'Nargacuga', 'Odogaron'
        ]

        rotted = [
            'Brute Tigrex', 'Ebony Odogaron', 'Radobaan','Rajang', 'Savage Deviljho', 'Acidic Glavenus',
            'Ruiner Nergigante', 'Blackveil Vaal Hazak', 'Velkhana'
        ]

        volcanic = [
            'Seething Bazelgeuse', 'Rathalos', 'Azure Rathalos', 'Silver Rathian', 'Dodogama', 'Uragaan',
            'Brachydios', 'Savage Deviljho', 'Glavenus', 'Acidic Glavenus','Rajang', 'Ruiner Nergigante', 'Velkhana'
        ]

        tundra = [
            'Barioth', 'Shrieking Legiana', 'Nargacuga', 'Tigrex', 'Brute Tigrex', 'Paolumu', 'Nightshade Paolumu',
            'Odogaron', 'Ebony Odogaron', 'Rajang', 'Zinogre', 'Savage Deviljho','Stygian Zinogre', 'Ruiner Nergigante', 'Velkhana'
        ]

        regions = {'Ancient Forest': forest, 'Wildspire Waste': wildspire, 'Coral Highlands': coral, 'Rotten Vale': rotted, 'Elders Recess': volcanic, 'Hoarfrost Reach': tundra, 'world':world}
        s = input("Please type your weapon followed by 'world' to see the log for that weapon.\n Or type your weapon of choice, followed by hunting region.\nEx: 'sns world'\nEx: 'ls tundra' \nLog Request:")
        s_split = s.split(' ')
        weapon = weapon_cleaner(s_split[0])
        area = region_cleaner(s_split[1])


        print(f"Weapon: {weapon}")
        print(f"Area: {region_cleaner(area)}")
        if area == 'world': print("Were searching the whole world here, so please be patient as this loads.")

        selected_region = regions.get(area, [])

        weapon_cell = str(wks.find(weapon))
        weapon_cell = weapon_cell.split(' ')
        weapon_column = weapon_cell[1][0]

        missing_log = ''

        for monster in selected_region:
            monster_cell = str(wks.find(monster))
            monster_cell = monster_cell.split(' ')
            monster_row = monster_cell[1]
            monster_row = monster_row[1:]
            cell =  weapon_column + monster_row
            test_cell = str(wks.cell((cell)))


            if test_cell[-3:] == "''>":
                missing_log += monster + ', '
        
        # todo, chop last comma of and replace with a peroid. 
        if missing_log == '': print(f"Log for {weapon} complete!")
        else: print(f"\nMissing Log for {weapon}: {missing_log}\n")

        main()

        '''
        s = input("Would you like to check another log?(y/n):")
        if s.lower() == 'y':
            check_log()
        '''
        '''
        s = input("Return to main menu? (y/n): ")
        if s.lower() == 'y': main()
        else: print('Happy Hunting!')
        '''
    except Exception as e:
        print(f"Error: {str(e)}")
        if str(e) == 'list index out of range': 
            #to do, change this to debugg
            print(" - - - Double check spellings of monsters in selected region - - -")
        print("Booting you back to startup")
        main()

def weapon_cleaner(s):

    #I chose to use nested loops here for my convience. dictonaries are faster, yes, but much less readable
    #and for this scale of data? the difference is marginal. 
    ig_list = ['Insect Glaive', 'insectglaive', 'glaive', 'ig', 'insect', 'kinsect']
    ham_list = ['Hammer', 'hammer', 'ham']
    sns_list = ['Sword and Shield', 'sword', 'shield', 'sns', 'ss']
    gs_list = ['Great Sword', 'greatsword', 'great','gs']
    ls_list = ['Long Sword', 'longsword','long', 'ls']
    db_list = ['Dual Blades', 'dualblades','blades', 'dual', 'db']
    sa_list = ['Switch Axe', 'switchaxe', 'switch','axe', 'sa']
    cb_list = ['Charge Blade', 'chargeblade', 'cb']
    hh_list = ['Hunting Horn', 'huntinghorn', 'horn', 'hh']
    lance_list = ['Lance', 'lance', 'ln']
    gl_list = ['Gunlance', 'gunlance', 'gl']
    bow_list = ['Bow', 'bow']
    hbg_list = ['Heavy Bowgun', 'heavybowgun', 'hbg']
    lbg_list = ['Light Bowgun', 'lightbowgun', 'lbg']

    weapon_nest = [ig_list,ham_list,sns_list,gs_list, ls_list,db_list,sa_list,cb_list,hh_list,lance_list,gl_list,bow_list,hbg_list, lbg_list]

    original = s
    s = s.replace(' ', '').lower()

    for weapon_list in weapon_nest:
        for name_var in weapon_list[1:]:
            if re.match(name_var, s):
                return weapon_list[0]
            
    return original

def monster_cleaner(s):

    #not an exhaustive list, and there are MANY monsters in the game. inclusion is arbitray, or whichever monsters i consistnelty spell wrong
    #g sheets has a decent change of cleaning up our responses automaticlly, but its not perfect. 
    monster_nest = [
        ['Rathalos', 'rathalos', 'rath'],
        ['Rathian', 'rathian', 'ian'],
        ['Diablos', 'diablos', 'diablo'],
        ['Kirin', 'kirin', 'thunderhorse','unicorn'],
        ['Nergigante', 'nergigante', 'nergi', 'nerr','nergs'],
        ['Teostra', 'teostra', 'teo'],
        ['Kushala Daora', 'kushala', 'kush','daora'],
        ['Vaal Hazak', 'vaal','val', 'hazak', 'vaalhazak','havok'],
        ['Xeno\'jiiva', 'xeno', 'jiiva'],
        ['Zinogre', 'zinogre', 'zino', 'gre'],
        ['Brachydios', 'brachydios', 'brachy', 'dios', 'bracky'],
        ['Tigrex', 'tigrex', 'tig', 'rex'],
        ['Odogaron', 'odogaron', 'odo', 'dog', 'hellpuppy'],
        ['Legiana', 'legiana', 'leg', 'liana','legi'],
        ['Anjanath', 'anjanath', 'anja', 'janath'],
        ['Pukei-Pukei', 'pukei', 'puki', 'pooky'],
        ['Barroth', 'barroth', 'bar', 'roth'],
        ['Kulu-Ya-Ku', 'kulu', 'kulu-ya-ku', 'kuluyaku','chicken'],
        ['Savage Deviljho', 'savagedeviljho', 'savage', 'jho','jo','pickle'],
        ['Frostfang Barioth','frostfang','frostbarioth','fang','frost'],
        ['Nightshade Paolumu','nightshadepaolumu','nightshade','night'],
        ['Paolumu','paolumu','palomu'],
        ['Seething Bazelgeuse', 'seething','bazel','goose','bomber', 'bazo'],
        ['Raging Brachydios', 'ragingbrachydios', 'raging','raging brachy']
    ]

    original = s.capitalize()
    s = s.replace(' ', '').lower()
    for monster_list in monster_nest:
        for name_var in monster_list[1:]:
            if re.match(name_var, s):
                return monster_list[0]
            
    return original
def region_cleaner(s):
        #the first letter tags correlate to thier guiding land regions names
        region_nest = [
        ['Rotten Vale', 'rotten','rotted','vale', 'rot', 'r'],
        ['Elders Recess', 'elder', 'elders', 'recess', 'volano', 'volcanic','v'],
        ['Hoarfrost Reach','hoarfrostreach', 'hoarfrost','reach','tundra','t'],
        ['Ancient Forest', 'ancient', 'forest','woods','f'],
        ['Coral Highlands', 'coralhighlands','coral','highlands', 'c' ],
        ['Wildspire Waste','wildspirewaste','wildspire','waste','desert','w'],
    ]

        original = s.capitalize()
        s = s.replace(' ', '').lower()
        for region_list in region_nest:
            for name_var in region_list[1:]:
                if re.match(name_var, s):
                    return region_list[0]
        return(original)
            
def mhw_help():
    #to do, list accepted names for a monsters
    #to do, list accepted names for a weapon
    #to do, allow user to add more names to the list off acceptbale nicknames
    ...

if __name__ == "__main__":
    main()
