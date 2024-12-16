import numpy as np
import os

def normalize_data_manually(image_data):
    # jumlah gambar
    N = image_data.shape[0]
    mean_vector = np.sum(image_data, axis=0) / N

    #normalisasi dengan mean vector
    normalized_data = image_data - mean_vector

    return normalized_data, mean_vector

def save_normalized_data(normalized_data, mean_vector, data_file, mean_file):
    custom_path = r"src\backend\image\processing"
    np.save(os.path.join(custom_path, data_file), normalized_data)
    np.save(os.path.join(custom_path, mean_file), mean_vector)
    print(f"normalized data disave ke: {data_file}")
    print(f"Mean vector disave ke: {mean_file}")

if __name__ == "__main__":
    image_data = np.load("processed_imagestesnoimg2.npy")

    normalized_data, mean_vector = normalize_data_manually(image_data)
    save_normalized_data(normalized_data, mean_vector, "normalized_images.npy", "mean_vector.npy")

    print(f"normalized data shape: {normalized_data.shape}")
    print(f"Mean vector shape: {mean_vector.shape}")
