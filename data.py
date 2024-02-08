from dataclasses import dataclass, fields
import json
from datetime import datetime
import faker
import random

from logger import logger
from __init__ import *

fake = faker.Faker()

class data_elaboration:
    def __init__(self, **kwargs):
        if len(kwargs) != 1 and len(kwargs) != len(fields(self)):
            raise ValueError(f"Invalid number of arguments ({len(kwargs)} out of {len(fields(self))}). Please provide values for one or all attributes.")
        for field in fields(self):
            setattr(self, field.name, kwargs.get(field.name, self.generate_random_value(field)))
            
    def generate_random_value(self, field):            
        if field.type == int:
            return random.randint(1, 100)
        elif field.type == float:
            return round(random.uniform(0.0, 100.0), 5)
        elif field.type == bool:
            return random.choice([True, False])
        elif field.type == str:
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz ', k=10))
        elif field.type == list[str]:
            return [''.join(random.choices('abcdefghijklmnopqrstuvwxyz ', k=5)) for _ in range(3)]
        elif field.type == dict[str, str]:
            return random.choice(PHASE_design).markers
        elif field.type == dict[str, float]:
            return random.choice(PHASE_design).anatomy
        else:
            logger.critical(f"generate_random_value: unsupported value type: {field.type}")

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
                    for ECP_design in PHASE_design:
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
                logger.critical(f"db_create_table: unsupported value type: {type(v)} {k} {v}")
        return f"INSERT INTO {table} ({', '.join(dbkeys)}) VALUES ({','.join(['?'] * len(dbkeys))})", tuple(dbvals)
    
    def db_update_table(self, table, id) -> str:
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
                dbvals.append(1 if v else 0)
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
                logger.critical(f"db_create_table: unsupported value type: {type(v)} {k} {v}")

        return f"UPDATE {table} SET {', '.join([f"{key} = '{value}'" for key, value in zip(dbkeys, dbvals)])} WHERE id = '{id}';"

@dataclass
class ECP_design:
    ktarget: str
    markers: dict[str, str]
    anatomy: dict[str, float]

# relative to phantom v2.3.5
anatomy_eval: dict[str, str] = {
    "basilic vein": -1.0,
    "brachial artery": -1.0,
    "brachial vein": -1.0,
    "cephalic vein": -1.0,
    "inferior ulnar collateral artery": -1.0,
    "median antebrachial vein": -1.0,
    "median cubital vein": -1.0,
    "median cubital vein 1": -1.0,
    "middle collateral artery": -1.0,
    "radial artery": -1.0,
    "radial collateral artery": -1.0,
    "radial veins": -1.0,
    "random artery 1": -1.0,
    "random artery 2": -1.0,
    "ulnar artery": -1.0,
    "ulnar veins": -1.0,

    "anterior branch of medial antebrachial cutaneous nerve": -1.0,
    "anterior interosseous nerve of forearm": -1.0,
    "deep branch of radial nerve": -1.0,
    "lateral antebrachial cutaneous nerve": -1.0,
    "median nerve": -1.0,
    "muscular branches of radial nerve": -1.0,
    "musculocutaneous nerve": -1.0,
    "posterior antebrachial cutaneous nerve": -1.0,
    "posterior branch of medial antebrachial cutaneous nerve": -1.0,
    "radial nerve": -1.0,
    "superficial branch of radial nerve": -1.0,
    "ulnar nerve": -1.0,
}

PHASE_design: list[ECP_design] = [
    ECP_design("ECP:1",
               {"A": "M:2", "B": "M:3", "C": "M:7", "D": "M:8"},
               anatomy_eval),
    ECP_design("ECP:2",
               {"A": "M:3", "B": "M:4", "C": "M:8", "D": "M:9"},
               anatomy_eval),
    ECP_design("ECP:3",
               {"A": "M:2", "B": "M:3", "C": "M:7", "D": "M:8"},
               anatomy_eval)
]

@dataclass
class PHASEdata(data_elaboration):
    "test data"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    datatype: str
    id: str
    ECP_ids: list[str]
    PA_ids: list[str]
    comment: str; "used to mark data on database for later technical analysis"
    time_init: float
    phase: int
    phantom_id: str
    country_orig: str
    country: str
    city: str
    institute: str
    name: str
    surname: str
    gender: str
    right_handed: bool
    age: int
    medicine_surge_year: int
    specialization_year: int
    surgeon_year: int
    exp_operation_count: int

    glasses: bool
    glasses_type: str
    glasses_power: float

    exp_vr: int
    exp_ar: int
    exp_3D_editor: int

    realism_xray: int
    realism_ar: int
    realism_phantom: int

    sim_quality_xray: int
    sim_quality_ar: int
    sim_quality_phantom: int

    comfort_xray: int
    comfort_ar: int

    PHASE_D: float
    PHASE_RPC: int; "PHASE radiation picture count"
    PHASE_PAC: int
    PHASE_PACF: int
    PHASE_ECPC: int

@dataclass
class ECPdata(data_elaboration):
    "estimated correct position data"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    datatype: str
    PHASE_id: str
    id: str
    PA_ids: list[str]
    time_init: float
    ease_of_placement: int
    phase: int
    ECP_number: int
    ECP_D: float; "ECP duration"
    ECP_RPC: int; "ECP radiation picture count"
    ECP_PAC: float
    ECP_PACF: float

@dataclass
class PAdata(data_elaboration):
    "positioning attempt data"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    datatype: str
    PHASE_id: str
    ECP_id: str
    id: str
    comment: str; "used to mark data on database for later technical analysis"
    time_init: float
    phase: int
    ECP_number: int
    PA_number: int
    success: bool

    entered_articulation: int; "kwire entered articulation cavity (-1: not analyzed; 0: not entered; 1: entered)"

    PA_D: float
    PA_RPC: int;    "PA radiation picture count"

    values_from_unity: str
    P1A: float;     "P1 - marker: measured with caliper"
    P1B: float
    P1C: float
    P1D: float
    P2A: float
    P2B: float
    P2C: float
    P2D: float
    P1A_F: float;   "P1 - marker: measured in fusion"
    P1B_F: float
    P1C_F: float
    P1D_F: float
    P2A_F: float
    P2B_F: float
    P2C_F: float
    P2D_F: float

    P2eA: float;   "P2e - marker: measured in fusion"
    P2eB: float
    P2eC: float
    P2eD: float
    
    P1A_U: float;   "P1A - marker: measured in unity"
    P1B_U: float
    P1C_U: float
    P1D_U: float
    P2eA_U: float
    P2eB_U: float
    P2eC_U: float
    P2eD_U: float

    P1_mean_max: float
    P1_mean:  float
    P2_mean_max: float
    P2_mean:  float
    
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

PHASE_toinsert:    PHASEdata     = None
ECPs_toinsert:     list[ECPdata] = []
PAs_toinsert:      list[PAdata]  = []
fusion360_imports: list[str]     = []
companion_imports: list[str]     = []