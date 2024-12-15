import numpy as np
import os
from PIL import Image

def reconstruct_images(projected_data, eigenvectors, mean_vector, original_shape, output_dir):

    reconstructed_data = np.dot(projected_data, eigenvectors.T) + mean_vector
    num_images = reconstructed_data.shape[0]
    for i in range(num_images):
        image_array = reconstructed_data[i].reshape(original_shape)
        image_array = np.clip(image_array, 0, 255).astype(np.uint8)
        img = Image.fromarray(image_array, mode="L")
        img.save(os.path.join(output_dir, f"reconstructed_{i}.png"))

if __name__ == "__main__":

    projected_data = np.load("projected_imagesscipy.npy")
    eigenvectors = np.load("eigenvectorsscipy.npy") 
    mean_vector = np.load("mean_vector.npy") 
    original_shape = (400, 400)
    output_dir = "checkprojected"
    os.makedirs(output_dir, exist_ok=True)

    reconstruct_images(projected_data, eigenvectors, mean_vector, original_shape, output_dir)
    print(f"Reconstructed images saved to: {output_dir}")

