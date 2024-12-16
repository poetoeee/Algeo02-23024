import numpy as np
from scipy.sparse.linalg import svds

def compute_svd(data, k=None, fraction = 0.5, max_k = 50): #data - normalized data, k yang dikeep

    num_images = data.shape[0]
    if k is None:
        k = max(1, int(fraction * num_images))
        k = min(k, max_k, num_images)

    covariance_matrix = np.dot(data, data.T) / data.shape[1]

    # svd
    eigenvectors_sample, singular_values, _ = svds(covariance_matrix, k=k)

    # ini balikin biar k dari terbesar (svds spicy return yng paling kecil (ga perlu yng kecil))
    eigenvectors_sample = eigenvectors_sample[:, ::-1]
    singular_values = singular_values[::-1]

    # Transfor eigenvector dari sample ke feature space
    eigenvectors_feature = np.dot(data.T, eigenvectors_sample)
    eigenvectors_feature = eigenvectors_feature / np.linalg.norm(eigenvectors_feature, axis=0)
    print(f"PCA selesai, k = {k}")

    return eigenvectors_feature, singular_values



def project_data(data, eigenvectors):
    return np.dot(data, eigenvectors)

def save_data(projected_data, eigenvectors, singular_values):
    np.save("projected.npy", projected_data)
    np.save("eigenvectors.npy", eigenvectors)
    np.save("svd.npy", singular_values)



if __name__ == "__main__":
    normalized_data = np.load("normalized_images.npy")
    # k = 50
    eigenvectors, singular_values = compute_svd(normalized_data) #k bisa diubah
    projected_data = project_data(normalized_data, eigenvectors)

    save_data(projected_data, eigenvectors, singular_values)
    print("hasil pca selesai disimpan.")
