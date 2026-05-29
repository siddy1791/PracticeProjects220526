import yaml
from pathlib import Path
from db_connector import *
import json

class readConfig:

    def __init__(self,file_path):
        self.path = file_path

    def read_ymlfile(self):
        with open(self.path,"r") as ymlfile:
            data = yaml.safe_load(ymlfile)
            return data
        
    def rules_check(self,df,rule_config):
        rule_type = rule_config['type']
        print(f"<< RULE TYPE: {rule_type} >>")
        columns = rule_config['columns']
        print(f"<< COLUMNS: {columns} >>")
        
        if rule_type == "null_check":
            print("<<<<<<<<<<<<<<<< Null Check data::>>>>>>>>>")
            return df[df[columns].isnull().any(axis=1)]
        
        elif rule_type == 'duplicate_check':
            print("<<<<<<<<<<<<<<<<<<<<<<< duplicate check inside the dataframe :>>>>>>>>>>>>>>>>>>>>>")
            # return df[df[columns].duplicated()]
            return df[df.duplicated(subset=columns)]
        
        elif rule_type == 'value_range_check':
            print("<<<<<<<<<<<<<<<<<<<<<< Outlier checks inside the DF >>>>>>>>>>>>>>>>>>>>>>>>>")
            target_column = columns[0] # its best for single column

            max_val = rule_config['max']
            min_val = rule_config['min']

            return df[(df[target_column] > max_val) | (df[target_column] < min_val)]
        else:
            raise ValueError("NO rules matched")


if  __name__ == "__main__":
    final_result_op = []

    base_dir = Path(__file__).resolve().parent.parent       # >>>>>> ITS WINDOWS PATH
    validationRules_path = base_dir / "config" / "validation_rules.yaml"
    report_path = base_dir / "docs" / "validation_report.json"
    fileRead = readConfig(validationRules_path)
    yaml_data = fileRead.read_ymlfile()
    print(yaml_data)

    Database = yaml_data['databases'][0]['name']
    table_name = yaml_data['databases'][0]['tables'][0]['name']

    num_of_rules = len(yaml_data['databases'][0]['tables'][0]['rules'])
    df = db_connection('postgresql','psycopg2','admin','postgres123','localhost','5432','project1')
    for i in range(num_of_rules):
        final_result_op.append({'DataBase':Database,'TableName':table_name})
        rules_config = yaml_data['databases'][0]['tables'][0]['rules'][i]
        final_result_op[i]['rule_type'] = rules_config['type']
        final_result_op[i]['target_columns'] = rules_config['columns']
        final_result_op[i]['severity_level'] = rules_config['severity']
         
        rules_output = fileRead.rules_check(df,rules_config)
        print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< OUTPUT RULES {i+1} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        final_result_op[i]['Num_of_rows_failed'] = len(rules_output)
        failed_records = rules_output.to_dict(orient='records')
        if len(rules_output) == 0:
            final_result_op[i]["Failed_records"] = "NO FAILED RECORDS FOUND"
            final_result_op[i]['status'] = "WARNING"
        else:
            final_result_op[i]["Failed_records"] = failed_records
            final_result_op[i]['record_status'] = "PRESENT"
        print(final_result_op)

    with open(report_path,"w") as f:
        json.dump(final_result_op,f,indent=4,default=str)
        
