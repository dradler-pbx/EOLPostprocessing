# calculate the four missing parameters to the "orig" file

import pandas as pd
import os
from CoolProp.CoolProp import PropsSI as CPPSI
import matplotlib.pyplot as plt


def test_elements_in_list(list1, list2):
    # iterate over each element elem in list2, and check if it is present in list1
    # using a list comprehension
    present_in_list1 = [elem in list1 for elem in list2]

    # check if all elements in present_in_list1 are True using the all function
    if all(present_in_list1):
        # if all elements in list2 are present in list1, return True
        return True
    else:
        # otherwise, return False
        return False

def main():
    # first load the data
    data_folder = "data_original/"
    file_list = os.listdir(data_folder)
    onewire_sensor_names = ['phe_out', 'cond_in', 'cond_out', 'cond_air']

    for file in file_list:
        filename = file.split('.')
        if filename[0][-4:] != 'orig':
            continue
        df = pd.read_csv(data_folder+file)

        # check, if the onewire sensors are identified
        print('Please identify the onewire temperature sensors. Just type the number of the sensor.')
        if not test_elements_in_list(df.columns, onewire_sensor_names):
            temp_sensors = ['temp_sensor_1', 'temp_sensor_2', 'temp_sensor_3', 'temp_sensor_4']
            for s in temp_sensors:
                plt.plot(df[s])
            plt.legend(temp_sensors)
            plt.title(file)
            plt.show(block=False)
            plt.pause(0.1)
            for sensor in onewire_sensor_names:
                identified_dataset = input('Please identify the onewiresensor {}: '.format(sensor))
                id_sensor = 'temp_sensor_'+identified_dataset
                df.rename(columns={id_sensor: sensor}, inplace=True)
            plt.close()

        # calculate the remaining parameters
        df['t0'] = df.apply(lambda row: CPPSI('T', 'P', row['low_pressure']*1e5, 'Q', 1, 'R290')-273.15, axis=1)
        df['tc'] = df.apply(lambda row: CPPSI('T', 'P', row['high_pressure']*1e5, 'Q', 1, 'R290')-273.15, axis=1)
        df['superheat'] = df['phe_out'] - df['t0']
        df['sub_cooling'] = df['tc'] - df['cond_out']

        filename[0] = filename[0]+'cleaned'
        df.to_csv(data_folder+filename[0]+'.'+filename[1])


if __name__ == '__main__':
    main()
