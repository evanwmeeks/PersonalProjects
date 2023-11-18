from PIL import Image
import os
import boto3
import pytesseract
import shutil

session = boto3.Session(profile_name="default")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

s3 = boto3.resource('s3',
                    endpoint_url='https://s3.US-central-1.wasabisys.com',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key
                    )

# Get bucket object
mpdb = s3.Bucket('mpdb')


def resize_images_in_directory(input_directory, output_directory, max_size):
    """
    Resizes all images in a given directory to a maximum size.

    Args:
        input_directory (str): The directory containing the images you wish to resize.
        output_directory (str): The directory in which you wish to place the resized photos.
        max_size (int): The number in pixels you wish to have as the maximum photo size.
                        Used for both width and height.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Get a list of all files in the input directory
    file_list = os.listdir(input_directory)

    # Loop through each file in the input directory
    Count = 0
    for file_name in file_list:
        Count += 1
        # Construct the full path of the input and output files
        input_path = os.path.join(input_directory, file_name)
        output_path = os.path.join(output_directory, file_name)

        # Check if the file is an image
        if is_image_file(input_path):
            try:
                # Resize the image and save it to the output directory
                resize_image(input_path, output_path, max_size)
                if Count % 1000 == 0:
                    itemPath = input_path.split(".")[0]
                    itemName = itemPath.split("/")[-1]
                    print(f"{itemName} resized: Record {Count}")
            except Exception as e:
                print(f"Error resizing file: {file_name} - {str(e)}")


def is_image_file(file_path):
    """
    Checks if a file has a supported image extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file has a supported image extension, False otherwise.
    """
    # Check if the file has a supported image extension
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in supported_extensions


def resize_image(input_path, output_path, max_size):
    """
    Resizes an image to fit within a maximum size while preserving its aspect ratio.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the resized image.
        max_size (int): The maximum size (in pixels) for both width and height.
    """
    # Open the image file
    image = Image.open(input_path)

    # Convert the image to RGB mode if it is in RGBA mode
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Calculate the aspect ratio
    width, height = image.size
    aspect_ratio = width / height

    # Determine the new dimensions
    if width > height:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)
    else:
        new_width = int(max_size * aspect_ratio)
        new_height = max_size

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Save the resized image as JPEG
    resized_image.save(output_path, 'JPEG')


def count_wasabi_uploads(bucket):
    """
    Counts the number of files present inside the given Wasabi bucket.

    Args:
        bucket (str): The name of the Wasabi bucket.

    Requires accurate Wasabi credentials in '/.aws/credentials' inside the root directory.
    """
    counting_session = boto3.Session(profile_name="default")
    counting_credentials = counting_session.get_credentials()
    counting_aws_access_key_id = counting_credentials.access_key
    counting_aws_secret_access_key = counting_credentials.secret_key

    counting_s3 = boto3.resource('s3',
                                 endpoint_url='https://s3.us-central-1.wasabisys.com',
                                 aws_access_key_id=counting_aws_access_key_id,
                                 aws_secret_access_key=counting_aws_secret_access_key
                                 )

    # Get bucket object
    counting_mpdb = counting_s3.Bucket(bucket)
    count = 0
    for _ in counting_mpdb.objects.all():
        count += 1
    print(f"{count} objects found in the {counting_mpdb.name} bucket")


def delete_object_from_bucket(file_name, bucket="mpdb", folder=""):
    """
    Deletes a given file from the Wasabi bucket.

    Args:
        file_name (str): The name of the file (including extension) you wish to delete.
        bucket (str, optional): The name of the Wasabi bucket where the file is located. Defaults to 'mpdb'.
        folder (str, optional): The name of the folder (if present) where the desired file is located.
                               Defaults to an empty string.

    Requires accurate Wasabi credentials in '/.aws/credentials' inside the root directory.
    """
    delete_session = boto3.Session(profile_name="default")
    delete_credentials = delete_session.get_credentials()
    delete_aws_access_key_id = delete_credentials.access_key
    delete_aws_secret_access_key = delete_credentials.secret_key

    delete_s3 = boto3.resource('s3',
                               endpoint_url='https://s3.US-central-1.wasabisys.com',
                               aws_access_key_id=delete_aws_access_key_id,
                               aws_secret_access_key=delete_aws_secret_access_key
                               )

    delete_s3.Object(bucket, folder + file_name).delete()
    print(f"{file_name} deleted from {bucket}/{folder}")


def count_items_in_part_list():
    """
    Counts the number of items inside the part number upload log created by the Image Uploader.

    Assumes the log file is located at '/Users/evanmeeks/Documents/Wasabi_UploadedPNS.txt'.
    """
    with open('/Users/evanmeeks/Documents/Wasabi_UploadedPNS.txt', 'r') as f:
        x = len(f.readlines())
    f.close()
    print(f"{x} items in the part number log")


def count_files_in_directory(directory):
    """
    Counts the number of files in a given directory.

    Args:
        directory (str): The directory path to count files in.
    """
    count = 0

    # Loop through each file in the directory
    for _, _, files in os.walk(directory):
        count += len(files)

    print(f'{count} files found in the directory')


def rename_files_in_directory(directory):
    """
    Renames all files in a given directory by extracting the last part of the filename.

    Args:
        directory (str): The directory path containing files to be renamed.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            new_name = filename.split()[-1]
            new_path = os.path.join(directory, new_name)
            os.rename(file_path, new_path)
            print(f"File renamed: {filename} -> {new_name}")


def check_images_for_text(input_directory, output_directory):
    """
    Moves images with text content from an input directory to an output directory for review.

    Args:
        input_directory (str): The directory containing the images to check for text.
        output_directory (str): The directory to move images with text content for review.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Get a list of all files in the input directory
    file_list = os.listdir(input_directory)

    # Iterate over the files in the input directory
    for file_name in file_list:
        # Construct the full path of the input file
        input_path = os.path.join(input_directory, file_name)

        # Check if the file is an image
        if is_image_file(input_path):
            # Perform OCR on the image
            text = perform_ocr(input_path)

            # If text is found, move the file to the output directory for review
            if text:
                output_path = os.path.join(output_directory, file_name)
                shutil.move(input_path, output_path)
                print(f"File moved for review: {file_name}")


def perform_ocr(image_path):
    """
    Performs OCR on an image to extract text content.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: Extracted text content from the image.
    """
    # Configure the OCR engine with additional options
    custom_config = r'--oem 3 --psm 6'  # Example: Use LSTM OCR engine and assume a single uniform block of text

    # Use pytesseract to perform OCR on the image with the custom configuration
    text = pytesseract.image_to_string(image_path, config=custom_config)
    return text.strip()


def check_file_exists(file_key):
    """
    Checks if a file with the given key exists in the 'mpdb' bucket.

    Args:
        file_key (str): The key of the file in the 'mpdb' bucket.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    bucket = s3.Bucket('mpdb')
    return any(obj.key == file_key for obj in bucket.objects.all())


count_wasabi_uploads(mpdb)