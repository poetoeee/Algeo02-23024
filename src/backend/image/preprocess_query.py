import numpy as np
from PIL import Image
from image.vectorize import resize
from image.pcasvd import project_data
import os

def preprocess_image(image_path, size=(400, 400)):
    image = Image.open(image_path).convert("L")
    image_array = np.array(image)
    resized_image = resize(image_array, size) 
    flattened_image = resized_image.flatten()
    
    return flattened_image

def preprocess_query_image(input_image_path, output_folder, eigenvectors_path, mean_vector_path, size=(400, 400)):
    #proses awal
    query_image = preprocess_image(input_image_path, size)
    eigenvectors = np.load(eigenvectors_path)
    mean_vector = np.load(mean_vector_path)

    #normalisasi dengan dataset
    normalized_query = query_image.reshape(1, -1)
    normalized_query = normalized_query - mean_vector
    projected_query = project_data(normalized_query, eigenvectors)#projeksi

    # save
    os.makedirs(output_folder, exist_ok=True)
    np.save(os.path.join(output_folder, "processed_query.npy"), normalized_query)
    np.save(os.path.join(output_folder, "projected_query.npy"), projected_query)

    print(f"hasil proses query disave ke {output_folder}")

if __name__ == "__main__":
    input_image_path = "query.jpg"
    output_folder = "query"
    eigenvectors_path = "eigenvectorsscipy.npy"
    mean_vector_path = "mean_vector.npy"
    projected_data_path = "projected_imagesscipy.npy"

    preprocess_query_image(input_image_path, output_folder, eigenvectors_path, mean_vector_path, projected_data_path)
