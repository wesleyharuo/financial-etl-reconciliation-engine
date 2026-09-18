# ==========================================
# M&A FINANCIAL RECONCILIATION & ETL ENGINE
# Developed by Wesley Kurosawa (NextLens Data)
# Target: Financial Systems & Bank Data Integration
# ==========================================

import pandas as pd
import sqlite3
import logging
from datetime import datetime

# Configure Logging for Audit Trail
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_financial_etl():
    logging.info("Starting automated financial ETL and reconciliation pipeline...")
    
    # 1. Extraction Phase (Simulating transactional and General Ledger extracts)
    # In a bank setting, this connects via secure SQL or Snowflake/SAP connectors
    try:
        # Creating mock dataframes for demonstration if files don't exist yet
        data_tx = {
            'tx_id': [101, 102, 103, 104],
            'account_id': ['ACC-5001', 'ACC-5002', 'ACC-5001', 'ACC-5003'],
            'tx_date': ['2026-09-01', '2026-09-01', '2026-09-02', '2026-09-02'],
            'debit': [1500.00, 3200.50, 450.00, 12000.00],
            'credit': [0.00, 0.00, 0.00, 0.00]
        }
        data_gl = {
            'account_id': ['ACC-5001', 'ACC-5002', 'ACC-5003'],
            'gl_balance': [1950.00, 3200.50, 12000.00] # ACC-5001 has a intentional discrepancy for audit demo
        }
        
        df_transactions = pd.DataFrame(data_tx)
        df_gl = pd.DataFrame(data_gl)
        
    except Exception as e:
        logging.error(f"Error loading source files: {e}")
        return

    # 2. Transformation & Cleaning Phase
    logging.info("Cleaning records and applying standard Canadian numeric conventions...")
    df_transactions.drop_duplicates(inplace=True)
    df_gl.drop_duplicates(inplace=True)
    
    df_transactions['tx_date'] = pd.to_datetime(df_transactions['tx_date'])
    
    # Aggregate transactions by account
    tx_aggregated = df_transactions.groupby('account_id')['debit'].sum().reset_index()
    
    # 3. Automated Reconciliation Matching (Operational vs. General Ledger)
    reconciliation_summary = pd.merge(
        tx_aggregated,
        df_gl,
        on='account_id',
        how='outer'
    ).fillna(0)
    
    reconciliation_summary['discrepancy'] = reconciliation_summary['debit'] - reconciliation_summary['gl_balance']
    
    # Flagging variances for compliance review
    discrepancies = reconciliation_summary[reconciliation_summary['discrepancy'].abs() > 0.01]
    
    if not discrepancies.empty:
        logging.warning(f"Audit Alert: Found {len(discrepancies)} account(s) with unreconciled variances.")
        print(discrepancies)
    else:
        logging.info("Reconciliation complete. Zero material variances detected.")
        
    # 4. Load Phase (Exporting to analytical SQLite database)
    conn = sqlite3.connect('financial_audit_2026.db')
    reconciliation_summary.to_sql('reconciliation_results', conn, if_exists='replace', index=False)
    conn.close()
    logging.info("Data successfully loaded into analytical database storage.")

if __name__ == "__main__":
    run_financial_etl()
