import os
from csv_utils import Execute
from data_class import data_cl
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])
BOT_TOKEN = '5880925429:AAHnImGc0-6BNQycmwRXSm8W0fOFMZdsA78'
tg_ids = [1021524873, 5013549994]
url_ads = 'http://local.adspower.com:57829'
txt_file = homeDir + '\\txt\\data.txt'
name_csv_file = homeDir + '\\csv\\regs.csv'
csv_columns = ['data']

datas = Execute(name_file=txt_file, name_csv_file=name_csv_file, list_columns=csv_columns, target_column='data', formater=data_cl)
csv = datas.csv