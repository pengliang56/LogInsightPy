from apps.service.MilvusClientBase import MilvusClientBase

host = "127.0.0.1"
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

milvus_client = MilvusClientBase(host=host, port=port, user=user, password=password, db_name=db_name, token=token)
