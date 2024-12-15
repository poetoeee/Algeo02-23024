import numpy as np
from vectorize import process_images
from normalize import normalize_data_manually, save_normalized_data
from pcasvd import compute_svd, project_data, save_data
from similaritycomputation import compute_similarity

def process_dataset(input_folder, output_folder, save_path):
    # bikin vektor
    image_vectors = process_images(input_folder, output_folder, save_path)
    
    # normalize
    normalized_data, mean_vector = normalize_data_manually(image_vectors)
    save_normalized_data(normalized_data, mean_vector, "normalized_data.npy", "mean_vector.npy")
    
    # PCA
    eigenvectors, singular_values = compute_svd(normalized_data, k=50) #k bisa diubah
    projected_data = project_data(normalized_data, eigenvectors)
    save_data(projected_data, eigenvectors, singular_values)
    print("Dataset selesai diproses.")

def handle_query(query_image_path):
    dataset_projected_data = np.load("projected.npy")

    output_folder = "queryfolder"
    compute_similarity(query_image_path, dataset_projected_data, output_folder, dataset_folder)

if __name__ == "__main__":
    dataset_folder = "dataset"
    output_folder = "integfiles"
    save_path = "processed_data.npy"

    process_dataset(dataset_folder, output_folder, save_path)
    query_image_path = "query.jpg"
    handle_query(query_image_path)
