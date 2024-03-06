import pygsheets
import pandas as pd
import re
from datetime import date

#to do, setup two sheet generation; one for just ratings and the other including comments

#authorization
gc = pygsheets.authorize(service_account_file=r'C:\Users\mathe\project\mhw-rating-tracker.json')

# Create empty dataframe
df = pd.DataFrame()

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('MHW Hunting Log')

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
current_log = []

def main():

    try:
        opening_question = '''Welcome! Please type a command below using one of the following keywords.
        Generate New Sheet / Modify Sheet / Log, open / Quit
        Ex: 'gen','mod','log', or 'quit'
        Task:'''
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
    main()
    
def mod_sheet():

    try:
        #to do, bulk mod multiple monsters with 'This monster was hunted on: '
        s = input('\nExample Entry: "ls alatreon s+ example text"\nOr, type "log" to see your log. \n\nMod:')
        if s.lower() == 'log': check_log()
        s_split = s.split(' ')
        weapon = weapon_cleaner(s_split[0])
        monster = monster_cleaner(s_split[1])
        text = ' '.join(s_split[2:])  
        entry_date = str(date.today())
        text += ' (' + entry_date + ')'

        print(f"\nWeapon: {weapon}")
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
    
        if len(text) > 0 and check.lower() != 'n':
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
        s = input('''\nPlease type your weapon followed by 'world' to see the log for that weapon. 
        Or type your weapon of choice, followed by hunting region, elenement, or species
        Ex: 'sns world' || 'ls tundra' 
        Ex: 'bow fire'  || 'ig brutes'
        Log Request:''')
        s_split = s.split(' ')
        weapon = weapon_cleaner(s_split[0])
        target_log = s_split[1]
        missing_log = ''
        empty_log = True

        element = element_cleaner(target_log)
        if element != False:
            target_log = element
            empty_log = False
            missing_log = element_log(weapon, element)

        species = species_cleaner(target_log)
        if species != False:
            target_log = species
            empty_log = False
            missing_log = species_log(weapon, species)

        if empty_log:
            area = region_cleaner(s_split[1])
            target_log = area
            missing_log = region_log(weapon, area)
        
        #to do, share current_log between functions to show wheneever you mod a weapon
        if missing_log == '': 
            print(f"Log for {weapon} and {target_log} complete!\n")
            main()
        if missing_log[-2:] == ', ':
            missing_log = missing_log[:-2]
            missing_log += '.'
        print(f"\nMissing Log for {weapon}: {missing_log}\n")

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
        ['Pukei-Pukei', 'pukei', 'puki', 'pooky','pookie'],
        ['Coral Pukei-Pukei','coral'],
        ['Barroth', 'barroth', 'bar', 'roth'],
        ['Kulu-Ya-Ku', 'kulu', 'kulu-ya-ku', 'kuluyaku','chicken'],
        ['Savage Deviljho', 'savagedeviljho', 'savage', 'jho','jo','pickle'],
        ['Frostfang Barioth','frostfang','frostbarioth','fang','frost'],
        ['Nightshade Paolumu','nightshadepaolumu','nightshade','night'],
        ['Paolumu','paolumu','palomu'],
        ['Seething Bazelgeuse', 'seething','bazel','goose','bomber', 'bazo'],
        ['Raging Brachydios', 'ragingbrachydios', 'raging','raging brachy'],
        ["Glavenus", 'glavenus','glave'],
        ["Acidic Glavenus", 'acidicglavenus','acidicglave','acidic','acid']
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
        #note: elders does not use elder. this is because elder is needed for the species, and dragon for the element. 
        region_nest = [
        ['Rotten Vale', 'rotten','rotted','vale', 'rot', 'r'],
        ['Elders Recess', 'recess', 'volano', 'volcanic','v'],
        ['Hoarfrost Reach','hoarfrostreach', 'hoarfrost','reach','tundra','t'],
        ['Ancient Forest', 'ancient', 'forest','woods','f'],
        ['Coral Highlands', 'coralhighlands','coral','highlands', 'c' ],
        ['Wildspire Waste','wildspirewaste','wildspire','waste','desert','wild'],
        ['World','world','all','everywhere',],
    ]

        original = s.capitalize()
        s = s.replace(' ', '').lower()
        for region_list in region_nest:
            for name_var in region_list[1:]:
                if re.match(name_var, s):
                    return region_list[0]
        return(original) 
def region_log(weapon, area):

    
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
        "Furious Rajang", "Rathalos", "Azure Rathalos", "Silver Rathalos",
        "Rathian", "Pink Rathian", "Gold Rathian", "Safi'jiiva",
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
        'Diablos', 'Black Diablos', 'Ebony Odogaron', 'Rajang', 'Tobi-Kadachi', 'Nightshade Paolumu', 'Barroth',
        'Kulu-Ya-Ku', 'Pink Rathian', 'Pukei-Pukei', 'Banbaro', 'Pink Rathian',
        'Anjanath', 'Fulgur Anjanath', 'Savage Deviljho', 'Lunastra', 'Teostra', 'Glavenus', 'Ruiner Nergigante', 'Velkhana'
    ]

    coral = [
        'Legiana', 'Paolumu', 'Coral Pukei-Pukei', 'Namielle', 'Savage Deviljho','Ruiner Nergigante', 'Rajang', 'Tzitzi-Ya-Ku', 'Kirin', 'Velkhana', 'Zinogre', 
        'Pink Rathian', 'Banbaro', 'Silver Rathalos', 'Ebony Odogaron', 'Fulgur Anjanath', 'Nargacuga', 'Odogaron'
    ]

    rotted = [
        'Brute Tigrex', 'Ebony Odogaron', 'Radobaan','Rajang', 'Savage Deviljho', 'Acidic Glavenus',
        'Ruiner Nergigante', 'Blackveil Vaal Hazak', 'Velkhana'
    ]

    volcanic = [
        'Seething Bazelgeuse', 'Rathalos', 'Azure Rathalos', 'Silver Rathalos', 'Gold Rathian','Tigrex', 'Dodogama', 'Uragaan',
        'Brachydios', 'Savage Deviljho', 'Glavenus', 'Rajang', 'Ruiner Nergigante', 'Velkhana', 'Lavasioth',
        'Ebony Odogaron','Fulgur Anjanath', 'Kushala Daora', 'Lunastra', 'Teostra'
    ]

    tundra = [
        'Barioth', 'Shrieking Legiana', 'Tigrex', 'Paolumu', 'Nightshade Paolumu', 'Legiana',
        'Odogaron', 'Ebony Odogaron', 'Rajang', 'Zinogre', 'Savage Deviljho','Stygian Zinogre', 'Ruiner Nergigante', 'Velkhana'
    ]
    regions = {'Ancient Forest': forest, 'Wildspire Waste': wildspire, 'Coral Highlands': coral, 'Rotten Vale': rotted, 'Elders Recess': volcanic, 'Hoarfrost Reach': tundra, 'World':world}

    print(f"\nWeapon: {weapon}")
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

    return missing_log

def element_cleaner(s):
        element_nest = [
        ['Fire Weakness', 'fire',],
        ['Ice Weakness', 'ice', 'cold',],
        ['Water Weakness','water', 'wat',],
        ['Thunder Weakness', 'thunder', 'lightning','thun','light'],
        ['Dragon Weakness', 'dragon','drag'],
        ]
        s = s.replace(' ', '').lower()
        for element_list in element_nest:
            for name_var in element_list[1:]:
                if re.match(name_var, s):
                    return element_list[0]
        return(False) 

def species_cleaner(s):
        species_nest = [
        ['Bird Wyverns', 'birds','bird','burb'],
        ['Brute Wyverns', 'brutes','brute','brut'],
        ['Elder Dragons','elder dragons', 'elders','elder'],
        ['Fanged Wyverns', 'fanged', 'fangs','fang'],
        ['Flying Wyverns', 'flying', 'fly'],
        ['Piscine Wyvern', 'piscine', 'pisc', 'fish']
        ]
        s = s.replace(' ', '').lower()
        for species_list in species_nest:
            for name_var in species_list[1:]:
                if re.match(name_var, s):
                    return species_list[0]
        return(False) 

def species_log(weapon,species):
    bird = [
        "Kulu-Ya-Ku", "Pukei-Pukei", "Tzitzi-Ya-Ku",
        "Coral Pukei-Pukei", "Yian Garuga", "Scarred Yian Garuga"
    ]
    brute = [
        "Anjanath", "Barroth",
        "Radobaan", "Uragaan", "Fulgur Anjanath",
        "Banbaro", "Brachydios", "Raging Brachydios",
        "Savage Deviljho", "Glavenus", "Acidic Glavenus"
    ]
    elder = [
        "Behemoth", "Kirin", "Kulve Taroth",
        "Kushala Daora", "Lunastra",
        "Teostra", "Alatreon", "Namielle",
        "Ruiner Nergigante", "Safi'jiiva", "Shara Ishvalda",
        "Blackveil Vaal Hazak", "Velkhana", "Fatalis"
    ]
    fanged = [
        "Dodogama", "Great Girros", "Great Jagras",
        "Odogaron", "Tobi-Kadachi", "Ebony Odogaron",
        "Viper Tobi-Kadachi", "Zinogre", "Stygian Zinogre"
    ]
    flying = [
        "Diablos", "Black Diablos",
        "Legiana", "Paolumu", "Rathalos",
        "Azure Rathalos", "Rathian", "Pink Rathian",
        "Barioth", "Seething Bazelgeuse", "Shrieking Legiana",
        "Nargacuga", "Nightshade Paolumu", "Silver Rathalos",
        "Gold Rathian", "Tigrex", "Brute Tigrex",
        "Frostfang Barioth"
    ]
    piscine = [
        "Jyuratodus", "Lavasioth", "Beotodus"
    ]

    species_dict = {'Bird Wyverns': bird, 'Brute Wyverns': brute,
                'Elder Dragons': elder, 'Fanged Wyverns': fanged,
                'Flying Wyverns': flying, 'Piscine Wyvern': piscine,
                }

    #to do, figure out how to add ' weakness' later, instead of listing here
    print(f"\nWeapon: {weapon}")
    print(f"Species: {species_cleaner(species)}")

    selected_species = species_dict.get(species, [])

    weapon_cell = str(wks.find(weapon))
    weapon_cell = weapon_cell.split(' ')
    weapon_column = weapon_cell[1][0]

    missing_log = ''

    for monster in selected_species:
        monster_cell = str(wks.find(monster))
        monster_cell = monster_cell.split(' ')
        monster_row = monster_cell[1]
        monster_row = monster_row[1:]
        cell =  weapon_column + monster_row
        test_cell = str(wks.cell((cell)))

        if test_cell[-3:] == "''>":
            missing_log += monster + ', '
    return missing_log
    
def mhw_help():
    #to do, list accepted names for a monsters
    #to do, list accepted names for a weapon
    #to do, allow user to add more names to the list off acceptbale nicknames
    ...

def element_log(weapon,element):
    water = [
        "Anjanath", "Kulu-Ya-Ku", "Great Girros",
        "Teostra", "Zorah Magdaros","Uragaan",
        "Tobi-Kadachi", "Lavasioth", "Glavenus",
        "Ebony Odogaron", "Nightshade Paolumu", "Yian Garuga",
        "Scarred Yian Garuga", "Silver Rathalos", "Brute Tigrex"
    ]
    fire = [
        "Great Jagras", "Paolumu", "Legiana",
        "Kirin", "Vaal Hazak", "Leshen",
        "Ancient Leshen", "Beotodus", "Velkhana",
        "Shrieking Legiana", "Barioth", "Acidic Glavenus",
        "Namielle", "Alatreon", "Frostfang Barioth"
    ]
    lightning = [
        "Tzitzi-Ya-Ku", "Pukei-Pukei", "Bazelgeuse",
        "Jyuratodus", "Legiana", "Nergigante",
        "Dodogama", "Kushala Daora", "Deviljho",
        "Viper Tobi-Kadachi", "Nargacuga", "Tigrex",
        "Savage Deviljho", "Gold Rathian"
    ]
    ice = [
        "Diablos", "Odogaron", "Tzitzi-Ya-Ku",
        "Black Diablos", "Teostra", "Lunastra",
        "Coral Pukei-Pukei","Brachydios",
        "Fulgur Anjanath", "Seething Bazelgeuse",
        "Shara Ishvalda", "Zinogre", "Rajang",
        "Raging Brachydios", "Furious Rajang", "Alatreon"
    ]
    dragon = [
        "Rathian", "Rathalos", "Radobaan",
        "Pink Rathian", "Azure Rathalos",
        "Vaal Hazak", "Deviljho", "Banbaro",
        "Savage Deviljho", "Ruiner Nergigante"
    ]

    elements = {'Fire Weakness': fire, 'Water Weakness': water, 'Lightning Weakness':lightning, 'Ice Weakness':ice, 'Dragon Weakness':dragon}
    #to do, figure out how to add ' weakness' later, instead of listing here

    print(f"\nWeapon: {weapon}")
    print(f"Element: {element_cleaner(element)}")

    selected_element = elements.get(element, [])

    weapon_cell = str(wks.find(weapon))
    weapon_cell = weapon_cell.split(' ')
    weapon_column = weapon_cell[1][0]

    missing_log = ''

    for monster in selected_element:
        monster_cell = str(wks.find(monster))
        monster_cell = monster_cell.split(' ')
        monster_row = monster_cell[1]
        monster_row = monster_row[1:]
        cell =  weapon_column + monster_row
        test_cell = str(wks.cell((cell)))

        if test_cell[-3:] == "''>":
            missing_log += monster + ', '
    return missing_log

if __name__ == "__main__":
    main()
