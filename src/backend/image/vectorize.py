import os
import numpy as np
from PIL import Image

def resize(image, image2):
    src_h, src_w = image.shape
    target_h, target_w = image2
    resized = np.zeros((target_h, target_w), dtype=np.float32)

    scale_h = src_h / target_h
    scale_w = src_w / target_w

    for y in range(target_h):
        for x in range(target_w):
            src_y = int(y * scale_h)
            src_x = int(x * scale_w)
            resized[y, x] = image[src_y, src_x]

    return resized

def process_images(input_folder, save_path, size=(400, 400)): #output folder bekas testing
    #input folder -> input gambar, save_path -> output npy proses
    #os.makedirs(output_folder, exist_ok=True) tidak diperlukan, untuk testing awal saja
    image_vectors = []
    filenames = sorted([f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))])

    for filename in filenames:
            # buka gambar
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            # grayscale
            grayscale = img.convert('RGB')
            grayscale = np.array(grayscale)
            grayscale = 0.2989 * grayscale[:, :, 0] + 0.5870 * grayscale[:, :, 1] + 0.1140 * grayscale[:, :, 2]

            resized_array = resize(grayscale, size)

            """ bekas juga
            grayscale_image = Image.fromarray(resized_array).convert('L')
            save_img_path = os.path.join(output_folder, filename)
            grayscale_image.save(save_img_path)
            """

            # 1d
            flattened = resized_array.flatten()
            image_vectors.append(flattened)

    # Save ke npy
    image_vectors = np.array(image_vectors)
    np.save(save_path, image_vectors)
    print(f"data proses disave ke: {save_path}")
    return image_vectors

#input_dir =  r"D:\Skool\univ\algeo2\dataset"
#output_dir = r"D:\Skool\univ\algeo2\datasetprocessednpytesnoimg2"
#save_file = "processed_imagestesnoimg2.npy"

#image_data = process_images(input_dir, output_dir, save_file)