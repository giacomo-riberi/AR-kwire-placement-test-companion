from dataclasses import dataclass
import json
from datetime import datetime
from __init__ import *

# dependent on ECP research decision
kwire_target_byECP: list[str]           = ["K-wire:1",
                                           "K-wire:2",
                                           "K-wire:3"]
markers_byECP: dict[str, str]           = [{"A": "M:3", "B": "M:4", "C": "M:8", "D": "M:9"},
                                           {"A": "M:3", "B": "M:4", "C": "M:8", "D": "M:9"},
                                           {"A": "M:3", "B": "M:4", "C": "M:8", "D": "M:9"}]
anatomy_structs_byECP: dict[str, float] = [{"MeshBody26": -1.0, "MeshBody27": -1.0, "MeshBody28": -1.0, "MeshBody29": -1.0},
                                           {"MeshBody26": -1.0, "MeshBody30": -1.0},
                                           {"MeshBody28": -1.0, "MeshBody31": -1.0}]

@dataclass
class data_elaboration:
    def dumps(self) -> str:
            "dump data into json string"
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    def db_create_table(self, table) -> str:
        "dump data into db table creation string"
        s = []
        for k, v in vars(self).items():
            if k == "id":
                s.append(f"{k} TEXT NOT NULL PRIMARY KEY")
            elif k == "time_init":
                s.append(f"{k} TIMESTAMP")
            elif type(v) == int:
                s.append(f"{k} INTEGER")
            elif type(v) == float:
                s.append(f"{k} REAL")
            elif type(v) == str:
                s.append(f"{k} TEXT")
            elif type(v) == list:
                s.append(f"{k} TEXT")
            elif type(v) == dict:
                if k == "anatomy":
                    for anat_s in anatomy_structs_byECP:
                        for kk, vv in anat_s.items():
                            s.append(f"{kk} REAL")
                elif k == "markers":
                    for kk, vv in v.items():
                        s.append(f"{kk} TEXT")
                else:
                    logger.critical(f"db_create_table: unsupported dict key: {type(v)} {k} {v}")
            elif type(v) == bool:
                s.append(f"{k} BOOL")
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
                dbkeys.append(k)
                dbvals.append(v)
            elif k == "time_init":
                dbkeys.append(k)
                dbvals.append(f"{datetime.fromtimestamp(round(v, 0))}")
            elif type(v) == int:
                dbkeys.append(k)
                dbvals.append(v)
            elif type(v) == float:
                dbkeys.append(k)
                dbvals.append(v)
            elif type(v) == str:
                dbkeys.append(k)
                dbvals.append(v)
            elif type(v) == list:
                dbkeys.append(k)
                dbvals.append(";".join(v))
            elif type(v) == dict:
                dbkeys.extend(v.keys())
                dbvals.extend(v.values())
            elif type(v) == bool:
                dbkeys.append(k)
                dbvals.append(v)
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
    time_init: float
    phase: str
    phantom_id: int
    name: str
    surname: str
    gender: str
    right_handed: bool
    age: int
    specialization_year: str
    num_operations: int
    test_duration: float
    test_radiation: float
    test_PAC: int
    test_PACF: int
    test_ECPC: int

@dataclass
class ECPdata(data_elaboration):
    "estimated correct position data"
    datatype: str
    TEST_id: int
    id: int
    PA_ids: list[str]
    time_init: float
    phase: str
    ECP_number: int
    ECPD: float; "ECP duration"
    ECPR: float; "ECP radiation"
    ECP_PAC: float
    ECP_PACF: float


@dataclass
class PAdata(data_elaboration):
    "positioning attempt data"
    datatype: str
    TEST_id: int
    ECP_id: int
    id: int
    time_init: float
    phase: str
    ECP_number: int
    PA_number: int
    success: bool
    PAD: float
    PAR: float
    P1A: float
    P1B: float
    P1C: float
    P1D: float
    P2A: float
    P2B: float
    P2C: float
    P2D: float
    ktarget: str; "k-wire target component name on fusion 360"
    markers: dict[str, str]
    fusion_computed: bool; "analyzed by fusion 360"
    anatomy: dict[str, float]
    angle_kPA_ktarget: float
    distance_ep_kPA_ktarget: float; "distance skin entrance point"
    distance_ep_kPA_ktarget_X: float
    distance_ep_kPA_ktarget_Y: float
    distance_ep_kPA_ktarget_Z: float
    distance_id_kPA_ktarget: float; "delta insertion depth"
