# kmeans_example.py
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# 1. 生成示例数据（两维）
np.random.seed(0)
data = np.vstack([
    np.random.randn(50, 2) + np.array([0, 0]),   # 第一类
    np.random.randn(50, 2) + np.array([5, 5]),   # 第二类
    np.random.randn(50, 2) + np.array([0, 6])    # 第三类
])

# 2. 创建 KMeans 模型
kmeans = KMeans(n_clusters=3, random_state=0)

# 3. 训练
kmeans.fit(data)

# 4. 获取聚类标签与中心点
labels = kmeans.labels_
centers = kmeans.cluster_centers_

# 5. 打印结果
print("聚类标签前10个：", labels[:10])
print("聚类中心：\n", centers)

# 6. 画结果图
plt.scatter(data[:, 0], data[:, 1], c=labels, s=30)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', s=200)
plt.title("KMeans Clustering Example")
plt.show()
