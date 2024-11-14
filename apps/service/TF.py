import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from MilvusClientBase import MilvusClientBase


class TfidfVectorizerWrapper:
    def __init__(self, max_features=32, dim=32):
        self.max_features = max_features
        self.dim = dim
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)

    def get_tfidf_vector(self, text: str):
        X = self.vectorizer.fit_transform([text])
        tfidf_vectors = X.toarray()
        tfidf_vectors = np.array(tfidf_vectors, dtype=np.float32)
        print(f"生成的TF-IDF向量维度: {tfidf_vectors.shape}")

        if tfidf_vectors.shape[1] < self.dim:
            padding = np.zeros((tfidf_vectors.shape[0], self.dim - tfidf_vectors.shape[1]), dtype=np.float32)
            tfidf_vectors = np.hstack((tfidf_vectors, padding))

        tfidf_vectors_list = tfidf_vectors.tolist()

        return tfidf_vectors_list

    def insert_log_data(text, app_code, app_instance, log_thread, ai_seari):
        vectorizer = TfidfVectorizerWrapper(max_features=32, dim=64)
        tfidf_vector = vectorizer.get_tfidf_vector(text)

        data = [
            tfidf_vector,
            [app_code],
            [app_instance],
            [log_thread],
            [ai_seari]
        ]


        host = "8.138.13.106"
        port = "19530"
        user = "TestUser"
        password = "TestUser"
        db_name = "TEST"
        token = "TestUser:TestUser"
        collection_name = "log_data"

        milvus_client = MilvusClientBase(host=host, port=port, user=user, password=password, db_name=db_name,
                                         token=token)

        milvus_client.insertList(collection_name=collection_name, data=data)

        print("数据已成功插入到 Milvus!")
