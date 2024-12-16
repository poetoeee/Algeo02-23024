import numpy as np
import os
from scipy.spatial.distance import cdist
from image.preprocess_query import preprocess_query_image

def compute_similarity(query_image_path, dataset_projected_data, output_folder, dataset_folder):
    dataset_file_names = [f for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
    dataset_file_names.sort() 
    
    # Preprocess query dlu
    preprocess_query_image(query_image_path, output_folder, eigenvectors_path=r'src\backend\image\processing\eigenvectors.npy', 
                           mean_vector_path=r'src\backend\image\processing\mean_vector.npy')
    projected_query = np.load(os.path.join(output_folder, "projected_query.npy"))

    # hitung jarak
    distances = cdist(projected_query, dataset_projected_data, metric='euclidean').flatten()

    # hitung persentase kemiripian (menggunakan max dan min)
    min_dist, max_dist = 0, distances.max()
    similarity_percentages = (1 - (distances - min_dist) / (max_dist - min_dist))

    similarity_dict = {dataset_file_names[idx]: similarity_percentages[idx] 
                        for idx in range(len(dataset_file_names)) 
                        if similarity_percentages[idx] >= 0.65}

    if not similarity_dict:
        top_3_indices = np.argsort(similarity_percentages)[-3:][::-1]
        similarity_dict = {dataset_file_names[idx]: similarity_percentages[idx] for idx in top_3_indices}

    sorted_similarity_dict = {k: v for k, v in sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)}

    return sorted_similarity_dict

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
