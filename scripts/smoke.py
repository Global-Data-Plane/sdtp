import pandas as pd
from sdtp import RowTable, SDMLTypeConverter, TableBuilder
import json

print("==== SDTP End-to-End Smoke Test ====")

df = pd.DataFrame([
    {"timestamp": "2023-01-01T12:34:56", "value": 42, "note": "good"},
    {"timestamp": None, "value": "NaN", "note": "missing value"},
    {"timestamp": "NaT", "value": 99, "note": ""},
    {"timestamp": pd.NaT, "value": 1.5, "note": "should work"},
])

schema = [
    {"name": "timestamp", "type": "datetime"},
    {"name": "value", "type": "number"},
    {"name": "note", "type": "string"}
]

tc = SDMLTypeConverter(strict=False)
rows = df.values.tolist()

table = RowTable(schema=schema, rows=rows, type_converter=tc)
json_data = table.to_json()
spec = json.loads(json_data)
table2 = TableBuilder.build_table(spec, type_converter=tc)

# FIXED HERE: use .rows and .schema, reconstruct DataFrame for display
columns = [col["name"] for col in table2.schema]
df2 = pd.DataFrame(table2.rows, columns=columns)
print("Reconstructed DataFrame:\n", df2)

filtered = df2[df2["value"] > 10]
print("Filtered DataFrame (value > 10):\n", filtered)
assert table.schema == table2.schema, "Schema mismatch after round-trip"

print("==== All SDTP package smoke tests passed ====")
