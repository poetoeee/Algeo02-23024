import numpy as np
import os
from scipy.spatial.distance import cdist
from preprocess_query import preprocess_query_image

def compute_similarity(query_image_path, dataset_projected_data, output_folder):
    # preprocess query dlu
    preprocess_query_image(query_image_path, output_folder, eigenvectors_path='eigenvectors.npy', 
                           mean_vector_path='mean_vector.npy')
    projected_query = np.load(os.path.join(output_folder, "projected_query.npy"))

    # hitung jarak
    distances = cdist(projected_query, dataset_projected_data, metric='euclidean').flatten()

    # hitung persentase kemiripian (menggunakan max dan min)
    min_dist, max_dist = 0, distances.max()
    similarity_percentages = (1 - (distances - min_dist) / (max_dist - min_dist)) * 100

    similar_idx = np.where(similarity_percentages >= 65)[0]
    sorted_idx = similar_idx[np.argsort(similarity_percentages[similar_idx])][::-1]

    if len(sorted_idx) == 0:
        print("Tidak ada gambar yang mirip.")
    else:
        print(f"gambar dengan kemiripan diatas 65% terurut dari yang tertinggi:")
        for idx in sorted_idx:
            print(f"Image Index: {idx}, Distance: {distances[idx]:.2f}, Similarity: {similarity_percentages[idx]:.2f}%")

""" buat testing
    sorted_indices = np.argsort(distances)

    top_k = 5 
    closest_images_indices = sorted_indices[:top_k]

    print(f"{top_k} gambar paling mirip:")
    for idx in closest_images_indices:
        print(f"Index: {idx}, Distance: {distances[idx]:.2f}, Kemiripan: {similarity_percentages[idx]:.2f}%")
"""
if __name__ == "__main__":

    query_image_path = "query.jpg"
    dataset_projected_data = np.load("projected_imagesscipy.npy")
    eigenvectors = np.load("eigenvectorsscipy.npy")
    mean_vector = np.load("mean_vector.npy")
    output_folder = "queryfolder"

    compute_similarity(query_image_path, dataset_projected_data, output_folder)
