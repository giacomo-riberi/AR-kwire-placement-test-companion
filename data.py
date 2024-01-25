from dataclasses import dataclass
import json
from datetime import datetime

from logger import logger
from __init__ import *

@dataclass
class ECP_design:
    ktarget: str
    markers: dict[str, str]
    anatomy: dict[str, float]

# relative to phantom v2.3.5
TEST_design: list[ECP_design] = [
    ECP_design("ECP:1",
               {"A": "M:2", "B": "M:3", "C": "M:7", "D": "M:8"},
               {"brachial artery": -1.0,
                "brachial vein": -1.0,
                "cephalic vein": -1.0,
                "basilic vein": -1.0,
                "random artery 1": -1.0,
                "median cubital vein": -1.0,
                "median cubital vein 1": -1.0,
                "inferior ulnar collateral artery": -1.0,
                "radial collateral artery": -1.0,
                "middle collateral artery": -1.0,

                "ulnar nerve": -1.0,
                "median nerve": -1.0,
                "musculocutaneous nerve": -1.0,
                "posterior branch of medial antebrachial cutaneous nerve": -1.0,
                "anterior branch of medial antebrachial cutaneous nerve": -1.0,
                "muscular branches of radial nerve": -1.0,
                "radial nerve": -1.0,
                "posterior antebrachial cutaneous nerve": -1.0,
                "anterior interosseous nerve of forearm": -1.0,
               }),
    ECP_design("ECP:2",
               {"A": "M:3", "B": "M:4", "C": "M:8", "D": "M:9"},
               {"cephalic vein": -1.0,
                "basilic vein": -1.0,
                "brachial artery": -1.0,
                "brachial vein": -1.0,
                "ulnar artery": -1.0,
                "ulnar veins": -1.0,
                "radial artery": -1.0,
                "radial veins": -1.0,
                "radial collateral artery": -1.0,
                "middle collateral artery": -1.0,
                "inferior ulnar collateral artery": -1.0,
                "random artery 1": -1.0,
                "random artery 2": -1.0,
                "median cubital vein": -1.0,
                "median cubital vein 1": -1.0,
                "median antebrachial vein": -1.0,
                   
                "anterior interosseous nerve of forearm": -1.0,
                "median nerve": -1.0,
                "ulnar nerve": -1.0,
                "posterior branch of medial antebrachial cutaneous nerve": -1.0,
                "posterior antebrachial cutaneous nerve": -1.0,
                "anterior branch of medial antebrachial cutaneous nerve": -1.0,
                "lateral antebrachial cutaneous nerve": -1.0,
                "superficial branch of radial nerve": -1.0,
                "deep branch of radial nerve": -1.0,
               }),
    ECP_design("ECP:3",
               {"A": "M:2", "B": "M:3", "C": "M:7", "D": "M:8"},
               {"middle collateral artery": -1.0,
                "random artery 1": -1.0,
                "basilic vein": -1.0,
                "brachial vein": -1.0,
                "median cubital vein": -1.0,
                "brachial artery": -1.0,
                "inferior ulnar collateral artery": -1.0,
                "radial collateral artery": -1.0,

                "ulnar nerve": -1.0,
                "posterior branch of medial antebrachial cutaneous nerve": -1.0,
                "median nerve": -1.0,
                "anterior branch of medial antebrachial cutaneous nerve": -1.0,
                "musculocutaneous nerve": -1.0,
                "radial nerve": -1.0,
                "muscular branches of radial nerve": -1.0,
               })
]

class data_elaboration:
    def dumps(self) -> str:
            "dump data into json string"
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    def db_create_table(self, table) -> str:
        "dump data into db table creation string"
        s = []
        for k, v in vars(self).items():
            if k == "id":
                s.append(f"`{k}` TEXT NOT NULL PRIMARY KEY")
            elif k == "time_init":
                s.append(f"`{k}` TIMESTAMP")
            elif type(v) == int:
                s.append(f"`{k}` INTEGER")
            elif type(v) == float:
                s.append(f"`{k}` REAL")
            elif type(v) == bool:
                s.append(f"`{k}` BOOL")
            elif type(v) == str:
                s.append(f"`{k}` TEXT")
            elif type(v) == list:
                s.append(f"`{k}` TEXT")
            elif type(v) == dict:
                if k == "anatomy":
                    for ECP_design in TEST_design:
                        for kk, vv in ECP_design.anatomy.items():
                            s.append(f"`{kk}` REAL")
                elif k == "markers":
                    for kk, vv in v.items():
                        s.append(f"`{kk}` TEXT")
                else:
                    logger.critical(f"db_create_table: unsupported dict key: {type(v)} {k} {v}")
            else:
                logger.critical(f"db_create_table: unsupported value type: {type(v)} {k} {v}")
        s = list(dict.fromkeys(s)) # remove duplicates
        return f"CREATE TABLE IF NOT EXISTS {table} (" + ", ".join(s) + ")"

    def db_insert_table(self, table) -> tuple[str, tuple]:
        "dump data into db table insertion string"
        dbkeys: list[str] = []
        dbvals: list[any] = []
        for k, v in vars(self).items():
            if k == "id":
                dbkeys.append(f"`{k}`")
                dbvals.append(v)
            elif k == "time_init":
                dbkeys.append(f"`{k}`")
                dbvals.append(f"{datetime.fromtimestamp(round(v, 0))}")
            elif type(v) == int:
                dbkeys.append(f"`{k}`")
                dbvals.append(v)
            elif type(v) == float:
                dbkeys.append(f"`{k}`")
                dbvals.append(v)
            elif type(v) == bool:
                dbkeys.append(f"`{k}`")
                dbvals.append(v)
            elif type(v) == str:
                dbkeys.append(f"`{k}`")
                dbvals.append(v)
            elif type(v) == list:
                dbkeys.append(f"`{k}`")
                dbvals.append(";".join(v))
            elif type(v) == dict:
                dbkeys.extend([f"`{kk}`" for kk in v.keys()])
                dbvals.extend(v.values())
            else:
                logger.error(f"db_create_table: unsupported value type: {type(v)} {k} {v}")
        return f"INSERT INTO {table} (" + ", ".join(dbkeys) + f") VALUES ({','.join(['?'] * len(dbkeys))})", tuple(dbvals)

@dataclass
class TESTdata(data_elaboration):
    "test data"
    datatype: str
    id: str
    ECP_ids: list[str]
    PA_ids: list[str]
    comment: bool; "used to mark data on database for later technical analysis"
    time_init: float
    phase: str
    phantom_id: str
    name: str
    surname: str
    gender: str
    right_handed: bool
    age: int
    medicine_surge_year: int
    specialization_year: int
    surgeon_year: int
    exp_operation_count: int

    glasses: float
    glasses_type: str
    glasses_power: float

    exp_vr: int
    exp_ar: int
    exp_3D_editor: int
    TEST_D: float
    TEST_RPC: int; "TEST radiation picture count"
    TEST_PAC: int
    TEST_PACF: int
    TEST_ECPC: int

@dataclass
class ECPdata(data_elaboration):
    "estimated correct position data"
    datatype: str
    TEST_id: int
    id: int
    PA_ids: list[str]
    time_init: float
    ease_of_placement: int
    phase: str
    ECP_number: int
    ECP_D: float; "ECP duration"
    ECP_RPC: int; "ECP radiation picture count"
    ECP_PAC: float
    ECP_PACF: float

@dataclass
class PAdata(data_elaboration):
    "positioning attempt data"
    datatype: str
    TEST_id: int
    ECP_id: int
    id: int
    comment: str; "used to mark data on database for later technical analysis"
    time_init: float
    phase: int
    ECP_number: int
    PA_number: int
    success: bool
    PA_D: float
    PA_RPC: int;    "PA radiation picture count"
    P1A: float
    P1B: float
    P1C: float
    P1D: float
    P2A: float
    P2B: float
    P2C: float
    P2D: float
    P1A_V: float
    P1B_V: float
    P1C_V: float
    P1D_V: float
    P2A_V: float
    P2B_V: float
    P2C_V: float
    P2D_V: float
    max_mean: float
    max_SD:   float
    max_SE:   float
    P1_mean:  float
    P1_SD:    float
    P1_SE:    float
    P2_mean:  float
    P2_SD:    float
    P2_SE:    float
    confidence_position: float
    confidence_angle: float
    estimate_hit: bool
    target: str; "k-wire target component name on fusion 360"
    markers: dict[str, str]
    fusion_computed: bool; "analyzed by fusion 360"
    anatomy: dict[str, float]
    angle_PA_target: float

    distance_P1_PA_target: float; "distance P1"
    distance_P1_PA_target_X: float
    distance_P1_PA_target_Y: float
    distance_P1_PA_target_Z: float

    distance_P2_PA_target: float; "distance P2"
    distance_P2_PA_target_X: float
    distance_P2_PA_target_Y: float
    distance_P2_PA_target_Z: float

    distance_P2e_PA_target: float; "distance P2 estimated"
    distance_P2e_PA_target_X: float
    distance_P2e_PA_target_Y: float
    distance_P2e_PA_target_Z: float
    
    delta_id_PA_target: float; "delta insertion depth"

ECPs_toinsert:     list[ECPdata] = []
PAs_toinsert:      list[PAdata]  = []
fusion360_imports: list[str]     = []