import concurrent.futures
import os
from typing import List, Union

import dotenv
import numpy as np
import oceandb
import pandas as pd
import pyarrow.parquet as pq
from oceandb.utils.embedding_functions import ImageBindEmbeddingFunction
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_random_exponential


# Embedding functions for different modalities
text_embedding_function = ImageBindEmbeddingFunction(modality="text")
vision_embedding_function = ImageBindEmbeddingFunction(modality="vision")
audio_embedding_function = ImageBindEmbeddingFunction(modality="audio")


class Elysium:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def get_embedding(self, data: Union[str, Image.Image], data_type: str) -> List[float]:
        if data_type == 'text':
            return text_embedding_function.embed(data)
        elif data_type == 'image':
            return vision_embedding_function.embed(data)
        elif data_type == 'audio':
            return audio_embedding_function.embed(data)
        elif data_type == 'video':
            # Implement video embedding generation using an appropriate pre-trained model
            pass
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def read_csv_file(self):
        self.df = pd.read_csv(self.file_path)
        for index, row in self.df.iterrows():
            if row['DataType'] in ['image', 'audio', 'video']:
                file_path = row['Data']
                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")

    def generate_embeddings(self):
        embeddings = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_embedding = {executor.submit(self.get_embedding, row['Data'], row['DataType']): row for _, row in self.df.iterrows()}
            for future in concurrent.futures.as_completed(future_to_embedding):
                embeddings.append(future.result())
                print(len(embeddings), end='\r')
        self.df['Embedding'] = embeddings

    def save_to_parquet(self):
        parquet_file_name = self.file_path.replace('.csv', '.parquet')
        self.df.to_parquet(parquet_file_name)

    def verify_embeddings(self):
        parquet_file_name = self.file_path.replace('.csv', '.parquet')
        table = pq.read_table(parquet_file_name)
        df = table.to_pandas()
        print(df.head())


if __name__ == "__main__":
    file_path = 'path_to_your_file.csv'
    elysium = Elysium(file_path)
    elysium.read_csv_file()
    elysium.generate_embeddings()
    elysium.save_to_parquet()
    elysium.verify_embeddings()