from sklearn.feature_extraction.text import TfidfVectorizer
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections
import numpy as np
from TF import TfidfVectorizerWrapper
from MilvusClientBase import MilvusClientBase

host = "localhost"
port = "19530"
user = "TestUser"
password = "TestUser"
db_name = "TEST"
token = "TestUser:TestUser"
collection_name = "log_data"


text = "vectorization22222"
app_code = "app_001"
app_instance = "instance_001"
log_thread = "thread_001"
ai_seari = "AI Search"

TfidfVectorizerWrapper.insert_log_data(text, app_code, app_instance, log_thread, ai_seari);
# 创建 MilvusClient 实例
milvus_client = MilvusClientBase(host=host, port=port, user=user, password=password, db_name=db_name, token=token)

# 创建 MilvusClient 实例
text = "example search query"
print(milvus_client.queryVector(collection_name=collection_name,text=text,top_k=5));
