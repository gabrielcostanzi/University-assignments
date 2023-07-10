import os

# Define the path of the directory containing the image pastes
path = "dataset/train"

# Define the class labels for each paste
class_labels = {
    "EOSINOPHIL": "eosinophil",
    "LYMPHOCYTE": "lymphocyte",
    "MONOCYTE": "monocyte",
    "NEUTROPHIL": "neutrophil"

}

# Iterate through the pastes and rename each image
for paste_name in os.listdir(path):
    if not os.path.isdir(os.path.join(path, paste_name)):
        continue
    class_label = class_labels[paste_name]
    i = 1
    for filename in os.listdir(os.path.join(path, paste_name)):
        if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
            # Construct the new file name
            new_name = f"{i}.jpeg"
            i += 1
            
            # Rename the image
            os.rename(os.path.join(path, paste_name, filename), os.path.join(path, paste_name, new_name))
