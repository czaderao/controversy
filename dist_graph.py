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

# plot that thing
plt.figure(figsize=(19, 10))
plt.plot(yearly_all['year'], deg_to_km(yearly_all['straightdis']), label='All', marker='o', color='blue',
         linestyle='dashed')
plt.plot(yearly_false['year'], deg_to_km(yearly_false['straightdis']), label='Church-unrelated', marker='o',
         color='red')
plt.plot(yearly_true['year'], deg_to_km(yearly_true['straightdis']), label='Church-related', marker='o', color='green')
plt.title('Average Bishopric/Archbishopric Distance from charter origin per Year during the reign of Henry IV.')
plt.xlabel('Year')
plt.ylabel('Average Hub Distance (km)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()