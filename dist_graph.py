import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv('./raw/dist.csv')

mask = df['start_date'].isna()
df.loc[mask, 'start_date'] = pd.to_datetime(df.loc[mask, 'start_date'], errors='coerce')

df['year'] = df['start_date'].dt.year
yearly_avg = df.groupby('year')['length'].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(yearly_avg['year'], yearly_avg['length'], marker='o')
plt.title('Average Hub Distance per Year')
plt.xlabel('Year')
plt.ylabel('Average Hub Distance')
plt.grid(True)
plt.tight_layout()
plt.show()
