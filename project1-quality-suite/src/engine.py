import yaml
import json
from pathlib import Path
from src.rules import RULE_RIGISTRY

class DataQualityEngine:
    def __init__(self,config_path:Path):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self):
        try:
            with open(self.config_path,"r") as ymlfile:
                return yaml.safe_load(ymlfile)
        except Exception as e:
            print(f"CRITICAL: Failed to load configuration file at {self.config_path}: {e}")
            raise e
            
    def run_validation(self,df):
        final_report = []

        # Guard against completely malformed YAML structures
        if not self.config or 'databases' not in self.config:
            print("CRITICAL: Configuration is empty or missing 'databases' hierarchy root.")
            return final_report

        for db_entry in self.config.get('databases',[]):
            db_name = db_entry.get('name', 'UNKNOWN_DB')
            
            for table_entry in db_entry.get('tables',[]):
                table_name = table_entry.get('name', 'UNKNOWN_TABLE')

                for rule_config in table_entry.get('rules',[]):
                    rule_type = rule_config.get('type', 'UNKNOWN_RULE')
                    columns = rule_config.get('columns', [])
                    severity = rule_config.get('severity','error') # error handling. if severity is not passed in yaml then it defaults to error

                    print(f"🔄 Processing [{rule_type}] on {db_name}.{table_name}...")

                    status = "PASSED"
                    num_failed = 0
                    failed_records_payload = "NO FAILED RECORDS FOUND"
                    try:
                        # 1. Enforce validation structural rules before running
                        if not columns:
                            raise ValueError("The 'columns' definition is completely missing or empty.")
                        validator_func = RULE_RIGISTRY.get(rule_type)

                        if not validator_func:
                            raise NotImplementedError(f"Rule type '{rule_type}' is not registered in RULE_REGISTRY.")

                        print(f"Executing [{rule_type}] on {db_name}.{table_name}")
                        failed_rows_df = validator_func(df,rule_config)

                        num_failed = len(failed_rows_df)
                        if num_failed > 0:
                            status = "FAILED"
                            failed_records_payload = failed_rows_df.to_dict(orient='records')
                            
                            # Log alerts to console based on severity routing
                            if severity == "error":
                                print(f"SEVERITY ERROR: {num_failed} rows failed validation check.")
                            else:
                                print(f"SEVERITY WARNING: {num_failed} rows failed validation check.")
                                
                    except Exception as rule_error:
                        # TRAP THE CRASH: Isolate the exception to this rule block only
                        print(f"RULE EXECUTION CRASHED: {rule_error}")
                        status = "ERROR"
                        num_failed = -1  # Standard indicator representing execution processing error
                        failed_records_payload = f"RuntimeException: {str(rule_error)}"

                    result_item = {
                        "database":db_name,
                        "table_name":table_name,
                        "rule_type": rule_type,
                        "target_columns": columns,
                        "severity_level": severity,
                        "num_of_rows_failed": num_failed,
                        "status": status,
                        "failed_records": failed_records_payload
                    }

                    final_report.append(result_item)

        return final_report

        