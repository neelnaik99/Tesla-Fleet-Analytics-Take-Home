import configparser
from distutils.command.config import config
import pandas as pd
import numpy as np
from dtaidistance import dtw
import itertools
import os 
import logging 
import sys
logging.basicConfig(stream=sys.stderr, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




def get_dataframe_from_path (path):
    """
    Given a path, use pandas to get a dataframe from it.

    Time_complexity:  O(N)
        where N is the length of the time series

    Parameters
    ----------
    path: str
       absolute or relative path to csv with stored data

    Returns
    -------
    df: pd.DataFrame
        information extracted as a dataframe


    """
    df = pd.read_csv(path,index_col=0)
    return df

def time_spent_in_state (df):
    """
    finds the time spent in each state in the dataframe

    time spent in state = (time stamp of current state - time stamp of next state)*-1

    Time_complexity:  O(N)
        where N is the length of the time series

    Parameters
    ----------
    df: pd.DataFrame
        signal information as a dataframe

    Returns
    -------

    df: pd.DataFrame
        signal information as a dataframe with column time_spent_in_state
        for time spent in each state

    """

    date_time_df = pd.to_datetime(df['timestamp_utc'])
    time_spent_in_state = date_time_df.diff(periods = -1)
    df['time_spent_in_state'] = time_spent_in_state*-1

    df['time_spent_in_state'] = df['time_spent_in_state'].fillna(pd.NaT)

    return df



def select_n_values_by_occurence(path,n=1,least_common=True):
    """
    selects n most/least common occurences by total occurence

    Assumption: Occurence = frequency of value

    Time_complexity:  O(N)
        where N is the length of the time series

    Parameters
    ----------
    df: pd.DataFrame
        information extracted as a dataframe

    n: int
        Number of occurences. Default = 1
    
    least_common: bool
        Return least common if true, most common if false. Default = True

    Returns
    -------
    series_time_spent_in_state: Series
        Series with N most/least common values by total occurence 
        and time spent in state

    """
    df = get_dataframe_from_path (path)

    series_frequency_of_occurence = df['sig_value'].value_counts(ascending=least_common)

    series_frequency_of_occurence = series_frequency_of_occurence.rename("Occurence of state i ")

    return series_frequency_of_occurence.head(n)


def select_n_values_by_time_spent(path,n=1,least_common=True):
    """
    selects n most/least common occurences by time spent in the state

    Time_complexity:  O(N)
        where N is the length of the time series

    Parameters
    ----------
    df: pd.DataFrame
        information extracted as a dataframe

    n: int
        Number of occurences. Default = 1
    
    least_common: bool
        Return least common if true, most common if false. Default = True

    Returns
    -------
    
    series_time_spent_in_state: Series
        Series with N most/least common values by total occurence 
        and time spent in state

    """

    df = get_dataframe_from_path (path)

    df = time_spent_in_state (df)

    series_time_spent_in_state = df.groupby('sig_value')['time_spent_in_state'].sum().sort_values(ascending=least_common)

    series_time_spent_in_state = series_time_spent_in_state.rename("Time Spent in state i ")
   

    return series_time_spent_in_state.head(n)

def select_n_cycles(path,n=1,smallest=True):
    """
    selects n most/least common occurences by time spent in the state

    Time_complexity:  O(N)
        where N is the length of the time series

    Assumptions: no flat peaks/valleys

    Definition:
        Minima: x is a minima iff x<x+1 & x<x-1
        Maxima: y is a maxima iff x>x+1 & x>x-1

    Parameters
    ----------
    df: pd.DataFrame
        information extracted as a dataframe

    n: int
        Number of occurences. Default = 1
    
    smallest: bool
        Return smallest cycles if true, largest if false. Default = True

    Returns
    -------
    
    df_cycle: pd.DataFrame
        with the columns: [minima,maxima,cycle_length,cycle_time]
            

    """

    df = get_dataframe_from_path (path)

    df['minima'] = df.sig_value[(df.sig_value.shift(1) > df.sig_value) & (df.sig_value.shift(-1) > df.sig_value)]

    df['maxima'] = df.sig_value[(df.sig_value.shift(1) < df.sig_value) & (df.sig_value.shift(-1) < df.sig_value)]
                                

    df_cycle = df[(df['minima'].notna()) | (df['maxima'].notna())][['timestamp_utc','minima','maxima','sig_value']]
    

    df_cycle['minima'] = df_cycle['minima'].fillna(method='bfill')
    df_cycle['maxima'] = df_cycle['maxima'].fillna(method='bfill')

    df_cycle['cycle_length'] = df_cycle['sig_value'].diff(-1).abs()
 


    #only keep edges of non-flat peaks/valleys
    df_cycle = df_cycle[df_cycle['cycle_length']>0]
    
   
    df_cycle = time_spent_in_state (df_cycle)
    df_cycle=df_cycle.rename(columns={"time_spent_in_state": "cycle_time"})

    df_cycle=df_cycle.sort_values(by=['cycle_length'],ascending=smallest)
    df_cycle = df_cycle.drop(['timestamp_utc','sig_value'],axis=1)
    
    return df_cycle.head(n)



def identify_n_different_time_series(dir_path,n=2,fraction_of_samples=0.15):
    """
    Packages used: 
    Uses Dynamic Time Warping to compute pairwise distance between all timeseries

    dtaidistance.dtw: https://dtaidistance.readthedocs.io/en/latest/usage/dtw.html#dtw-distance-measure-between-two-time-series

    Time_complexity:  O(N^2*M^2)
        where N is the length of the time series
              M is the number of csv files to iterate

    Parameters
    ----------
    dir_path: str
        path to directory with csv containing time series

    n: int
        Number of time series to identify. Default = 2

    fraction_of_samples: float
        Percentage of fractions to use when computing samples. Default = 0.15
    

    Returns
    -------
    
    list_csv_different: List
        Ordered list of n Csv file names containing time series which are the 
        most different than others
            

    """

    dict_signal_val= {}
    dict_total_distance ={}
    Percentage_of_samples_used = fraction_of_samples*100
    
    logger.info(f"Only using {Percentage_of_samples_used} % from each to compute difference in time series")
    

    logger.info(f"Converting all CSV files to dataframes and subsampling")
    for csv_file in os.listdir(dir_path):
            csv_path = os.path.join(dir_path,csv_file)
            df = get_dataframe_from_path(csv_path)
        

            choose= df['sig_value'].sample(frac=fraction_of_samples)
            dict_signal_val[csv_file]=np.array(choose , dtype=np.double)
            dict_total_distance[csv_file] = 0
           

    p = list(itertools.combinations(list(dict_signal_val.keys()),2))
    
    logger.info("Computing pairwise DTW Distance between the given time series data")
    for pair in p:
        
        X,Y = pair
        dtw_score = dtw.distance_fast(dict_signal_val[X],dict_signal_val[Y],window =0,use_pruning=True)

        dict_total_distance[X]+=dtw_score
        dict_total_distance[Y]+=dtw_score
        

   
    list_max_dist = sorted(dict_total_distance, key=dict_total_distance.get, reverse=True)

    logger.info(f"The {n} most different time series are:")

    return list_max_dist[:n]


