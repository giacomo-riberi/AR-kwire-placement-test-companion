import time
import signal
from datetime import datetime

from utils.utils import logger, chronometer
from __init__ import *
import db

def main():
    def handler(signum, frame):
        logger.info("\nexiting. DATA NOT SAVED!")
        exit(0)
    signal.signal(signal.SIGINT, handler)

    logger.info(f"# POSITIONING TEST COMPANION ({version}) #\n")

    TEST_data = TEST()

    db.db_save(TEST_data)

    logger.info("bye!")

def TEST():
    "TEST performs 3 ECPs with multiple PA"

    global ECPs

    logger.info("# BEGIN POSITIONING TEST FOR A CANDIDATE (ONE SINGLE PHASE) #\n")    

    logger.info(f"# {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')} #")

    logger.info("DATA COLLECTION")
    test_data = {
        "id": db.db_newid(3),
        "datatype": "test",
        "time_init": time.time(),
        "phase":                ci.int(" |-- phase [INTEGER]:               "),
        "name":                 ci.str(" |-- name [STRING]:                 "),
        "surname":              ci.str(" |-- surname [STRING]:              "),
        "gender":               ci.acc(" |-- gender [M/F]:                  ", ["m", "f"]).upper(),
        "age":                  ci.int(" |-- age [INTEGER]:                 "),
        "specialization_year":  ci.int(" |-- specialization year [INTEGER]: "),
        "num_operations":       ci.int(" |-- operations count [INTEGER]:    "),
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
        "id": db.db_newid(4),
        "datatype": "ecp",
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

    chrono = chronometer()

    def terminatePA(PA_success: bool):
        "terminatePA terminates PA, performs data extraction and candidate extracts K-wire"

        chrono.pause() # pause chronometer to get data
        logger.info(f"DATA COLLECTION - PA{ECP_number}.{PA_number}")
        PA_data = {
            "id": db.db_newid(5),
            "datatype": "pa",
            "time_init": time_init,
            "phase": phase,
            "ECP_number": ECP_number,
            "PA_number": PA_number,
            "PA_success": PA_success,
            # "PAD", # set after K-wire extraction
            "PAR": ci.flo(" |-- positioning attempt RADIATION [FLOAT]: "),
            "P1A": ci.flo(" |-- P1A [FLOAT]: "),
            "P1B": ci.flo(" |-- P1B [FLOAT]: "),
            "P1C": ci.flo(" |-- P1C [FLOAT]: "),
            "P1D": ci.flo(" |-- P1D [FLOAT]: "),
            "P2A": ci.flo(" |-- P2A [FLOAT]: "),
            "P2B": ci.flo(" |-- P2B [FLOAT]: "),
            "P2C": ci.flo(" |-- P2C [FLOAT]: "),
            "P2D": ci.flo(" |-- P2D [FLOAT]: "),
            "test_id": test_id,
            "ECP_id": ECP_id
        }

        # time also extraction time of K-wire in PA
        ci.all("PERFORM:\t give instruction to extract K-wire [ENTER when instruction given]: ")
        chrono.start()
        ci.all("CANDIDATE:\t extracting the K-wire... [ENTER when done]: ")
        PA_data["PAD"] = chrono.reset()
        logger.info(f"PA{ECP_number}.{PA_number} FINISHED!")
        return PA_data

    logger.info(f"\n------------------------")
    logger.info(f"PA{ECP_number}.{PA_number} START!")
    ci.all("PERFORM:\t reset x-ray machine [ENTER when done]: ")
    ci.all("PERFORM:\t give instruction to insert K-wire [ENTER when instruction given]: ")
    time_init = chrono.start()

    i = ci.acc("CANDIDATE:\t inserting K-wire... -> checks it and declares it failed [f] or successful [s]: ", ["f", "s"])
    if i.lower() == 'f': # PA FAILED
        logger.info("\t\t |-candidate has FAILED positioning attempt!")
        return terminatePA(False)
    elif i.lower() == 's': # PA SUCCESS
        logger.info("\t\t |-candidate has performed SUCCESSFUL positioning attempt!")
        return terminatePA(True)
    
if __name__ == "__main__":
    main()