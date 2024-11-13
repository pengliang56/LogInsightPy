from typing import List

from pymilvus import Collection, connections
from pymilvus.exceptions import MilvusException
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class MilvusClientBase:
    def __init__(self, host: str, port: str, user: str, password: str, db_name: str, token: str = ""):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.token = token
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = connections.connect(
                alias="default",
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db_name=self.db_name,
                token=self.token
            )
            print(f"[SUCCESS] Success connect Milvus service: {self.host}:{self.port}")
        except MilvusException as e:
            print(f"[ERROR] Connect Milvus service fail: {e}")
            raise

    def query(self, collection_name: str, expr: str, output_fields: list = None, limit: int = 10):
        """
        查询指定 collection 中的数据
        :param collection_name: Collection 名称
        :param expr: 查询表达式
        :param output_fields: 要返回的字段列表
        :param limit: 查询结果的数量限制
        :return: 查询结果
        """

        try:
            collection = Collection(name=collection_name)  # 获取 Collection 实例
            results = collection.query(expr=expr, output_fields=output_fields, limit=limit)
            return results
        except MilvusException as e:
            print(f"查询失败: {e}")
            return []

    def insert(self, collection_name: str, data: dict):
        try:
            # 获取 Collection 实例
            collection = Collection(name=collection_name)
            # 插入数据
            result = collection.insert(data)
            print(f"成功插入 {len(data['id'])} 条数据.")
            return result
        except MilvusException as e:
            print(f"插入数据失败: {e}")
            return None

    def insertList(self, collection_name: str, data: list):
        try:
            # 获取 Collection 实例
            collection = Collection(name=collection_name)
            # 插入数据
            result = collection.insert(data)
            print(f"成功插入 {len(data[0])} 条数据.")
            return result
        except MilvusException as e:
            print(f"插入数据失败: {e}")
            return None

    def disconnect(self):
        """断开 Milvus 连接"""
        if self.connection:
            connections.disconnect("default")
            print("已断开 Milvus 连接。")
        else:
            print("没有连接 Milvus 服务。")

    def get_tfidf_vector(self, text: str, max_features=32, dim=32):

        # 初始化 TF-IDF 向量化器
        vectorizer = TfidfVectorizer(max_features=max_features)

        # 使用 TF-IDF 向量化器处理文本
        X = vectorizer.fit_transform([text])  # 传递单个字符串
        tfidf_vectors = X.toarray()
        tfidf_vectors = np.array(tfidf_vectors, dtype=np.float32)
        print(f"生成的TF-IDF向量维度: {tfidf_vectors.shape}")

        # 如果 TF-IDF 向量的维度小于目标维度，则进行零填充
        if tfidf_vectors.shape[1] < dim:
            padding = np.zeros((tfidf_vectors.shape[0], dim - tfidf_vectors.shape[1]), dtype=np.float32)
            tfidf_vectors = np.hstack((tfidf_vectors, padding))  # 填充到右边

        # 转换为 list of lists 格式
        tfidf_vectors_list = tfidf_vectors.tolist()

        return tfidf_vectors_list

    def queryVector(self, collection_name: str, text: str, top_k=5):

        try:

            query_vector = self.get_tfidf_vector(text, 32, 64);
            collection = Collection(name=collection_name)

            results = collection.search(
                data=query_vector,  # 转换为列表格式，确保符合 Milvus 接受的格式
                anns_field="vector",  # 查询的字段（存储向量的字段）
                param={"metric_type": "L2", "params": {"nprobe": 10}},  # 使用 L2 距离计算
                limit=top_k  # 返回最相似的前 top_k 条数据
            )

            return results

        except MilvusException as e:
            print(f"查询失败: {e}")
            return []
