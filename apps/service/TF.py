import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from MilvusClientBase import MilvusClientBase


class TfidfVectorizerWrapper:
    def __init__(self, max_features=32, dim=32):
        """
        初始化 TF-IDF 向量化器
        :param max_features: 设置最大特征数，默认是 32
        :param dim: 设置目标维度，默认是 32
        """
        self.max_features = max_features
        self.dim = dim
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)

    def get_tfidf_vector(self, text: str):
        """
        传入字符串，返回对应的 TF-IDF 向量
        :param text: 输入的字符串文本
        :return: 填充后的 TF-IDF 向量
        """
        # 使用 TF-IDF 向量化器处理文本
        X = self.vectorizer.fit_transform([text])  # 传递单个字符串
        tfidf_vectors = X.toarray()
        tfidf_vectors = np.array(tfidf_vectors, dtype=np.float32)
        print(f"生成的TF-IDF向量维度: {tfidf_vectors.shape}")

        # 如果 TF-IDF 向量的维度小于目标维度，则进行零填充
        if tfidf_vectors.shape[1] < self.dim:
            padding = np.zeros((tfidf_vectors.shape[0], self.dim - tfidf_vectors.shape[1]), dtype=np.float32)
            tfidf_vectors = np.hstack((tfidf_vectors, padding))  # 填充到右边

        # 转换为 list of lists 格式
        tfidf_vectors_list = tfidf_vectors.tolist()

        return tfidf_vectors_list

    def insert_log_data(text, app_code, app_instance, log_thread, ai_seari):
        """
        插入日志数据到 Milvus 数据库
        :param text: 日志文本，生成 TF-IDF 向量
        :param app_code: 应用代码
        :param app_instance: 应用实例
        :param log_thread: 日志线程
        :param ai_seari: AI 相关的查询
        :return: None
        """
        # 实例化 TfidfVectorizerWrapper，设定特征数和维度
        vectorizer = TfidfVectorizerWrapper(max_features=32, dim=64)

        # 使用 TfidfVectorizerWrapper 生成向量
        tfidf_vector = vectorizer.get_tfidf_vector(text)

        # 构建插入数据的格式
        data = [
            tfidf_vector,  # 生成的 TF-IDF 向量
            [app_code],  # app_code
            [app_instance],  # app_instance
            [log_thread],  # log_thread
            [ai_seari]  # ai_seari
        ]

        # 配置 Milvus 连接信息
        # 配置连接信息
        host = "8.138.13.106"
        port = "19530"
        user = "TestUser"
        password = "TestUser"
        db_name = "TEST"
        token = "TestUser:TestUser"  # 如果没有 token，可以传空字符串
        collection_name = "log_data"

        # 创建 MilvusClient 实例
        milvus_client = MilvusClientBase(host=host, port=port, user=user, password=password, db_name=db_name,
                                         token=token)

        milvus_client.insertList(collection_name=collection_name, data=data)

        print("数据已成功插入到 Milvus!")
