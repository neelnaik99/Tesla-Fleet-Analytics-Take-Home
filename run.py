
from functions import *

CURRENT_PATH =  os.path.dirname(os.path.realpath(__file__))
config_file = 'config.ini'

config_file_path = os.path.join(CURRENT_PATH,config_file)
parser = configparser.ConfigParser()
parser.read(config_file_path)

data_folder =  parser['input']['data_folder']
csv_file_name = parser['input']['csv_name']

CURRENT_PATH =  os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = os.path.join(CURRENT_PATH,data_folder)
INPUT_FILE = os.path.join(INPUT_DIR,csv_file_name)


logger.info(f"Using {csv_file_name} as data source for the first 3 functions")

print('least 5 common values by occurence')
print(select_n_values_by_occurence(INPUT_FILE,n=5,least_common=True))


print('The 3 most common values by total time spent at that value') 

print(select_n_values_by_time_spent(INPUT_FILE,n=3,least_common=False))


print('The 3 cycles with the largest amplitude')

print(select_n_cycles(INPUT_FILE,n=3,smallest=False))


print('The 2 Vehicle which are behaving differently from others ')

print(identify_n_different_time_series(INPUT_DIR,n=2,fraction_of_samples=0.15))