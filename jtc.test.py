import unittest
import os
import json
import pandas as pd
from JsonToCsv import ConvertToCsv
from colorama import init, Fore

init(autoreset=True)

class TestConvertToCsv(unittest.TestCase):

    def setUp(self):
        # Create a sample JSON file for testing
        self.json_file = 'test.json'
        self.csv_file = 'output.csv'
        self.sample_data = [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "555-555-5555",
                "password": "password123"
            },
            {
                "id": 2,
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "phone": "555-555-1234",
                "password": "password456"
            }
        ]
        
        with open(self.json_file, 'w') as f:
            json.dump(self.sample_data, f)


    def test_convert(self):
        # Call the convert method
        ConvertToCsv.convert(self.json_file, self.csv_file)
        
        # Verify that the output CSV file exists
        self.assertTrue(os.path.exists(self.csv_file))
        
        # Verify the contents of the CSV file
        df = pd.read_csv(self.csv_file, sep='\t')
        
        # Check the data in the DataFrame
        self.assertEqual(df.shape[0], 2)  
        self.assertEqual(df.shape[1], 6)  
        
        # Check the data values
        self.assertEqual(df.iloc[0]['id'], 1)
        self.assertEqual(df.iloc[0]['first_name'], 'John')
        self.assertEqual(df.iloc[0]['last_name'], 'Doe')
        self.assertEqual(df.iloc[0]['email'], 'john.doe@example.com')
        self.assertEqual(df.iloc[0]['phone'], '555-555-5555')
        self.assertEqual(df.iloc[0]['password'], 'password123')

        self.assertEqual(df.iloc[1]['id'], 2)
        self.assertEqual(df.iloc[1]['first_name'], 'Jane')
        self.assertEqual(df.iloc[1]['last_name'], 'Smith')
        self.assertEqual(df.iloc[1]['email'], 'jane.smith@example.com')
        self.assertEqual(df.iloc[1]['phone'], '555-555-1234')
        self.assertEqual(df.iloc[1]['password'], 'password456')

        print(Fore.GREEN + "Test passed successfully")
         
    def tearDown(self):
        # Remove the sample JSON file and output CSV file after tests
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

if __name__ == '__main__':
    unittest.main()
