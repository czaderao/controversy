import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./raw/dist.csv')
df = df[df['straightdis'] <= 20]


df[['year', 'month', 'day']] = df['start_date'].str.split('/', expand=True).astype(float)
yearly_avg = df.groupby('year')['straightdis'].mean().reset_index()

yearly_all = df.groupby('year')['straightdis'].mean().reset_index()
yearly_true = df[df['ecclesiastical_flag'] == True].groupby('year')['straightdis'].mean().reset_index()
yearly_false = df[df['ecclesiastical_flag'] == False].groupby('year')['straightdis'].mean().reset_index()

# Convert degrees to km
def deg_to_km(series):
    return np.deg2rad(series) * 6371

plt.figure(figsize=(19, 10))
plt.plot(yearly_all['year'], deg_to_km(yearly_all['straightdis']), label='All', marker='o')
plt.plot(yearly_true['year'], deg_to_km(yearly_true['straightdis']), label='Ecclesiastical', marker='o')
plt.plot(yearly_false['year'], deg_to_km(yearly_false['straightdis']), label='Non-Ecclesiastical', marker='o')
plt.title('Average Hub Distance per Year')
plt.xlabel('Year')
plt.ylabel('Average Hub Distance (km)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
