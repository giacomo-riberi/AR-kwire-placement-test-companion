from utils.utils import custom_input
import data

version = "v1.3"
db_name = f"positioning_test_data-({version}).db"

ECPs: list[data.ECPdata] = []
PAs: list[data.PAdata] = []
ci = custom_input()