# compilation with auto-py-to-exe (as admin)
#  C:\Users\Giacomo\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe --noconfirm --onefile --console --paths "." --name "AR kwire placement test companion" --icon ".\media\icon.ico" "main.py"

import time
import signal
from datetime import datetime
import pyperclip

from logger import logger
from __init__ import *
import db
import data

ci = custom_input()

def main():
    def handler(signum, frame):
        logger.info("\nexiting. DATA NOT SAVED!")
        exit(0)
    signal.signal(signal.SIGINT, handler)

    logger.info(f"# POSITIONING TEST COMPANION ({version})")
    logger.info(f"# What a beautiful day to stick some anti-pigeon spikes into plastic!\n")

    TEST_data = TEST()

    # save on db at the end
    db.db_save(TEST_data)

    # save on fusion360 to import strings at the end
    with open("logs/fusion_TOIMPORT.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        for s in data.fusion360_imports:
            f.write(s+"\n")

    logger.info("bye!")

def TEST():
    "TEST performs 3 ECPs with multiple PA"

    id = db.db_newid(3)

    logger.info(f"# BEGIN POSITIONING TEST FOR A CANDIDATE, ONE SINGLE PHASE ({id})")    
    logger.info(f"# {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')}")

    logger.info("DATA COLLECTION")
    while True:
        TEST_data = data.TESTdata(
            id=id,
            ECP_ids=[],          # to update
            PA_ids=[],           # to update
            comment="",
            datatype="TEST",
            time_init=time.time(),
            phase=               ci.int(" |-- phase [INTEGER]:               ", 0, 10),
            phantom_id=          ci.str(" |-- phantom id [STRING]:           ", 2),
            name=                ci.str(" |-- name [STRING]:                 "),
            surname=             ci.str(" |-- surname [STRING]:              "),
            gender=              ci.acc(" |-- gender [M/F]:                  ", ["m", "f"]).upper(),
            right_handed=        ci.boo(" |-- right-handed [Y/N]:            "),
            age=                 ci.int(" |-- age [INTEGER]:                 ", 0, 99),
            medicine_surge_year= ci.int(" |-- medsurg year [INTEGER]:        ", 0, 7),
            specialization_year= ci.int(" |-- specialization year [INTEGER]: ", 0, 6),
            num_operations=      ci.int(" |-- operations count [INTEGER]:    ", 0, 1000),
            TEST_D=0.0,        # to update
            TEST_RPC=0,        # to update
            TEST_RESD=0.0,     # to update
            TEST_PAC=0,        # to update
            TEST_PACF=0,       # to update
            TEST_ECPC=0,       # to update
        )
        if ci.boo("\tTECHNICAL:\t is data entered correct? [Y/N]: "):
            break

    for ECP_number in range(1, len(data.TEST_design)+1):
        ECP_data = ECP(TEST_data.phase, TEST_data.id, ECP_number)

        # add ECP_data to ECPs
        data.ECPs_toinsert.append(ECP_data)

        # update test_data
        TEST_data.TEST_D    += ECP_data.ECP_D
        TEST_data.TEST_RPC  += ECP_data.ECP_RPC
        TEST_data.TEST_RESD += ECP_data.ECP_RESD
        TEST_data.TEST_PAC  += ECP_data.ECP_PAC
        TEST_data.TEST_PACF += ECP_data.ECP_PACF
        TEST_data.TEST_ECPC  = ECP_number
        TEST_data.ECP_ids.append(ECP_data.id)
        TEST_data.PA_ids.extend(ECP_data.PA_ids)
    
    TEST_data.comment = ci.str(f"\tTECHNICAL:\t comment on TEST ({id}) [STRING]: ")

    return TEST_data

def ECP(phase, TEST_id, ECP_number) -> data.ECPdata:
    "ECP performs single ECP with multiple PA"

    id = db.db_newid(4)
    logger.info(f"\n########################")
    logger.info(f"ECP{ECP_number} START! ({id})")

    ECP_data = data.ECPdata(
        TEST_id=TEST_id,
        PA_ids=[],       # update for each PA
        id=id,
        datatype="ECP",
        time_init=time.time(),
        ease_of_placement=-1, # input at the end
        phase=phase,
        ECP_number=ECP_number,
        ECP_D=0.0,       # update for each PA
        ECP_RPC=0,       
        ECP_RESD=0.0,    # update for each PA
        ECP_PAC=0,       # update for each PA
        ECP_PACF=0       # update for each PA
    )

    PA_number = 0
    while True:
        PA_number += 1
        PA_data = PA(phase, TEST_id, ECP_number, ECP_data.id, PA_number)

        # add PA_data to PAs
        data.PAs_toinsert.append(PA_data)

        # update ECP_data
        ECP_data.ECP_D += PA_data.PA_D
        ECP_data.ECP_RPC += PA_data.PA_RPC
        ECP_data.ECP_RESD += PA_data.PA_RESD
        ECP_data.ECP_PAC = PA_number
        ECP_data.ECP_PACF += 0 if PA_data.success else 1
        ECP_data.PA_ids.append(PA_data.id)
        
        if PA_data.success:
            break
    
    logger.info(f"DATA COLLECTION - ECP{ECP_number} - ({id})")

    # after multiple PA now the k-wire is in the estimated correct position
    ECP_data.ease_of_placement=ci.int(" |-- ease of placement [0 difficult - 5 easy]: ", min=0, max=5)
    
    return ECP_data
      
def PA(phase: int, test_id: str, ECP_number: int, ECP_id: str, PA_number: int) -> data.PAdata:
    "PA performs single PA"

    id = db.db_newid(5)
    logger.info(f"\n------------------------")
    logger.info(f"PA{ECP_number}.{PA_number} START! ({id})")
    ci.str("PERFORM:\t reset x-ray machine [ENTER when done]: ")
    ci.str("PERFORM:\t give instruction to insert K-wire [ENTER when instruction given]: ")

    chrono = chronometer()
    time_init = chrono.start()

    # insertion of K-wire
    i = ci.acc("CANDIDATE:\t inserting K-wire... -> checks it and declares it failed [f] or successful [s]: ", ["f", "s"])
    if i.lower() == 'f': # PA FAILED
        logger.info("\t\t \_candidate has FAILED positioning attempt!")
        success = False
    elif i.lower() == 's': # PA SUCCESS
        logger.info("\t\t \_candidate has performed SUCCESSFUL positioning attempt!")
        success = True
    
    # get PA data
    chrono.pause()
    logger.info(f"DATA COLLECTION - PA{ECP_number}.{PA_number} - ({id})")

    while True:
        PA_data = data.PAdata(
            TEST_id=test_id,
            ECP_id=ECP_id,
            id=id,
            comment="",
            datatype="PA",
            time_init=time_init,
            phase=phase,
            ECP_number=ECP_number,
            PA_number=PA_number,
            success=success,
            PA_D=-1.0, # set after K-wire extraction
            PA_RPC =ci.int(" |-- RADIATION picture count       [INT]  : ", min=0),
            PA_RESD=ci.flo(" |-- RADIATION entrance skin dose  [FLOAT]: "),
            PA_RDAP=ci.flo(" |-- RADIATION dose-area product   [FLOAT]: "),
            PA_RmAs=ci.flo(" |-- RADIATION milliampere-seconds [FLOAT]: "),
            PA_RkVp=ci.flo(" |-- RADIATION kilovoltage peak    [FLOAT]: "),
            P1A=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: "),
            P1B=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: "),
            P1C=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: "),
            P1D=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: "),
            P2A=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: "),
            P2B=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: "),
            P2C=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: "),
            P2D=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: "),
            confidence_position= ci.flo(" |-- CANDIDATE: confidence on entrance position in mm? [FLOAT]: ", min=0),
            confidence_angle=    ci.flo(" |-- CANDIDATE: confidence on angle in deg? [FLOAT]:            ", min=0),
            estimate_hit=        ci.boo(" |-- CANDIDATE: estimate structures hit [Y/N]?:                 "),
            ktarget=data.TEST_design[ECP_number-1].ktarget,
            markers=data.TEST_design[ECP_number-1].markers,
            anatomy=data.TEST_design[ECP_number-1].anatomy,
            fusion_computed=False,
            angle_kPA_ktarget=-1.0,
            distance_ep_kPA_ktarget=-1.0,
            distance_ep_kPA_ktarget_X=-1.0,
            distance_ep_kPA_ktarget_Y=-1.0,
            distance_ep_kPA_ktarget_Z=-1.0,
            delta_id_kPA_ktarget=-1.0
        )
        if ci.boo("\tTECHNICAL:\t is data entered correct? [Y/N]: "):
            break
    
    # send to fusion 360 for computation
    PA_data_str = PA_data.dumps()
    pyperclip.copy(PA_data_str)
    logger.info(f"PERFORM:\t test following string on fusion 360 (already copied in clipboard) -> \n{PA_data_str}")
    data.fusion360_imports.append(PA_data_str)

    # receive from fusion 360
    PA_data = ci.PAdata_computed(f"PERFORM:\t enter data from fusion 360: ", PA_data.id)
    
    # K-wire extraction of PA
    ci.str("PERFORM:\t give instruction to extract K-wire [ENTER when instruction given]: ")
    chrono.start()
    ci.str("CANDIDATE:\t extracting the K-wire... [ENTER when done]: ")
    PA_data.PA_D = chrono.reset()

    PA_data.comment = ci.str(f"\tTECHNICAL:\t comment on PA ({id}) [STRING]: ")

    logger.info(f"PA{ECP_number}.{PA_number} FINISHED!")
    return PA_data
    
if __name__ == "__main__":
    main()