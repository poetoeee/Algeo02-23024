import numpy as np
from PIL import Image
import os

def reconstruct(npy_file, output_folder, image_size=(400, 400)):
    os.makedirs(output_folder, exist_ok=True)
    
    image_data = np.load(npy_file)
    num_images = image_data.shape[0]
    
    for i, flattened_image in enumerate(image_data):
        reconstructed_image = flattened_image.reshape(image_size)
        img = Image.fromarray(reconstructed_image).convert('L')
        img_path = os.path.join(output_folder, f"reconstructed_image_{i+1}.jpg")
        img.save(img_path)
        print(f"Saved: {img_path}")
    
    print(f"Reconstructed {num_images} images to {output_folder}")


npy_file = "normalized_images.npy"
output_dir = r"D:\Skool\univ\algeo2\processed"
reconstruct(npy_file, output_dir)


#input_dir = r"D:\Skool\univ\algeo2\dataset"
#output_dir = r"D:\Skool\univ\algeo2\dataprocessednpy"