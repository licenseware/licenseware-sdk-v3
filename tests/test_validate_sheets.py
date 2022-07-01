import unittest
from licenseware.utils.file_validators import validate_sheets, validate_rows_number, GeneralValidator, validate_columns


# python3 -m unittest tests/test_validate_sheets.py


class TestSheetsValidator(unittest.TestCase):


    def test_sheets_validator_simple_sheets(self):

        filepath = "./test_files/RVTools.xlsx"

        assert validate_sheets(file=filepath, required_sheets=[
          'tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'  
        ])

        with self.assertRaises(ValueError):
            validate_sheets(file=filepath, required_sheets=[
                'non-existent-tab'  
            ])

    def test_sheets_validator_alternative_sheets(self):

        filepath = "./test_files/RVTools.xlsx"

        assert validate_sheets(file=filepath, required_sheets=[
            ('tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'),
            ('vInfo', 'vCPU', 'vHost', 'vCluster'),
        ])

        with self.assertRaises(ValueError):
            validate_sheets(file=filepath, required_sheets=[
            ('tabvInfoMissing', 'tabvCPU', 'tabvHost', 'tabvCluster'),
            ('vInfoMissing', 'vCPU', 'vHost', 'vCluster'),
        ])

    
    def test_validate_rows_number(self):

        filepath = "./test_files/RVTools.xlsx"

        df = GeneralValidator(input_object=filepath)._parse_excel()

        assert isinstance(df, dict) 
        assert len(df) > 1 

        assert validate_rows_number(df, min_rows_number=12)
        assert validate_rows_number(df, min_rows_number=12, required_sheets=['tabvInfo'])

        with self.assertRaises(ValueError):
            validate_rows_number(df, min_rows_number=100000000)

        with self.assertRaises(ValueError):
            validate_rows_number(df, min_rows_number=100000000, required_sheets=['tabvInfo'])

        

    def test_validate_columns(self):
        import pandas as pd

        filepath = "./test_files/RVTools.xlsx"
        df = pd.read_excel(filepath)

        assert validate_columns(df, required_columns=['VM', 'Host', 'OS'])

        with self.assertRaises(ValueError):
            validate_columns(df, required_columns=['NON-EXISTENT'])




        

