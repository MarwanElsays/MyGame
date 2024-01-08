from PIL import Image
import os

colors = {(255, 255, 255):(0, 0, 0)}

def change_color(image_path,output_path):
    # Open the image
    img = Image.open(image_path)

    # Convert the image to RGB mode (if it's not already)
    img = img.convert("RGB")

    # Get the image data
    pixels = img.load()

    # Define a function to replace old_color with new_color
    def replace_color(pixel):
        
        if pixel in colors:
            return colors[pixel]
        return pixel

    # Iterate through each pixel and replace the color
    for i in range(img.width):
        for j in range(img.height):
            pixels[i, j] = replace_color(pixels[i, j])

    # Save the modified image
    img.save(output_path)


def change_color_folder(folder_path,output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Construct full paths
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)

            # Apply color change to each image
            change_color(input_path,output_path)


if __name__ == "__main__" :
    input_folder_path = "C:/Users/MARWAN/Desktop/Programing/Python/srengaGame/Assets/Images/tiles"
    output_folder_path = "C:/Users/MARWAN/Desktop/Programing/Python/srengaGame/Assets/Images/tiles"
    
    change_color_folder(input_folder_path, output_folder_path)
    
    #change_color("C:/Users/MARWAN/Desktop/Programing/Python/srengaGame/Assets/Images/tiles/Alien/ground_1.png","output_path.png")

