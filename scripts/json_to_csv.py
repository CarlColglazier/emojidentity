import json
import ast
import pandas as pd

lines = []
with open("samplecontrol120118.txt") as f:
    """
    for line in f:
        data = ast.literal_eval(line)
        lines.append(data)
    """
    for line in f:
        data = json.loads(line)
        lines.append(data)

pd.DataFrame(lines).to_csv("../data/updatedsamplecontrol.csv", index=False)
