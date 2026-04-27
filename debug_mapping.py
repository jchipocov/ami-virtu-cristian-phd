from src.simulation.data_simulator import DataSimulator
import pandas as pd

sim = DataSimulator(num_records=5)
df = sim.generate_dataset()
print("Columns:", df.columns.tolist())
print("C1 values:", df['C1'].tolist())
print("C1 unique:", df['C1'].unique())

likert_map = {
    "Totalmente en desacuerdo": 1, "En desacuerdo": 2, 
    "Ni de acuerdo ni en desacuerdo": 3, "De acuerdo": 4, 
    "Totalmente de acuerdo": 5
}

mapped = df['C1'].map(likert_map)
print("Mapped C1:", mapped.tolist())
