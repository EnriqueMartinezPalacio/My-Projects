import cv2
import glob
import os

def rotate_and_save_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)
        if os.path.isdir(folder_path):
            output_folder_path = os.path.join(output_folder, folder_name)
            os.makedirs(output_folder_path, exist_ok=True)

            for img in glob.glob(os.path.join(folder_path, "*.jpg")):
                print(folder_path)
                image = cv2.imread(img)
                height, width = image.shape[:2]

                for angle in range(0, 126, 7):  # Rotate 5 times, 25 degrees each time
                    # Get rotation matrix
                    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1.0)
                    # Apply rotation
                    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

                    output_path = os.path.join(output_folder_path, f"rotated_{angle}_{os.path.basename(img)}")
                    cv2.imwrite(output_path, rotated_image)

    print("Imágenes rotadas guardadas en las carpetas respectivas.")
    print(folder_path)

if __name__ == "__main__":
    input_folder = "C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Final/ROI/"
    output_folder = "C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Final/ROI/Rotated"

    rotate_and_save_images(input_folder, output_folder)

