"""
This module takes statisitcal inputs from the user and calculates
the passing performance from a quarterback based on the
average values of last year and the performances to other
quarterback values, that has been entered.
"""

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
    print("Welcome to the quarterback performance app!")
    print("The source for individual quarterback ratings.\n")
    print("Here you can enter the statistics of the match day...")
    print("and see exactly how your favorite players performed.\n")
    print("The QPA shows you first, how the QB entered performed")
    print("in relation to the average values of last year, \n"
          "assigning school grades to the performance.")
    print("Then, all QBs in the database are compared to eachother.")
    print("Each player gets a specific score, which is made up of \n"
          "the averages of yards thrown, touchdowns and interceptions.\n")
    print("################\n")


def get_quarterback():
    """
    Gets the name of the quarterback from the user.
    It makes sure, no number is included and the name is not "Average",
    because otherwise the program crashes.
    Capitalizes the first letter of the lastname.
    """
    while True:
        name = input("Enter the lastname of the quarterback here: \n")
        name = name.title()

        if True in [i.isdigit() for i in name]:
            print("The name must not contain numbers!")
            continue
        elif name == "Average":
            print("This name is already taken, please choose another one.")
            continue
        else:
            return name


def get_gameday():
    """
    Gets the gameday integer from the user.
    Checks if the number is between 1 and 17.
    """
    print("\nA football season has 17 game days for each team.")

    while True:
        gameday = int(input(
            "Please enter the current gameday (from 1 to 17)\n"))
        if gameday > 17 or gameday < 1:
            print(f"{gameday} is not a number between 1 and 17.\n")
            continue
        else:
            return gameday


def check(name, gameday):
    """
    This function checks, if the gameday already exists in the spreadsheet.
    """
    existing_names = user_input.col_values(7)
    existing_names = existing_names[1:]

    existing_gamedays = user_input.col_values(8)
    existing_gamedays = existing_gamedays[1:]

    overview = list(zip(existing_names, existing_gamedays))
    current_input = (name, str(gameday))

    if current_input in overview:
        print("\nThis game of the season has already been entered")
        print("Please choose another quarterback / gameday combination\n")
        main()
    else:
        print("\nPlease type in the following values for "
              f"{name}`s {gameday} game of the season")
        return current_input


def get_values(statistic):
    """
    This function gets all values from the user as an integer.
    It gets called with different parameters to cover any query.
    """
    while True:
        try:
            statistic = int(input(f"Enter the number of {statistic}: \n"))
        except ValueError:
            print("Please enter an integer number")
            continue
        else:
            return statistic


def value_block():
    """
    This code block calls all get_value functions and stores them in a
    container.If the input is completed the user has the chance to
    check the values and change them, if he wants to.
    The function returns the container list if the user confirms the input.
    """
    while True:
        passes_completed = get_values("pass completions")
        passes_thrown = get_values("pass attempts")
        yards = get_values("thrown yards")
        touchdowns = get_values("passing touchdowns")
        interceptions = get_values("interceptions")
        sacks = get_values("sacks")
        container = [passes_completed, passes_thrown,
                     yards, touchdowns, interceptions, sacks]
        print("Are the values above correct?")
        response = input("Enter y for yes or n for no: \n")
        if response == 'y':
            return container
        elif response == 'n':
            continue
        else:
            print("Please enter y or n")
            response = input("Enter y for yes or n for no: \n")


def save(entry, values):
    """
    The save function takes the entry (name and gameday) and the values
    as arguments. First, the entry tuple gets converted to a list,
    then the two value pairs get concatenated and
    then stored to the worksheet input.
    """
    entry = list(entry)
    data_to_update = values + entry
    user_input.append_row(data_to_update)
    print("Calculating... Please wait a second!\n")


def calculate_averages(name):
    """
    This function checks first, if the name is already in the sheets, or if it
    is the first time the user entered the name.
    If it is the first entry, the function just takes the value from the
    worksheet input and copies it into the averages, to save some resources.
    If the name is already in the input worksheet, the first if clause
    finds all entries, and trims them down to the necessary values.
    Then it converts every entry in the list to an integer number and adds
    all values together. Every item of the combined container then get divided
    by the number of entries to get the average. The last 4 lines in the
    if clause find the existing values in the averages, deletes them, and
    replaces them with the new correct values.
    """
    container = []
    if averages.find(name) is not None:
        cells = user_input.findall(name)
        for i in cells:
            trim = user_input.row_values(i.row)[0:6]
            container.append(trim)
        container = [[int(float(j)) for j in i] for i in container]
        combined_container = [sum(x) for x in zip(*container)]
        dividend = len(container)
        averages_container = []
        for i in combined_container:
            average = i / dividend
            averages_container.append(round(average, 1))
        target = averages.find(name)
        averages.delete_rows(target.row)
        averages_container.append(name)
        averages.append_row(averages_container)
    else:
        cell = user_input.find(name)
        values = user_input.row_values(cell.row)[0:7]
        averages.append_row(values)


def calculate_efficency():
    """
    The calculate_efficeny function calculates the pass completion percentage.
    It does it by grabbing and converting all values in the
    passes_completed and passes_thrown columns fo floats in the average
    worksheet. Then it zips them together in one container and calculates
    the percentage. After that, the columns are updated with the new
    value.
    """
    passes_completed = averages.col_values(1)[1:]
    passes_completed = [float(x.replace(',', '.')) for x in passes_completed]

    pass_attempts = averages.col_values(2)[1:]
    pass_attempts = [float(x.replace(',', '.')) for x in pass_attempts]

    percentage = [round((i / j) * 100, 1) for i, j in zip(passes_completed,
                                                          pass_attempts)]
    percentage = [[i] for i in percentage]
    length_of_column = len(percentage) + 1
    averages.update(f"H2:H{length_of_column}", percentage)


def compare():
    """
    The compare function first gets the average values and stores them in
    a list. After that, a player dictonary gets created by iterating over
    the players data.The dictonarys keys are the players, which contain a
    dictionary themselves.
    The players dictonary consists of the keys stats(individual player stats),
    diff(the difference calculated to the average values)
    and grades(calculated in the next function).
    The function returns the whole dictonary.
    """
    average = averages.batch_get(["C2:F2", "H2"])
    flat_list = [item for list in average for item in list]
    average_list = flat_list[0] + flat_list[1]

    players = averages.col_values(7)[2:]
    players_dict = {player: {"stats": "", "diff": "", "grades": [],
                    "score": ""} for player in players}

    for i in players_dict:
        target = averages.find(i)
        raw_player_stats = averages.row_values(target.row)
        reduced_player_stats = raw_player_stats[2:6]
        reduced_player_stats.append(raw_player_stats[7])
        players_dict[i]["stats"] = reduced_player_stats

    for player in players_dict:
        float_averages = [float(x.replace(',', '.')) for x in average_list]
        float_stats = [float(x.replace(',', '.'))
                       for x in players_dict[player]["stats"]]
        difference = [i - j for i, j in zip(float_averages, float_stats)]
        rounded_difference = [round(num, 1) for num in difference]
        players_dict[player]["diff"] = rounded_difference
    return players_dict


def rate(name, players_dict):
    """
    The rate function takes the complete players dict as an argument.
    It evaluates the grades for each stat by grabbing the differences
    to the average and comparing them to a set of conditions.
    """
    pass_diff = players_dict[name]["diff"][0]
    td_diff = players_dict[name]["diff"][1]
    int_diff = players_dict[name]["diff"][2]
    sack_diff = players_dict[name]["diff"][3]
    comp_diff = players_dict[name]["diff"][4]
    grade = players_dict[name]["grades"]

    if pass_diff <= -60.2:
        grade.append("A")
    elif pass_diff >= -60.1 and pass_diff <= -20.1:
        grade.append("B")
    elif pass_diff >= -20 and pass_diff <= 20:
        grade.append("C")
    elif pass_diff >= 20.1 and pass_diff <= 60.1:
        grade.append("D")
    else:
        grade.append("F")

    if td_diff <= -0.8:
        grade.append("A")
    elif td_diff >= -0.7 and td_diff <= -0.3:
        grade.append("B")
    elif td_diff >= -0.2 and td_diff <= 0.2:
        grade.append("C")
    elif td_diff >= 0.3 and td_diff <= 0.7:
        grade.append("D")
    else:
        grade.append("F")

    if int_diff >= 0.5:
        grade.append("A")
    elif int_diff >= 0.2 and int_diff <= 0.4:
        grade.append("B")
    elif int_diff >= -0.1 and int_diff <= 0.1:
        grade.append("C")
    elif int_diff >= -0.4 and int_diff <= -0.2:
        grade.append("D")
    elif int_diff <= -0.5:
        grade.append("F")

    if sack_diff >= 0.8:
        grade.append("A")
    elif sack_diff >= 0.3 and sack_diff <= 0.7:
        grade.append("B")
    elif sack_diff >= -0.2 and sack_diff <= 0.2:
        grade.append("C")
    elif sack_diff >= -0.7 and sack_diff <= -0.3:
        grade.append("D")
    elif sack_diff <= -0.8:
        grade.append("F")

    if comp_diff <= -4.2:
        grade.append("A")
    elif comp_diff >= -4.2 and comp_diff <= -2.1:
        grade.append("B")
    elif comp_diff >= -2 and comp_diff <= 2:
        grade.append("C")
    elif comp_diff >= 2.1 and comp_diff <= 4.1:
        grade.append("D")
    elif comp_diff >= 4.2:
        grade.append("F")

    return players_dict


def display_grades(name, grades_result):
    """
    The display_grades function shows the grades for the performance
    of the quarterback the user just entered in relation to the
    average values of last year.
    """
    yards_grade = grades_result[name]["grades"][0]
    efficency_grade = grades_result[name]["grades"][4]
    td_grade = grades_result[name]["grades"][1]
    int_grade = grades_result[name]["grades"][2]
    sack_grade = grades_result[name]["grades"][3]

    print("################\n")
    print("For the season performance registered so far, \n"
          f"{name} receives the following grades: \n")
    print(f"Passing yards: {yards_grade}")
    print(f"Efficency / completion percentage: {efficency_grade}")
    print(f"Touchdowns: {td_grade}")
    print(f"Interceptions: {int_grade}")
    print(f"Sacks: {sack_grade}\n")


def generate_leaderboard(players_dict):
    """
    The generate_leaderboard function takes the player_dict
    (without grades) as an argument and only runs, if there are two or
    more players in the database.
    It gets the average yards, touchdowns and interceptions and generates
    a score with these values. After that, a leaderboard dict is created
    with the players name as the key and the score as the value. The
    function returns the leaderboard.
    """
    if len(players_dict) >= 2:
        for player in players_dict:
            float_stats = [float(x.replace(',', '.')) for x
                           in players_dict[player]["stats"]]
            yards = float_stats[0]
            tds = float_stats[1]
            ints = float_stats[2]
            calculated_score = ((tds * 2) - ints) * yards
            rounded_score = round(calculated_score, 1)
            players_dict[player]["score"] = rounded_score

        leaderboard = {}
        for player in players_dict:
            individual_score = {player: players_dict[player]["score"]}
            leaderboard.update(individual_score)
        return leaderboard


def display_leaderboard(leaderboard):
    """
    The display_leaderboard function takes the dict leaderboard
    as an argument and sorts it from highest to lowest score, then displays it.
    """
    if leaderboard:
        print("################\n")
        print("The most productive QBs are in descending order: \n")
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda
                                    x: x[1], reverse=True)
        for entry in sorted_leaderboard:
            print(f"{entry[0]}: {entry[1]}")


def add():
    """
    The add function is the last function to call and it asks
    the user, if he / she would like to continue with the QPA.
    If so, the main function gets called again, otherwise the user
    exits the application.
    """
    while True:
        print("\nDo you want to add another statistic?")
        response = input("Enter y for yes or n for no: \n")
        if response == 'y':
            main()
            break
        elif response == 'n':
            print("\nThanks for updating your gameday statistics on QPA.")
            print("See you next weekend!")
            quit()
            break
        else:
            print("Please enter y or n")
            response = input("Enter y for yes or n for no: \n")


def main():
    """
    This function calls all necessary functions in the right order,
    according to the flow chart in the doc.
    """
    name = get_quarterback()
    gameday = get_gameday()
    new_entry = check(name, gameday)
    values = value_block()
    save(new_entry, values)
    calculate_averages(name)
    calculate_efficency()
    players_dict = compare()
    grades_result = rate(name, players_dict)
    display_grades(name, grades_result)
    leaderboard = generate_leaderboard(players_dict)
    display_leaderboard(leaderboard)
    add()


start()
main()
