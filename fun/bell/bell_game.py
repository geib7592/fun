import numpy as np
import pandas as pd


N = 100001
df = pd.DataFrame()
rng = np.random.default_rng()
df["Tester_A"] = rng.choice([True, False], N)
df["Tester_B"] = rng.choice([True, False], N)

df["Alice"] = True
df["Bob"] = df.Alice

df["flip"] = df.Tester_A & df.Tester_B
df["win"] = df.Alice & df.Bob
df.loc[df["flip"], "win"] = df.Alice & ~df.Bob

print(df.head())
print(df.win.mean())

...
