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
    """
    print("A football season has 17 game days for each team.")
    gameday = int(input("Enter the current gameday number(from 1 to 17)\n"))

    try: 
        if gameday > 17 or gameday < 1:
            raise ValueError("The number entered is not correct")
    except ValueError as e:
        print(f"Invalid value: {e}, please enter a number between 1 and 17.\n")
        get_gameday()
    else:
        return gameday


def check(name, gameday):
    """
    This function checks, if the gameday already exists in the spreadsheet.
    """
    existing_names = user_input.col_values(8)
    existing_gamedays = user_input.col_values(9)

    print(existing_names)


#def check_integer(value):
 #   """
  #  This helper function checks various variables for integer numbers.
   # If the values are not integer values, the user must change the given input.
    #"""

    #try'

def main():
    """
    This function calls all necessary functions in the right order, 
    according to the flow chart in the doc.
    """
    start()
    name = get_quarterback()
    gameday = get_gameday()
    check()


main()