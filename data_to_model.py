import eurostat
import pandas as pd

###########
# Home ownership ratio
##########
code = 'ilc_lvho02'
my_filter_pars = {'geo': ['BE'],
                  'incgrp': 'TOTAL',
                  'tenure': ['OWN_NL', 'OWN'], # owner no outstanding mortgage, owner with/without outstanding debt
                  'freq': 'A',
                  'hhtyp': 'TOTAL',                

}
df = eurostat.get_data_df(code, filter_pars=my_filter_pars)
df['Total'] = df.sum(axis=1)
non_numeric_columns = df.applymap(lambda x: pd.to_numeric(x, errors='coerce')).isna().all()

# Drop columns with all non-numeric values
df = df.drop(columns=non_numeric_columns[non_numeric_columns].index)
df = df.drop(columns = 'Total')
df['home_ownership_ratio'] = df.mean(axis = 1)
df.head()

###########
# Home ownership ratio
##########

# # Eurostat dataset code for Gross Capital Formation (GCF) by sector
# gcf_dataset = 'nama_10_a10'

# # Eurostat dataset code for Disposable Income by sector
# di_dataset = 'nama_10_a11'

# # Specify filters for GCF and DI datasets
# gcf_filters = {'na_item': 'P51GCF', 
#                   'sector': 'S14', 
#                   'geo': ['BE'],
#                   }
# di_filters = {'na_item': 'B6G', 'sector': 'S14'}

# # Download Eurostat data for GCF and DI
# gcf_data = download_eurostat_data(gcf_dataset, gcf_filters)
# di_data = download_eurostat_data(di_dataset, di_filters)

# # Merge GCF and DI data on the relevant columns (e.g., 'geo' for country and 'time' for year)
# merged_data = pd.merge(gcf_data, di_data, on=['geo', 'time'], suffixes=('_gcf', '_di'))

# # Calculate GCF to Disposable Income ratio
# merged_data['gcf_di_ratio'] = merged_data['values_gcf'] / merged_data['values_di']


###########
# Home house price to rent ratio
##########
# Eurostat dataset code for hicp for actual rentals for housing / actual rental paid by tenants by sector
df = []
dataset = 'prc_hicp_midx'

# Specify filters for GCF and DI datasets
filters = {'coicop': ['CP04', 'CP041'], #  actual rentals for housing / actual rental paid by tenants
            'geo': ['BE'],
            'unit': ['I15'], #  index 2015 = 100 
                  }
# # Download Eurostat data for GCF and DI
df =  eurostat.get_data_df(dataset, filter_pars=filters)
df = df.drop(columns = ['freq', 'unit', 'geo\TIME_PERIOD'])
df.set_index('coicop', inplace = True)

df = df.transpose().reset_index()
df['index'] = pd.to_datetime(df['index'], format='%Y-%m')
df.set_index('index', inplace=True)

# Calculate the yearly average
df = df.resample('Y').mean()
df
###
# House price index
###

# Specify dataset and filters for House Price Index
hpi_dataset = 'prc_hpi_q'
hpi_filters = {'purchase': ['TOTAL', 'DW_NEW', 'DW_EXST'] , #  purchases total, only new dwelling or existing dwellings
               'geo': ['BE'],
               'unit': ['I15_Q'], # quarterly index 2015 = 100 
               }

# Download Eurostat data for House Price Index
hpi_df = eurostat.get_data_df(hpi_dataset, filter_pars=hpi_filters)
# Drop unnecessary columns
hpi_df = hpi_df.drop(columns=['freq', 'unit', 'geo\\TIME_PERIOD'])
hpi_df
# Set the appropriate column as an index (e.g., 'indic' for HPI)
hpi_df.set_index('purchase', inplace=True)

# Transpose the DataFrame and reset the index
hpi_df = hpi_df.transpose().reset_index()

hpi_df['index'] = pd.to_datetime(hpi_df['index'].str.replace('Q', ''), format='%Y-%m')

hpi_df.set_index('index', inplace=True)

# Calculate the yearly average
yearly_avg = hpi_df.resample('Y').mean()
yearly_avg

df_mearged = df.merge(yearly_avg, how = 'left', on='index')
df_mearged['new_homes_cpi_rent'] =  df_mearged.DW_NEW /  df_mearged.CP041  * 100
new_homes_cpi_rent = df_mearged['new_homes_cpi_rent'].mean()
df_mearged['existing_homes_cpi_rent'] =  df_mearged.DW_EXST /  df_mearged.CP041 * 100
existing_homes_cpi_rent = df_mearged['existing_homes_cpi_rent'].mean()
print(new_homes_cpi_rent)
print(existing_homes_cpi_rent)

###########
# Housing gross fixed capital formation
##########
# Eurostat dataset code for hicp for actual rentals for housing / actual rental paid by tenants by sector
df = []
dataset = 'namq_10_an6'

# Specify filters for GCF and DI datasets
filters = {'asset10': ['N111G'], #  gross fixed capital formation dwellings
            'geo': ['BE'],
            's_adj': ['SA']
            'unit': ['CLV_I15'], #  Chain linked volumes, index 2015=100
                  }
# # Download Eurostat data for GCF and DI
df =  eurostat.get_data_df(dataset, filter_pars=filters)
df = df.drop(columns = ['freq', 'unit', 'geo\TIME_PERIOD'])
df
df.set_index('asset10', inplace = True)

df = df.transpose().reset_index()
df['index'] = pd.to_datetime(df['index'], format='%Y-%m')
df.set_index('index', inplace=True)
df = df.dropna()

###########
# Household grpss disposable income
##########
# Eurostat dataset code for hicp for actual rentals for housing / actual rental paid by tenants by sector
df = []
dataset = 'sdg_10_20'

# Specify filters for GCF and DI datasets
filters = {'asset10': ['N111G'], #  gross fixed capital formation dwellings
            'geo': ['BE'],
            'unit': ['CLV_I15'], #  Chain linked volumes, index 2015=100
                  }
# # Download Eurostat data for GCF and DI
df =  eurostat.get_data_df(dataset, filter_pars=filters)
df = df.drop(columns = ['freq', 'unit', 'geo\TIME_PERIOD'])
df
df.set_index('asset10', inplace = True)

df = df.transpose().reset_index()
df['index'] = pd.to_datetime(df['index'], format='%Y-%m')
df.set_index('index', inplace=True)
df = df.dropna()