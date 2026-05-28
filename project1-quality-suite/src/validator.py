import yaml
from pathlib import Path
from db_connector import *

class readConfig:

    def __init__(self,file_path):
        self.path = file_path

    def read_ymlfile(self):
        with open(self.path,"r") as ymlfile:
            data = yaml.safe_load(ymlfile)
            return data
        
    def rules_check(self,df,rules,columns):
        
        if rules == "null_check":
            print("Null Check data::>>>>>>>>>")
            return df[(df['customer_id'].isnull()) | (df['order_id'].isnull())]
        elif rules == 'duplicate_check':
            print("duplicate check inside the dataframe :>>>>>>>>>>>>>>>>>>>>>")
            return df[df['order_id'].duplicated()]
        else:
            print("Range check inside the dataframe :>>>>>>>>>>>>>>>>>>>>>")
            return df[(df['total_amount'] > 50000) | (df['total_amount'] < 0)]


if  __name__ == "__main__":
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = Path(__file__).resolve().parent.parent       # >>>>>> ITS WINDOWS PATH
    config_path = base_dir / "config" / "validation_rules.yaml"
    fileRead = readConfig(config_path)
    yaml_data = fileRead.read_ymlfile()
    print(yaml_data)
    print(f"Database: {yaml_data['databases'][0]['name']}, table_name: {yaml_data['databases'][0]['tables'][0]['name']}")
    num_of_rules = len(yaml_data['databases'][0]['tables'][0]['rules'])
    df = db_connection('postgresql','psycopg2','admin','postgres123','localhost','5432','project1')
    for i in range(num_of_rules):
        print(f"rules: {yaml_data['databases'][0]['tables'][0]['rules'][i]['type']}")
        print(f"column_list: {yaml_data['databases'][0]['tables'][0]['rules'][i]['columns']}")
        rules_output = fileRead.rules_check(df,f"{yaml_data['databases'][0]['tables'][0]['rules'][i]['type']}")
        print(f"OUTPUT RULES {i+1} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(rules_output)
    print(config_path)