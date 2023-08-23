import pandas as pd
import os
from CoolProp.CoolProp import PropsSI as CPPSI
import matplotlib.pyplot as plt

# first load the data
data_folder = "data_original/"
file_list = os.listdir(data_folder)

# initialize the dictionary of DataFrames
df_dict = {}

# loop through all data files in the folder
for i, file in enumerate(file_list):
    # skip original files. this is necessary, because negative results created different log files
    if file.split('.')[0][-4:] == 'orig':
        continue

    # read the data file
    df = pd.read_csv(data_folder+file)

    # drop the Unnamed: 0 column, if there is one
    if 'Unnamed: 0' in df.columns:
       df = df.drop(columns=['Unnamed: 0'])

    # convert TimeStamp to datetime
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%d %H:%M:%S.%f')

    # create a time from start column
    df['TimeFromStart'] = df['TimeStamp'] - df['TimeStamp'][0]

    # create a list of dataframe starting at compressor start
    df_cropped = df[df['cmp_speed']>0]
    df_cropped = df_cropped.reset_index()

    # create a time from start column
    df_cropped['TimeFromStart'] = df_cropped['TimeStamp'] - df_cropped['TimeStamp'][0]

    # add an entry to the df_dict
    df_dict[file.split('_')[4]] = {'name': file.split('_')[4], 'df': df, 'df_cropped': df_cropped}

# Define the plot_series parameter. This defines, which entries of the df_dict shall be plotted
# plot_series = ['snid0102', 'snid0102-2']
plot_series = ['snid0109', 'snid0109-2']
plot_series = 'all'
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)

for series, data in df_dict.items():
    if plot_series == 'all':
        plot_series = df_dict.keys()
    if series in plot_series:
        ax1.plot(data['df']['TimeFromStart'], data['df']['t_glyc_in'])
        ax1.set_ylabel('t_glyc_in')
        ax2.plot(data['df']['TimeFromStart'], data['df']['t_glyc_out'])
        ax2.set_ylabel('t_glyc_out')
        ax3.plot(data['df']['TimeFromStart'], data['df']['l3_power'])
        ax3.set_ylabel('heater power')
fig.legend(plot_series)

glycol_end_temperature = []
fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True)
for series, data in df_dict.items():
    if plot_series == 'all':
        plot_series = df_dict.keys()
    if series in plot_series:
        ax[0, 0].plot(data['df_cropped']['TimeFromStart'], data['df_cropped']['t_glyc_out'])
        ax[0, 0].set_ylabel('Glycol temperature')
        ax[1, 0].plot(data['df_cropped']['TimeFromStart'], data['df_cropped']['superheat'])
        ax[1, 0].set_ylabel('Superheat')
        ax[2, 0].plot(data['df_cropped']['TimeFromStart'], data['df_cropped']['cmp_speed'])
        ax[2, 0].set_ylabel('Compressor speed')
        ax[0, 1].plot(data['df_cropped']['TimeFromStart'], data['df_cropped']['v_glyc'])
        ax[0, 1].set_ylabel('Glycol volume flow')
        ax[1, 1].plot(data['df_cropped']['TimeFromStart'], data['df_cropped']['high_pressure'])
        ax[1, 1].set_ylabel('high pressure')
        ax[2, 1].plot(data['df_cropped']['TimeFromStart'], data['df_cropped']['low_pressure'])
        ax[2, 1].set_ylabel('low pressure')
        glycol_end_temperature.append(data['df_cropped']['t_glyc_out'].iloc[-1])

fig.legend(plot_series)
plt.show()
#
# fig = plt.figure()
# plt.plot(glycol_end_temperature)
# plt.show()
