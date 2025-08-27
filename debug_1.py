from tests.table_data_good import names, ages, dates, times, datetimes, booleans
rows = [[names[i], ages[i], dates[i], times[i], datetimes[i], booleans[i]] for i in range(len(names))]
from sdtp import SDML_BOOLEAN, SDML_NUMBER, SDML_STRING, SDML_DATE, SDML_DATETIME, SDML_TIME_OF_DAY, InvalidDataException
from sdtp import jsonifiable_column
from sdtp import SDQLFilter
from sdtp import RowTable

schema = [
    {"name": "name", "type": SDML_STRING},
    {"name": "age", "type": SDML_NUMBER},
    {"name": "date", "type": SDML_DATE},
    {"name": "time", "type": SDML_TIME_OF_DAY},
    {"name": "datetime", "type": SDML_DATETIME},
    {"name": "boolean", "type": SDML_BOOLEAN}
]

filter_spec = {'column': 'name', 'operator': 'IN_RANGE', 'max_val': 'Wilmette', 'min_val': 'Aarika'}

table = RowTable(schema, rows)
data_plane_filter = SDQLFilter(filter_spec, schema)
indices = data_plane_filter.filter_index(rows)
pass