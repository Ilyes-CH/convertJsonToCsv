import pandas as pd
import json
from pymongo import MongoClient, errors

class ConvertToCsv:
    """
    This class is dedicated to converting JSON files to CSV files for further data manipulation.
    If a JSON file is not available, it provides a method to fetch data from MongoDB.
    """

    @staticmethod
    def convert(jsonFileName, outputFileName) -> None:
        """
        Converts a flat JSON file to a CSV file.

        Parameters:
        jsonFileName (str): The name of the JSON file to be converted.
        outputFileName (str): The name of the output CSV file.
        
        Returns:
        None

        Raises:
        FileNotFoundError: If the JSON file does not exist.
        JSONDecodeError: If the JSON file is not a valid JSON.
        Exception: For any other unexpected errors.
        """
        try:
            # Load JSON file
            with open(jsonFileName, 'r') as file:
                data = json.load(file)
            # Convert to DataFrame
            df = pd.DataFrame(data)
            # Save to CSV file format
            df.to_csv(outputFileName, index=False, sep="\t")

            print("Conversion terminated")
        except FileNotFoundError:
            print(f"Error: The file '{jsonFileName}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{jsonFileName}' is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def convertNested(jsonFileName, outputFileName) -> None:
        """
        Converts a nested JSON file to a CSV file using normalization.

        Parameters:
        jsonFileName (str): The name of the nested JSON file to be converted.
        outputFileName (str): The name of the output CSV file.

        Returns:
        None

        Raises:
        FileNotFoundError: If the JSON file does not exist.
        JSONDecodeError: If the JSON file is not a valid JSON.
        Exception: For any other unexpected errors.
        """
        try:
            # Load JSON file
            with open(jsonFileName, 'r') as file:
                data = json.load(file)
            # Convert complex JSON formats to DataFrame
            df = pd.json_normalize(data)
            # Save to CSV file format
            df.to_csv(outputFileName, index=False, sep="\t")

            print("Conversion terminated")
        except FileNotFoundError:
            print(f"Error: The file '{jsonFileName}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{jsonFileName}' is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def saveDataFromMongo(uri, collection, db, output) -> None:
        """
        Fetches data from a MongoDB collection and saves it as a CSV file.

        Parameters:
        uri (str): The MongoDB URI.
        collection (str): The name of the MongoDB collection.
        db (str): The name of the MongoDB database.
        output (str): The name of the output CSV file.

        Returns:
        None

        Raises:
        ValueError: If the specified database or collection does not exist, or if no documents are found.
        ServerSelectionTimeoutError: If unable to connect to the MongoDB server.
        Exception: For any other unexpected errors.
        """
        try:
            # Connect to MongoDB
            client = MongoClient(uri)
            database = client[db]

            # Check if the database exists
            if db not in client.list_database_names():
                raise ValueError(f"Database '{db}' not found.")

            coll = database[collection]

            # Check if the collection exists
            if collection not in database.list_collection_names():
                raise ValueError(f"Collection '{collection}' not found.")

            # Fetch documents from the collection
            documents = list(coll.find())

            if not documents:
                raise ValueError("No documents found in the collection.")

            # Convert documents to DataFrame
            df = pd.json_normalize(documents)

            # Save DataFrame to CSV
            df.to_csv(output, index=False, sep="\t")

            print("MongoDB data has been successfully converted to CSV.")
        except ValueError as e:
            print(f'Error: {e}')
        except errors.ServerSelectionTimeoutError:
            print("Error: Unable to connect to the MongoDB server. Please check your connection settings.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example usage:
# converter = ConvertToCsv()
# converter.convert("db.json", "db.csv")
