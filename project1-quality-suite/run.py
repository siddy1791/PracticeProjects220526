import json
from datetime import datetime, timezone
from pathlib import Path
from src.db_connector import *
from src.engine import *

def main():
    # 1. Setup dynamic projects path
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "validation_rules.yaml"
    report_output_path = base_dir / "docs" / "validation_report.json"

    print("Initializing Data Quality suite Orchestrator......")

    # 2. Instantiate our validation orchestrator engine
    dq_engine = DataQualityEngine(config_path)

    # 3. Pull the target database name dynamically from the YAML config structure
    # (Defaulting to 'project1' if not declared)
    target_db = dq_engine.config['databases'][0]['name'] if dq_engine.config.get('databases') else 'project1'

    # 4. Extract data safely once using the secure environment connector
    df = db_connection(target_db)

    # 5. Run execution matrix
    report_data = dq_engine.run_validation(df)

    execution_summary = {
        "Project_name" : "Project 1 Quality suite",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "total_rules_run": len(report_data),
        "results": report_data
    }

    report_output_path.parent.mkdir(parents=True,exist_ok=True)
    with open(report_output_path,"w") as f:
        json.dump(execution_summary,f,indent=4,default=str)

    print(f"✅ Data Quality Suite run complete! Report saved to: {report_output_path}")

if __name__ == '__main__':
    main()
