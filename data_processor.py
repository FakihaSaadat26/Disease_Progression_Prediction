"""
Simple Data Processor for Medical Data Analysis
Loads and analyzes ADMISSIONS and D_LABITEMS data
"""

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')


class DataAnalyzer:
    """Analyze medical admission and lab items data"""
    
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        self.admissions = None
        self.labitems = None
        
    def load_data(self):
        """Load ADMISSIONS and D_LABITEMS CSV files"""
        try:
            admissions_path = os.path.join(self.data_folder, 'ADMISSIONS.csv')
            labitems_path = os.path.join(self.data_folder, 'D_LABITEMS.csv')
            
            self.admissions = pd.read_csv(admissions_path)
            self.labitems = pd.read_csv(labitems_path)
            
            print(f"✓ Admissions loaded: {len(self.admissions)} records")
            print(f"✓ Lab Items loaded: {len(self.labitems)} records")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def get_admissions_summary(self):
        """Get basic statistics about admissions"""
        if self.admissions is None:
            return None
        
        return {
            'total_records': len(self.admissions),
            'columns': list(self.admissions.columns),
            'unique_patients': self.admissions['subject_id'].nunique() if 'subject_id' in self.admissions.columns else 'N/A',
            'memory_mb': self.admissions.memory_usage(deep=True).sum() / 1024**2
        }
    
    def get_labitems_summary(self):
        """Get basic statistics about lab items"""
        if self.labitems is None:
            return None
        
        return {
            'total_records': len(self.labitems),
            'columns': list(self.labitems.columns),
            'unique_items': self.labitems['itemid'].nunique() if 'itemid' in self.labitems.columns else 'N/A',
            'memory_mb': self.labitems.memory_usage(deep=True).sum() / 1024**2
        }
    
    def get_admissions_head(self, rows=100):
        """Get first N rows of admissions data"""
        if self.admissions is None:
            return None
        return self.admissions.head(rows).to_dict('records')
    
    def get_labitems_head(self, rows=100):
        """Get first N rows of lab items data"""
        if self.labitems is None:
            return None
        return self.labitems.head(rows).to_dict('records')
