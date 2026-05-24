import pandas as pd

df_global = pd.read_csv('data/raw/global_dengue_data.csv')

# only include data after 1995 due to missing data
df_filtered = df_global[df_global['Year'] >= 1995]

annual_totals = df_filtered.groupby(['adm_0_name', 'Year'])['dengue_total'].sum().reset_index()

df_pivoted = annual_totals.pivot(index='adm_0_name', columns='Year', values='dengue_total')

years_before_2022 = [yr for yr in df_pivoted.columns if isinstance(yr, int) and yr < 2022]

# remove countries with missing data
df_pivoted_cleaned = df_pivoted.dropna(subset=years_before_2022)

sources = df_filtered.groupby('adm_0_name')['UUID'].first().reset_index()
sources.columns = ['adm_0_name', 'Main Source']

final_df = df_pivoted_cleaned.reset_index().merge(sources, on='adm_0_name')
final_df = final_df.rename(columns={'adm_0_name': 'Country'})

final_df.to_csv('data/cleaned/cleaned_global_dengue_data.csv', index=False)