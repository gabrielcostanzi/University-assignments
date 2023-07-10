import os
import random
import shutil

# set the path to the source folder containing the images
path = 'dataset/train'

# set the path to the destination folder where the sampled images will be copied
dst_folder = 'dataset/train2'

# Define the class labels for each paste
class_labels = {
    "EOSINOPHIL": "EOSINOPHIL",
    "LYMPHOCYTE": "LYMPHOCYTE",
    "MONOCYTE": "MONOCYTE",
    "NEUTROPHIL": "NEUTROPHIL"
}

# set the number of images to sample
num_samples = 2000
for paste_name in os.listdir(path):
    if not os.path.isdir(os.path.join(path, paste_name)):
        continue
    class_label = class_labels[paste_name]
    # get a list of all the image files in the source folder
    image_files = [f for f in os.listdir(path+'/'+paste_name) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

    # randomly sample the specified number of images
    sampled_images = random.sample(image_files, num_samples)

    # create the destination folder if it doesn't already exist
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # copy the sampled images to the destination folder
    for image in sampled_images:
        src_path = os.path.join(path, paste_name, image)
        dst_path = os.path.join(dst_folder, class_label, image)
        shutil.copy(src_path, dst_path)
