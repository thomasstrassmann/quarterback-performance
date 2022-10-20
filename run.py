import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('quarterback_performance')

user_input = SHEET.worksheet('input')
averages = SHEET.worksheet("averages")


def start():
    """
    Welcomes the user to the interface.
    Explains the benefits of using the app.
    """
    print("Welcome to the quarterback performance app") 
    print("- The source for individual quarterback ratings\n")
    print("Here you can enter the statistics of the match day...")
    print("and see exactly how your favorite players performed.\n")
    print("################\n")


def get_quarterback():
    """
    Gets the name of the quarterback from the user.
    Capitalizes the first letter of the lastname.
    """
    name = input("Enter the lastname of the quarterback here: \n")
    name = name.title()
    return name


def get_gameday():
    """
    Gets the gameday integer from the user.
    Checks if the number is between 1 and 17.
    """
    print("A football season has 17 game days for each team.")
    
    while True: 
        gameday = int(input(
            "Please enter the current gameday (from 1 to 17)\n"))
        if gameday > 17 or gameday < 1:
            print(f"{gameday} is not a number between 1 and 17.\n")
            continue
        else:
            return gameday
            break


def check(name, gameday):
    """
    This function checks, if the gameday already exists in the spreadsheet.
    """
    existing_names = user_input.col_values(8)
    existing_names = existing_names[1:]

    existing_gamedays = user_input.col_values(9)
    existing_gamedays = existing_gamedays[1:]

    overview = list(zip(existing_names, existing_gamedays))
    current_input = (name, str(gameday))

    if current_input in overview:
        print("This game of the season has already been entered")
        print("Please choose another quarterback / gameday combination\n")
        main()
    else:
        print("Please type in the following values for " 
              f"{name}`s {gameday} game of the season")
        return current_input


def get_values(statistic):
    """
    This function gets all values from the user as an integer.
    It gets called with different parameters to cover any query.
    """
    while True:
        try:
            statistic = int(input(f"Enter the number of {statistic}: "))
        except ValueError:
            print("Please enter an integer number")
            continue
        else:
            return statistic
            break


def main():
    """
    This function calls all necessary functions in the right order, 
    according to the flow chart in the doc.
    """
    name = get_quarterback()
    gameday = get_gameday()
    new_entry = check(name, gameday)
    passes_completed = get_values("pass completions")
    passes_thrown = get_values("pass attempts")
    yards = get_values("thrown yards")
    touchdowns = get_values("passing touchdowns")
    interceptions = get_values("interceptions")
    sacks = get_values("sacks")
    

start()
main()