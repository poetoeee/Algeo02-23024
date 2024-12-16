import numpy as np
import os
from image.vectorize import process_images
from image.normalize import normalize_data_manually, save_normalized_data
from image.pcasvd import compute_svd, project_data, save_data
from image.similaritycomputation import compute_similarity

def process_dataset(input_folder, save_path):
    # bikin vektor
    image_vectors = process_images(input_folder, save_path)
    
    # normalize
    normalized_data, mean_vector = normalize_data_manually(image_vectors)
    save_normalized_data(normalized_data, mean_vector, "normalized_data.npy", "mean_vector.npy")
    
    # PCA
    eigenvectors, singular_values = compute_svd(normalized_data) #k bisa diubah
    projected_data = project_data(normalized_data, eigenvectors)
    save_data(projected_data, eigenvectors, singular_values)
    print("Dataset selesai diproses.")

def handle_query(query_image_path):
    dataset_projected_data = np.load(r"src\backend\image\processing\projected.npy")

    output_folder = r"src\backend\image\queryfolder"
    dataset_folder = os.path.join(r"src\backend\image\database_image")
    
    res = compute_similarity(query_image_path, dataset_projected_data, output_folder, dataset_folder)
    return res

if __name__ == "__main__":
    dataset_folder = os.path.join(r"src\backend\image\database_image")
    # dataset_folder = "dataset"
    save_path = "processed_data.npy"


    process_dataset(dataset_folder, save_path)
    query_image_path = "query.jpg"
    handle_query(r"src\backend\image\query\(1).jpg")
