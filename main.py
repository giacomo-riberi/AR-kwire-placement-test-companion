import sqlite3
import time
import secrets
import sys, traceback

from tools import custom_input, chronometer

version = "v1.0"

########## TODO ##########
# make logging system
##########################

ECPs = []
PAs = []

def main():
    print(f"# POSITIONING TEST COMPANION ({version}) #\n")

    TEST_data = TEST()

    save_db(TEST_data)

    print("bye!")


def save_db(TEST_data):
    "save_db saves data on database"

    global ECPs, PAs

    def printExcept(er):
        "printExcept prints logs generated in the try-except block"

        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    # create database tables
    try:
        conn = sqlite3.connect(f'positioning_test_data-({version}).db') # Create a connection to the SQLite database (or create it if it doesn't exist)
        cursor = conn.cursor() # Create a cursor object to interact with the database

        # create TEST table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TEST (
                id TEXT NOT NULL PRIMARY KEY,
                time_init REAL,
                phase INTEGER,
                gender TEXT,
                age INTEGER,
                specialization_year TEXT,
                num_operations INTEGER,
                test_duration REAL,
                test_radiation REAL,
                test_PAC INTEGER,
                test_PACF INTEGER,
                test_ECPC INTEGER,
                PA_ids TEXT,
                ECP_ids TEXT
            )''')

        # create ECP table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ECP (
                id TEXT NOT NULL PRIMARY KEY,
                time_init REAL,
                phase INTEGER,
                ECP_number INTEGER,
                ECPD REAL,
                ECPR REAL,
                ECP_PAC INTEGER,
                ECP_PACF INTEGER,
                test_id TEXT,
                PA_ids TEXT
            )''')

        # create PA table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PA (
                id TEXT NOT NULL PRIMARY KEY,
                time_init REAL,
                phase INTEGER,
                ECP_number INTEGER,
                PA_number INTEGER,
                PA_success BOOL,
                PAD REAL,
                PAR REAL,
                P1A REAL,
                P1B REAL,
                P1C REAL,
                P1D REAL,
                P2A REAL,
                P2B REAL,
                P2C REAL,
                P2D REAL,
                test_id TEXT,
                ECP_id TEXT
            )''')

        conn.commit()
    except sqlite3.Error as er:
        printExcept(er)
        sys.exit()
    
    ### DON'T COMMIT UNTIL ALL INSERTIONS ARE DONE! ###

    # insert TEST_data into database
    try:
        cursor.execute('''
            INSERT INTO TEST (
                id,
                time_init,
                phase,
                gender,
                age,
                specialization_year,
                num_operations,
                test_duration,
                test_radiation,
                test_PAC,
                test_PACF,
                test_ECPC,
                PA_ids,
                ECP_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (  TEST_data['id'],
                TEST_data['time_init'],
                TEST_data['phase'],
                TEST_data['gender'],
                TEST_data['age'],
                TEST_data['specialization_year'],
                TEST_data['num_operations'],
                TEST_data['test_duration'],
                TEST_data['test_radiation'],
                TEST_data['test_PAC'],
                TEST_data['test_PACF'],
                TEST_data['test_ECPC'],
                ",".join(TEST_data['PA_ids']),
                ",".join(TEST_data['ECP_ids'])))
    except sqlite3.Error as er:
        printExcept(er)
        sys.exit()
    
    # insert ECPs into database
    for ECP_data in ECPs:
        try:
            cursor.execute('''
                INSERT INTO ECP (
                    id,
                    time_init,
                    phase,
                    ECP_number,
                    ECPD,
                    ECPR,
                    ECP_PAC,
                    ECP_PACF,
                    test_id,
                    PA_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (  ECP_data['id'],
                    ECP_data['time_init'],
                    ECP_data['phase'],
                    ECP_data['ECP_number'],
                    ECP_data['ECPD'],
                    ECP_data['ECPR'],
                    ECP_data['ECP_PAC'],
                    ECP_data['ECP_PACF'],
                    ECP_data['test_id'],
                    ",".join(ECP_data['PA_ids'])))
        except sqlite3.Error as er:
            printExcept(er)
            sys.exit()

    # insert PAs into database
    for PA_data in PAs:
        try:
            cursor.execute('''
                INSERT INTO PA (
                    id,
                    time_init,
                    phase,
                    ECP_number,
                    PA_number,
                    PA_success,
                    PAD,
                    PAR,
                    P1A,
                    P1B,
                    P1C,
                    P1D,
                    P2A,
                    P2B,
                    P2C,
                    P2D,
                    test_id,
                    ECP_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (  PA_data["id"],
                    PA_data["time_init"],
                    PA_data["phase"],
                    PA_data["ECP_number"],
                    PA_data["PA_number"],
                    PA_data["PA_success"],
                    PA_data["PAD"],
                    PA_data["PAR"],
                    PA_data["P1A"],
                    PA_data["P1B"],
                    PA_data["P1C"],
                    PA_data["P1D"],
                    PA_data["P2A"],
                    PA_data["P2B"],
                    PA_data["P2C"],
                    PA_data["P2D"],
                    PA_data["test_id"],
                    PA_data["ECP_id"]))
        except sqlite3.Error as er:
            printExcept(er)
            sys.exit()
        
    conn.commit()
    conn.close()
    print("SAVED ON DATABASE!")


def TEST():
    "TEST performs 3 ECPs with multiple PA"

    global ECPs

    print("# BEGIN POSITIONING TEST FOR A CANDIDATE (ONE SINGLE PHASE) #\n")

    print("DATA COLLECTION")
    test_data = {
        "id": secrets.token_hex(3),
        "time_init": time.time(),
        "phase":                custom_input(" |-- phase [INTEGER]: ", "INTEGER"),
        "gender":               custom_input(" |-- gender [M/F]: ", ["m", "f"]).upper(),
        "age":                  custom_input(" |-- age [INTEGER]: ", "INTEGER"),
        "specialization_year":  custom_input(" |-- year of specialization [INTEGER]: ", "INTEGER"),
        "num_operations":       custom_input(" |-- number of operations [INTEGER]: ", "INTEGER"),
        "test_duration": 0.0,   # to update
        "test_radiation": 0.0,  # to update
        "test_PAC": 0,          # to update
        "test_PACF": 0,         # to update
        "test_ECPC": 0,         # to update
        "PA_ids": [],           # to update
        "ECP_ids": []           # to update
    }

    for ECP_number in range(1, 4):
        ECP_data = ECP(test_data["phase"], test_data["id"], ECP_number)

        # add ECP_data to ECPs
        ECPs.append(ECP_data)

        # update test_data
        test_data["test_duration"]  += ECP_data["ECPD"]
        test_data["test_radiation"] += ECP_data["ECPR"]
        test_data["test_PAC"]       += ECP_data["ECP_PAC"]
        test_data["test_PACF"]      += ECP_data["ECP_PACF"]
        test_data["test_ECPC"]       = ECP_number
        test_data["PA_ids"].extend(ECP_data["PA_ids"])
        test_data["ECP_ids"].append(ECP_data["id"])

    return test_data

def ECP(phase, test_id, ECP_number):
    "ECP performs single ECP with multiple PA"

    global PAs

    ECP_data = {
        "id": secrets.token_hex(3),
        "time_init": time.time(),
        "phase": phase,
        "ECP_number": ECP_number,
        "ECPD": 0.0,        # to update
        "ECPR": 0.0,        # to update
        "ECP_PAC": 0,       # to update
        "ECP_PACF": 0,      # to update
        "test_id": test_id,
        "PA_ids": []        # to update
    }

    PA_number = 1
    while True:
        PA_data = PA(phase, test_id, ECP_number, ECP_data["id"], PA_number)

        # add PA_data to PAs
        PAs.append(PA_data)

        # update ECP_data
        ECP_data["ECPD"] += PA_data["PAD"]
        ECP_data["ECPR"] += PA_data["PAR"]
        ECP_data["ECP_PAC"] = PA_number
        ECP_data["ECP_PACF"] += 0 if PA_data["PA_success"] else 1
        ECP_data["PA_ids"].append(PA_data["id"])
        
        if PA_data["PA_success"]:
            break
        PA_number += 1
    
    return ECP_data
    
    
def PA(phase, test_id, ECP_number, ECP_id, PA_number):
    "PA performs single PA"

    def terminatePA(PA_success: bool):
        "terminatePA terminates PA, performs data extraction and candidate extracts K-wire"

        chrono.pause() # pause chronometer to get data
        print(f"DATA COLLECTION - PA{ECP_number}.{PA_number}")
        PA_data["id"] = secrets.token_hex(3)
        PA_data["time_init"] = PAD_init
        PA_data["phase"] = phase
        PA_data["ECP_number"] = ECP_number
        PA_data["PA_number"] = PA_number
        PA_data["PA_success"] = PA_success
        # PA_data["PAD"] # set after K-wire extraction
        PA_data["PAR"] = custom_input(" |-- positioning attempt RADIATION [FLOAT]: ", "FLOAT")
        PA_data["P1A"] = custom_input(" |-- P1A [FLOAT]: ", "FLOAT")
        PA_data["P1B"] = custom_input(" |-- P1B [FLOAT]: ", "FLOAT")
        PA_data["P1C"] = custom_input(" |-- P1C [FLOAT]: ", "FLOAT")
        PA_data["P1D"] = custom_input(" |-- P1D [FLOAT]: ", "FLOAT")
        PA_data["P2A"] = custom_input(" |-- P2A [FLOAT]: ", "FLOAT")
        PA_data["P2B"] = custom_input(" |-- P2B [FLOAT]: ", "FLOAT")
        PA_data["P2C"] = custom_input(" |-- P2C [FLOAT]: ", "FLOAT")
        PA_data["P2D"] = custom_input(" |-- P2D [FLOAT]: ", "FLOAT")
        PA_data["test_id"] = test_id
        PA_data["ECP_id"] = ECP_id
        chrono.start() # start chronometer to include also extraction time in PA

        input("CANDIDATE: extract the K-wire [ENTER when done]: ")
        PA_data["PAD"] = chrono.reset()

    PA_data = {}

    print(f"\n------------------------\nPA{ECP_number}.{PA_number} START!")
    input("PERFORM:\t reset x-ray machine [ENTER]: ")
    
    chrono = chronometer()
    PAD_init = chrono.start()

    user_input = custom_input("CANDIDATE:\t insert K-wire, checks it and declares it failed[f] or successful[s]: ", ["f", "s"])
    
    # PA FAILED
    if user_input.lower() == 'f':
        print("\t\t |-candidate has FAILED positioning attempt!")
        terminatePA(False)
    
    # PA SUCCESS
    elif user_input.lower() == 's':
        print("\t\t |-candidate has performed SUCCESSFUL positioning attempt!")
        terminatePA(True)
    
    return PA_data

if __name__ == "__main__":
    main()