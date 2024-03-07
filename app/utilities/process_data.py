import os
import pandas as pd
from dotenv import load_dotenv

class processor:

    final_dataframe: pd.DataFrame
    data_file_path: str

    def __init__(self):
        load_dotenv()
        self.data_file_path = os.environ["data_file_path"]
        
    def read_json(self,path:list):
        #read JSON into initial Dataframe
        df_list = []
        #Loop through list of json Paths to process
        for p in path:
            df = pd.read_json(self.data_file_path+"/"+p["filepath"])
            
            #Setup empty list to store processed data
            processed = []

            #loop through DF to process data
            for index, row in df.iterrows():
                #Call function to read the individual SKUs
                ret_sku = self.read_individual_sku(row)
                #add processed SKU to the processed data list
                processed += ret_sku

            #Convert processed data list to PD dataframe
            processed_df = pd.DataFrame.from_dict(processed)

            processed_df["source"]=p["database"]

            df_list.append(processed_df)
        
        #concatenate list of dat    aframe from each JSON
        result = pd.concat(df_list)

        #Count the appearances of the skus in the df
        processed_result = self.count_appearances(result)

        self.final_dataframe = processed_result
            
    def get_dataframe(self):
        return self.final_dataframe

    @staticmethod
    def count_appearances(df:pd.DataFrame):
        #get list of unique skus
        skus = df['sku'].unique()
        #query DF to count the values in the similar_sku col
        counts = df["similar_sku"].value_counts()
        #loop through list of unique skus
        for sku in skus:
            #Try to find the sku in the counts list, if not then set count  = 0
            try:
                df.loc[df["sku"] == sku,"count_appearances_as_similar_sku"] = int(counts[sku])
            except:
                df.loc[df["sku"] == sku,"count_appearances_as_similar_sku"] = 0
        return df
            


    # Function to read the individaul SKUS in the format 
    # {
    #         "sku": "RKKRCiFa",
    #         "most_similar":[{"similar_sku": "04aPZS5g","similarity_score": 1.0},...]
    # }
    @staticmethod
    def read_individual_sku(df_row):
        sku = df_row['sku']
        similar_sku = df_row['most_similar']

        sku_list = []

        # Sort most_similar list of sku's by score for Ranking
        similar_sku = sorted(similar_sku, key=lambda k: k['similarity_score'],reverse=True)
        rank = 1

        #Loop through similar skus
        for similar in similar_sku:

            #Create dictionary structure in the desired format  “sku”, “similar_sku”, “similarity_score”, and “rank”.
            temp_row = {
                "sku" : sku,
                "similar_sku" : similar["similar_sku"],
                "similarity_score" : similar["similarity_score"],
                "rank": rank
            }

            #Add row to sku list and increment rank
            sku_list.append(temp_row)
            rank += 1
        return sku_list


