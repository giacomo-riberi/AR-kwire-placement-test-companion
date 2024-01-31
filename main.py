# compilation with auto-py-to-exe (as admin)
#  C:\Users\Giacomo\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe --noconfirm --onefile --console --paths "." --name "AR kwire placement test companion" --icon ".\media\icon.ico" "main.py"

import sys
import time
import signal
from datetime import datetime
import pyperclip
import textwrap

from logger import logger
from __init__ import *
import db
import data

ci = custom_input()

def checkargv():
    logger.info(f"flags: {sys.argv[1:]}")

    if len(sys.argv) <= 1:
        return
        
    if "--testdb" in sys.argv:
        data.TEST_toinsert = data.TESTdata(datatype="--testdb")
        data.ECPs_toinsert.append(data.ECPdata(datatype="--testdb"))
        data.PAs_toinsert.append(data.PAdata(datatype="--testdb"))

        db.db_save()
        print(f"now check database and delete \"--testdb\" datatype entries")
    else:
        print(f"unknown flags")
    quit()

def main():
    checkargv()

    def handler(signum, frame):
        logger.info("\nexiting. DATA NOT SAVED!")
        exit(0)
    signal.signal(signal.SIGINT, handler)

    logger.info(f"# POSITIONING TEST COMPANION ({version})")
    logger.info(f"# What a beautiful day to stick some anti-pigeon spikes into plastic!\n")

    data.TEST_toinsert = TEST()

    # save on db at the end
    db.db_save()

    # save on fusion360 to import data
    with open("logs/fusion360_imports.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {version}\n")
        for s in data.fusion360_imports:
            f.write(s+"\n")
    
    # save on companion to import data
    with open("logs/companion_imports.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {version}\n")
        for s in data.companion_imports:
            f.write(s+"\n")

    logger.info("bye!")

def TEST():
    "TEST performs 3 ECPs with multiple PA"

    id = db.db_newid(3)

    logger.info(f"# BEGIN POSITIONING TEST FOR A CANDIDATE, ONE SINGLE PHASE ({id})")
    logger.info(f"# {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')}")

    logger.info(f"DATA COLLECTION - TEST - ({id})")
    while True:
        TEST_data = data.TESTdata(
            id=id,
            ECP_ids=[],          # to update
            PA_ids=[],           # to update
            comment="",
            datatype="TEST",
            time_init=time.time(),
            phase=               ci.int(" |-- phase [INTEGER]:                ", 0, 9),
            phantom_id=          ci.str(" |-- phantom id [STRING]:            ", 2),
            name=                ci.str(" |-- name [STRING]:                  "),
            surname=             ci.str(" |-- surname [STRING]:               "),
            gender=              ci.acc(" |-- gender [M/F]:                   ", ["m", "f"]),
            right_handed=        ci.boo(" |-- right-handed [Y/N]:             "),
            age=                 ci.int(" |-- age [INTEGER]:                  ", 0, 99),
            medicine_surge_year= ci.int(" |-- medsurg year        [-1 : 6]:   ", -1, 6),
            specialization_year= ci.int(" |-- specialization year [-1 : 5]:   ", -1, 5),
            surgeon_year=        ci.int(" |-- surgeon year        [-1 : 100]: ", -1, 100),
            exp_operation_count= ci.int(" |-- exp operation count [INTEGER]:  ", 0, 1000),
            glasses=             ci.boo(" |-- glasses [Y/N]:                  "),
            glasses_type=        ci.acc(" |-- glasses type [None [] / Myopia (Nearsightedness) [M] / Hyperopia (Farsightedness) [H] / Astigmatism [AS] / Presbyopia [P] / Strabismus [S] / Amblyopia (Lazy Eye) [AM] / Cataract [C]: ", ["", "m", "h", "as", "p", "s", "am", "c"]),
            glasses_power=       ci.flo(" |-- glasses power [-1 : 100]:       ", -1, 100),
            exp_vr=              ci.int(" |-- exp Virtual Reality   [0 : 5]:  ", 0, 5),
            exp_ar=              ci.int(" |-- exp Augmented Reality [0 : 5]:  ", 0, 5),
            exp_3D_editor=       ci.int(" |-- exp 3D editors        [0 : 5]:  ", 0, 5),

            realism_xray=       -1.0,   # update post test
            realism_ar=         -1.0,   # update post test
            realism_phantom=    -1.0,   # update post test

            sim_quality_xray=   -1.0,   # update post test
            sim_quality_ar=     -1.0,   # update post test
            sim_quality_phantom=-1.0,   # update post test

            comfort_xray=       -1.0,   # update post test
            comfort_ar=         -1.0,   # update post test

            TEST_D=             0,   # update after each ECP
            TEST_RPC=           0,     # update after each ECP
            TEST_PAC=           0,     # update after each ECP
            TEST_PACF=          0,     # update after each ECP
            TEST_ECPC=          0,     # update after each ECP
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
        TEST_data.TEST_PAC  += ECP_data.ECP_PAC
        TEST_data.TEST_PACF += ECP_data.ECP_PACF
        TEST_data.TEST_ECPC  = ECP_number
        TEST_data.ECP_ids.append(ECP_data.id)
        TEST_data.PA_ids.extend(ECP_data.PA_ids)
    
    logger.info(f"DATA COLLECTION - TEST - ({id})")
    TEST_data.realism_xray=       ci.int(" |-- realism xray    [-1 : 5]:            ", -1, 5)
    TEST_data.realism_ar=         ci.int(" |-- realism AR      [-1 : 5]:            ", -1, 5)
    TEST_data.realism_phantom=    ci.int(" |-- realism phantom [-1 : 5]:            ", -1, 5)

    TEST_data.sim_quality_xray=   ci.int(" |-- simulation quality xray    [-1 : 5]: ", -1, 5)
    TEST_data.sim_quality_ar=     ci.int(" |-- simulation quality AR      [-1 : 5]: ", -1, 5)
    TEST_data.sim_quality_phantom=ci.int(" |-- simulation quality phantom [-1 : 5]: ", -1, 5)

    TEST_data.comfort_xray=       ci.int(" |-- comfort xray [-1 : 5]:               ", -1, 5)
    TEST_data.comfort_ar=         ci.int(" |-- comfort ar   [-1 : 5]:               ", -1, 5)
    
    TEST_data.comment = ci.str(f"\tTECHNICAL:\t comment on TEST ({id}) [STRING]: ")

    # print input-ready stats for next phase round with same candidate
    print(textwrap.dedent(f"""
    {TEST_data.phase}
    {TEST_data.phantom_id}
    {TEST_data.name}
    {TEST_data.surname}
    {TEST_data.gender}
    {TEST_data.right_handed}
    {TEST_data.age}
    {TEST_data.medicine_surge_year}
    {TEST_data.specialization_year}
    {TEST_data.surgeon_year}
    {TEST_data.exp_operation_count}
    {TEST_data.glasses}
    {TEST_data.glasses_type}
    {TEST_data.glasses_power}
    {TEST_data.exp_vr}
    {TEST_data.exp_ar}
    {TEST_data.exp_3D_editor}"""))

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
    ci.str("PERFORM:\t give instruction to insert k-wire [ENTER when instruction given]: ")

    chrono = chronometer()
    time_init = chrono.start()

    # insertion of k-wire
    while True:
        i = ci.acc("CANDIDATE:\t inserting k-wire... -> checks it and declares it failed [f] or successful [s] (restart timer [r]): ", ["f", "s", "r"])
        if i.lower() == 'f': # PA FAILED
            logger.info("\t\t \\_candidate has FAILED positioning attempt!")
            success = False
            break
        elif i.lower() == 's': # PA SUCCESS
            logger.info("\t\t \\_candidate has performed SUCCESSFUL positioning attempt!")
            success = True
            break
        elif i.lower() == 'r': # restart timer
            logger.info("\t\t \\_restart timer!")
            _ = chrono.reset()
            time_init = chrono.start()
    
    # get PA data
    chrono.pause()
    logger.info(f"DATA COLLECTION - PA{ECP_number}.{PA_number} - ({id})")

    # cycle until all PA data input is correct
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
            PA_D=-1.0, # set after k-wire extraction

            # confidence evaluation
            confidence_position= ci.flo(" |-- CANDIDATE: confidence on entrance position in mm? [FLOAT]: ", min=0),
            confidence_angle=    ci.flo(" |-- CANDIDATE: confidence on angle in deg? [FLOAT]:            ", min=0),
            estimate_hit=        ci.boo(" |-- CANDIDATE: estimate structures hit [Y/N]?:                 "),
            PA_RPC =ci.int(" |-- RADIATION picture count       [INT]  : ", min=0),

            P1A=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: ") - 0.8, # -0.8 as it's removing half a diameter of kwire 
            P1B=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: ") - 0.8,
            P1C=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: ") - 0.8,
            P1D=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: ") - 0.8,
            P2A=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: ") - 0.8,
            P2B=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: ") - 0.8,
            P2C=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: ") - 0.8,
            P2D=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: ") - 0.8,
            
            # computed by fusion
            P1A_F=-1.0,
            P1B_F=-1.0,
            P1C_F=-1.0,
            P1D_F=-1.0,
            P2A_F=-1.0,
            P2B_F=-1.0,
            P2C_F=-1.0,
            P2D_F=-1.0,
            P2eA=-1.0,
            P2eB=-1.0,
            P2eC=-1.0,
            P2eD=-1.0,

            # computed by unity
            P1A_U=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['A']} virtual [FLOAT]: "),
            P1B_U=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['B']} virtual [FLOAT]: "),
            P1C_U=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['C']} virtual [FLOAT]: "),
            P1D_U=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['D']} virtual [FLOAT]: "),
            P2eA_U=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['A']} virtual [FLOAT]: "),
            P2eB_U=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['B']} virtual [FLOAT]: "),
            P2eC_U=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['C']} virtual [FLOAT]: "),
            P2eD_U=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['D']} virtual [FLOAT]: "),
            
            # computed by fusion
            P1_mean_max=1.0,
            P1_mean=-1.0,
            P2_mean_max=2.0,
            P2_mean=-1.0,

            # ECP info
            target=data.TEST_design[ECP_number-1].ktarget,
            markers=data.TEST_design[ECP_number-1].markers,
            anatomy=data.TEST_design[ECP_number-1].anatomy,

            # computed by fusion
            fusion_computed=False,
            angle_PA_target=-1.0,
            distance_P1_PA_target=-1.0,
            distance_P1_PA_target_X=-1.0,
            distance_P1_PA_target_Y=-1.0,
            distance_P1_PA_target_Z=-1.0,
            distance_P2_PA_target=-1.0,
            distance_P2_PA_target_X=-1.0,
            distance_P2_PA_target_Y=-1.0,
            distance_P2_PA_target_Z=-1.0,
            distance_P2e_PA_target=-1.0,
            distance_P2e_PA_target_X=-1.0,
            distance_P2e_PA_target_Y=-1.0,
            distance_P2e_PA_target_Z=-1.0,
            delta_id_PA_target=-1.0
        )
        if ci.boo("\tTECHNICAL:\t is data entered correct? [Y/N]: "):
            break
    
    # cycle until fusion accepts measurement errors
    while True:
        # send to fusion 360 for computation
        PA_data_str = PA_data.dumps()
        pyperclip.copy(PA_data_str)
        logger.info(f"PERFORM:\t test following string on fusion 360 (already copied in clipboard) -> \n{PA_data_str}")

        # receive from fusion 360
        PA_data = ci.PAdata_computed(f"PERFORM:\t enter data from fusion 360: ", PA_data.id)

        if PA_data.P1_mean > PA_data.P1_mean_max:
            logger.info("\tTECHNICAL:\t ATTENTION: P1 measurement error is above max allowed! Please take measurement again:")
            PA_data.P1A=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: ")
            PA_data.P1B=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: ")
            PA_data.P1C=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: ")
            PA_data.P1D=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: ")
        elif PA_data.P2_mean > PA_data.P2_mean_max:
            logger.info("\tTECHNICAL:\t ATTENTION: P2 measurement error is above max allowed! Please take measurement again:")
            PA_data.P2A=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: ")
            PA_data.P2B=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: ")
            PA_data.P2C=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: ")
            PA_data.P2D=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: ")
        elif ci.boo("\tTECHNICAL:\t want to remeasure P1? [Y/N]: "):
            PA_data.P1A=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: ")
            PA_data.P1B=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: ")
            PA_data.P1C=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: ")
            PA_data.P1D=ci.flo(f" |-- P1{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: ")
        elif ci.boo("\tTECHNICAL:\t want to remeasure P2? [Y/N]: "):
            PA_data.P2A=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['A']} [FLOAT]: ")
            PA_data.P2B=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['B']} [FLOAT]: ")
            PA_data.P2C=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['C']} [FLOAT]: ")
            PA_data.P2D=ci.flo(f" |-- P2{data.TEST_design[ECP_number-1].markers['D']} [FLOAT]: ")
        else:
            # P1 and P2 measurement errors are below max allowed
            data.fusion360_imports.append(PA_data_str)
            break
    
    # k-wire extraction of PA is not counted in PA_D
    PA_data.PA_D = chrono.reset()

    data.companion_imports.append(textwrap.dedent(f"""
        ###### PA{ECP_number}.{PA_number} - ({id}) ######
        // following 8 values have already +0.8 inside (ready to paste in companion)
        {PA_data.P1A+0.8}
        {PA_data.P1B+0.8}
        {PA_data.P1C+0.8}
        {PA_data.P1D+0.8}
        {PA_data.P2A+0.8}
        {PA_data.P2B+0.8}
        {PA_data.P2C+0.8}
        {PA_data.P2D+0.8}
        ------
        {PA_data.P1A_U}
        {PA_data.P1B_U}
        {PA_data.P1C_U}
        {PA_data.P1D_U}
        {PA_data.P2eA_U}
        {PA_data.P2eB_U}
        {PA_data.P2eC_U}
        {PA_data.P2eD_U}
        """))

    PA_data.comment = ci.str(f"\tTECHNICAL:\t comment on PA ({id}) [STRING]: ")

    logger.info(f"PA{ECP_number}.{PA_number} FINISHED!")
    return PA_data
    
if __name__ == "__main__":
    main()