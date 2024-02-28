import pygsheets
import pandas as pd

#to do, setup two sheet generation; one for just ratings and the other including comments

#authorization
gc = pygsheets.authorize(service_file=r'C:\Users\mathe\project\mhw-rating-tracker.json')

# Create empty dataframe
df = pd.DataFrame()

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('MHW Ratings Export')

def main():

    try:
        s = input("Generate New Sheet / Modify Sheet")
        answer = s.lower()
        if answer == 'generate new sheet' or answer == 'gen':
            make_sheet()
        if answer == 'modify sheet' or answer == 'mod':
            mod_sheet()
    except:
        s = input("Generate New Sheet / Modify Sheet")

def make_sheet():
    # this could all be done manually, but for the sake of programing stuff
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
    "GS (Great Sword)", "LS (Long Sword)", "SNS (Sword and Shield)", "DB (Dual Blades)",
    "HAM (Hammer)", "HH (Hunting Horn)", "LANCE", "GL (Gunlance)",
    "SA (Switch Axe)", "CB (Charge Blade)", "IG (Insect Glaive)", "LBG (Light Bowgun)",
    "HBG (Heavy Bowgun)", "BOW"
    ]
    df[' '] = monsters

    #select the first sheet 
    wks = sh[0]

    #update the first sheet with df, starting at cell B2. 
    wks.update_row(1, weapons, col_offset=0)
    wks.set_dataframe(df,(1,1))

    print("Your new worksheet has been created!")
def mod_sheet():
    s = input('Example Mod: "bow kirin s+ skill issue "\nRating:')
    s_split = s.split(' ')
    weapon = s_split[0]
    monster = s_split[1]
    rating = s_split[2]
    print(s)
    
def func_3():
    ...

if __name__ == "__main__":
    main()
