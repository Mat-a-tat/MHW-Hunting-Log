import pygsheets
import pandas as pd
import re
import fnmatch

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
weapons = [
    "GS", "LS", "SNS", "DB", "HAM", "HH", "LANCE", "GL", "SA", "CB", "IG", "LBG", "HBG", "BOW"
]

str_cell = str(wks.cell((4,3)))
print(str_cell[-3:])

def main():

    try:
        s = input("Generate New Sheet / Modify Sheet / See Log\n")
        answer = s.lower()
        if answer == 'generate new sheet' or answer == 'gen':
            make_sheet()
        if answer == 'modify sheet' or answer == 'mod':
            mod_sheet()
        if answer == 'see log' or answer == 'log':
            check_log()
    except:
        s = input("Generate New Sheet / Modify Sheet")
def make_sheet():
    df[' '] = monsters

    #update the first sheet with df, starting at cell B2. 
    wks.update_row(1, weapons, col_offset=0)
    wks.set_dataframe(df,(1,1))

    print("Your new worksheet has been created!")
def mod_sheet():

    try:
        s = input('Example Entry: "ls alatreon s+ skill issue "\n Or, type "log" to see your log. \n Mod:')
        if s.lower() == 'log':
            check_log()
        s_split = s.split(' ')
        weapon = s_split[0].upper()
        monster = s_split[1].capitalize()
        text = ' '.join(s_split[2:])  # Join all elements after the weapon and monster


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
        # i orignally planned to put some testing in to regrex find partial spellings, but...this does that automaticly. very neat.

        if test_cell[-3:] != "''>":
            #to do, regex to get just the text of the cell
            print(f"Current Entry:{test_cell}")
            s = input("Cell not empty. Overwrite? (y/n):")
            if s.upper() != 'Y':
                print("Returning to mod menu.")
                mod_sheet()

        # Update the cell in the worksheet
        if len(text) > 0:
            wks.update_value(cell,text)
            print(f'Cell modified:{cell}')
            print("Update made!")
        else: 
            print("No text changed.")

        s = input("Would you like to make an another entry? (y/n):")
        if s.capitalize() == 'Y':mod_sheet()
        else: 
            print("Happy hunting!")
            quit()

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Booting you back to startup")
        main()


    
def check_log():
    forest = [
        'Nargacuga', 'Paolumu', 'Nightshade Paolumu', 'Rathalos', 'Azure Rathalos', 'Rathian',
        'Pink Rathian', 'Tigrex', 'Brute Tigrex', 'Dodogama', 'Great Girros', 'Great Jagras',
        'Ebony Odogaron', 'Rajang', 'Zinogre', 'Yian Garuga', 'Scarred Yian Garuga', 'Anjanath',
        'Fulgur Anjanath', 'Banbaro', 'Brachydios', 'Savage Deviljho', 'Glavenus', 'Namielle',
        'Ruiner Nergigante', 'Velkhana'
    ]

    wildspire = [
        'Diablos', 'Black Diablos', 'Legiana', 'Odogaron', 'Ebony Odogaron', 'Rajang',
        'Tobi-Kadachi', 'Viper Tobi-Kadachi', 'Kulu-Ya-Ku', 'Pukei-Pukei', 'Coral Pukei-Pukei',
        'Yian Garuga', 'Anjanath', 'Fulgur Anjanath', 'Banbaro', 'Barroth', 'Savage Deviljho',
        'Glavenus', 'Lunastra', 'Teostra', 'Velkhana'
    ]

    coral = [
        'Legiana', 'Nargacuga', 'Paolumu', 'Nightshade Paolumu', 'Rathalos', 'Azure Rathalos',
        'Tzitzi-Ya-Ku', 'Coral Pukei-Pukei', 'Namielle', 'Ruiner Nergigante', 'Velkhana'
    ]

    rotted = [
        'Seething Bazelgeuse', 'Nargacuga', 'Rathalos', 'Azure Rathalos', 'Silver Rathalos',
        'Paolumu', 'Nightshade Paolumu', 'Odogaron', 'Ebony Odogaron', 'Radobaan', 'Banbaro',
        'Savage Deviljho', 'Glavenus', 'Acidic Glavenus', 'Ruiner Nergigante', 'Velkhana'
    ]

    volcanic = [
        'Seething Bazelgeuse', 'Rathalos', 'Azure Rathalos', 'Silver Rathalos', 'Dodogama',
        'Uragaan', 'Brachydios', 'Savage Deviljho', 'Glavenus', 'Acidic Glavenus', 'Ruiner Nergigante', 'Velkhana'
    ]

    tundra = [
        'Barioth', 'Legiana', 'Shrieking Legiana', 'Nargacuga', 'Rathalos', 'Azure Rathalos',
        'Silver Rathalos', 'Paolumu', 'Nightshade Paolumu', 'Tigrex', 'Brute Tigrex', 'Odogaron',
        'Ebony Odogaron', 'Rajang', 'Zinogre', 'Stygian Zinogre', 'Kirin', 'Ruiner Nergigante',
        'Velkhana'
    ]

    regions = {'forest': forest, 'wildspire': wildspire, 'coral': coral, 'rotted': rotted, 'volcanic': volcanic, 'tundra': tundra}

    s = input("Please type your weapon of choice, followed by hunting region.\nEx: 'ls tundra'")
    s_split = s.split(' ')
    weapon = s_split[0].upper()
    area = s_split[1].lower()

    print(f"Weapon: {weapon}")
    print(f"Area: {area}")

    selected_region = regions.get(area, [])

    weapon_cell = str(wks.find(weapon))
    weapon_cell = weapon_cell.split(' ')
    weapon_column = weapon_cell[1][0]

    missing_log = []

    for monster in selected_region:
        monster_cell = str(wks.find(monster))
        monster_cell = monster_cell.split(' ')
        monster_row = monster_cell[1]
        monster_row = monster_row[1:]
        cell =  weapon_column + monster_row
        test_cell = str(wks.cell((cell)))
        # i orignally planned to put some testing in to regrex find partial spellings, but...this does that automaticly. very neat.

        if test_cell[-3:] == "''>":
            missing_log.append(monster)
    print(missing_log)

    s = input("Would you like to check another log?(y/n):")
    if s.lower() == 'y':
        check_log()
    else:
        s = input("Return to main menu? (y/n): ")
        if s.lower() == 'y': main()
        else: print('Happy Hunting!')






    
# to do: list missing monsters, list missing monsters in a GL region, dictonary of monster names / appreviates on a dictonary
if __name__ == "__main__":
    main()
