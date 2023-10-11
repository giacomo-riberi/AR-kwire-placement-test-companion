import sqlite3
import time
import secrets
import re

conn = sqlite3.connect('positioning_test_data.db') # Create a connection to the SQLite database (or create it if it doesn't exist)
cursor = conn.cursor() # Create a cursor object to interact with the database

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
        test id TEXT,
        ECP id TEXT
    )''')

conn.commit()
conn.close()

########## TODO ##########
# make logging system
##########################

test_data = {}
ECPs = []
PAs = []


def main():
    print("# BEGIN POSITIONING TEST #\n")
    
    print("DATA COLLECTION")
    test_data = {
        "id": secrets.token_hex(3),
        "time_init": time.time(),
        "phase":                custom_input(" ├-- phase [INTEGER]: ", "INTEGER"),
        "gender":               custom_input(" ├-- gender [M/F]: ", ["m", "f"]).upper(),
        "age":                  custom_input(" ├-- age [INTEGER]: ", "INTEGER"),
        "specialization_year":  custom_input(" ├-- year of specialization [INTEGER]: ", "INTEGER"),
        "num_operations":       custom_input(" ├-- number of operations [INTEGER]: ", "INTEGER"),
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
        test_data["PA_ids"].append([PA_id for PA_id in ECP_data["PA_ids"]])
        test_data["ECP_ids"].append(ECP_data["id"])

# ECP performs single ECP with multiple PA
def ECP(phase, test_id, ECP_number):
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
        ECP_data["ECP_PACF"] += [0 if PA_data["PA_success"] else 1]
        ECP_data["PA_ids"].append(PA_data["id"])
        
        if PA_data["PA_success"]:
            break
        PA_number += 1
    
    return ECP_data
    
    
# ECP performs single PA
def PA(phase, test_id, ECP_number, ECP_id,  PA_number):
    PA_data = {}

    input("PERFORM:\t reset x-ray machine [ENTER]: ")
    PAD_init = time.time()

    PA = {}
    user_input = custom_input("CANDIDATE:\t insert K-wire, checks it and declares it failed[f] or successful[s]: ", ["f", "s"])
    
    # PA FAILED
    if user_input.lower() == 'f':
        print("\t\t └-candidate has FAILED positioning attempt!")
        PA_data["PA_success"] = False

        input("CANDIDATE: remove the K-wire [ENTER]: ")
    
    # PA SUCCESS
    elif user_input.lower() == 's':
        print("\t\t └-candidate has performed SUCCESSFUL positioning attempt!")
        PA_data["PA_success"] = True
    

    print(f"DATA COLLECTION - PA{ECP_number}.{PA_number} finished")
    PA_data["id"] = secrets.token_hex(3)
    PA_data["time_init"] = time.time()
    PA_data["phase"] = phase
    PA_data["ECP_number"] = ECP_number
    PA_data["PA_number"] = PA_number
    # PA_data["PA_success"] -> already set
    PA_data["PAD"] = time.time() - PAD_init
    PA_data["PAR"] = custom_input(" ├-- positioning attempt RADIATION [FLOAT]: ", "FLOAT")
    PA_data["P1A"] = custom_input(" ├-- P1A [FLOAT]: ", "FLOAT")
    PA_data["P1B"] = custom_input(" ├-- P1B [FLOAT]: ", "FLOAT")
    PA_data["P1C"] = custom_input(" ├-- P1C [FLOAT]: ", "FLOAT")
    PA_data["P1D"] = custom_input(" ├-- P1D [FLOAT]: ", "FLOAT")
    PA_data["P2A"] = custom_input(" ├-- P2A [FLOAT]: ", "FLOAT")
    PA_data["P2B"] = custom_input(" ├-- P2B [FLOAT]: ", "FLOAT")
    PA_data["P2C"] = custom_input(" ├-- P2C [FLOAT]: ", "FLOAT")
    PA_data["P2D"] = custom_input(" ├-- P2D [FLOAT]: ", "FLOAT")
    PA_data["test_id"] = test_id
    PA_data["ECP_id"] = ECP_id
    
    return PA_data

#  custom_input behaves like input but continues to prompt the user until the input matches one of the accepted values
def custom_input(prompt, accepted_values):
    while True:
        user_input = input(prompt).strip().lower()  
        if user_input == "":
            continue
        if user_input in accepted_values:
            return user_input
        elif accepted_values == "INTEGER" and user_input.isdigit():
            return user_input
        elif accepted_values == "FLOAT" and (user_input.isdigit() or re.match(r'^-?\d+(?:\.\d+)$', user_input) != None):
            return user_input


if __name__ == "__main__":
    main()