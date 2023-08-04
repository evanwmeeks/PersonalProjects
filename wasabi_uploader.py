import boto3
import os


class WasabiUploader:

    def __init__(self, directory):
        self.directory = directory
        self.session = boto3.Session(profile_name="default")
        self.credentials = self.session.get_credentials()
        self.aws_access_key_id = self.credentials.access_key
        self.aws_secret_access_key = self.credentials.secret_key
        self.s3 = boto3.resource('s3',
                                 endpoint_url='https://s3.US-central-1.wasabisys.com',
                                 aws_access_key_id=self.aws_access_key_id,
                                 aws_secret_access_key=self.aws_secret_access_key
                                 )

        self.mpdb = self.s3.Bucket('mpdb')

    def create_list_of_uploaded_parts(self, directory):
        print("Working...")
        UploadedPNsFileLocation = "/".join(
            directory.split("/", )[:-1])

        with open(f'{UploadedPNsFileLocation}/Wasabi_UploadedPNS.txt', 'a+') as f:
            f.seek(0)
            existing_contents = f.read()

            for obj in self.mpdb.objects.all():
                item = obj.key.split("/", 1)[1]
                if item not in existing_contents:
                    f.write(f"{item}\n")
        f.close()

        print(f"Wasabi Data processed, PN file created. "
              f"Available at: {UploadedPNsFileLocation}/Wasabi_UploadedPNS.txt'")

    def upload_photos(self):
        recordNumber = 0
        recordsAdded = 0

        for filename in os.listdir(self.directory):

            recordNumber += 1

            with open(f'{self.directory}/Wasabi_UploadedPNS.txt', 'a+') as f:

                f.seek(0)
                existing_contents = f.read()
                file = os.path.join(self.directory, filename)
                PN = filename.split(".")[0]

                if os.path.isfile(file):

                    if PN not in existing_contents:

                        try:

                            self.mpdb.upload_file(file, f"productimages/{filename}")
                            f.write(f"{filename}\n")
                            recordsAdded += 1
                            if recordNumber % 20 == 0:  # only printing every 20th record for confirmation of upload

                                print(f"{PN} successfully uploaded to Wasabi ({recordsAdded} images uploaded)")

                        except Exception as e:
                            print(f"failed to upload {PN} to Wasabi. Error: {e}")

            f.close()  
        print(f"Complete! Records Added: {recordsAdded}")

    def count_uploads(self):
        counting_mpdb = self.s3.Bucket('mpdb')
        count = 0
        print("Counting...")
        for _ in counting_mpdb.objects.all():
            count += 1
        print(f"{count} objects found in the library's bucket")

    def count_items_in_part_list(self):
        """
                Counts the number of items inside the part number upload log created by the Image Uploader.

                Assumes the log file is located at 'Wasabi_UploadedPNS.txt' in the specified directory.
                """

        directory_parts = self.directory.split("/")[:-1]  # Remove the last part (file name) from the path
        directory = "/".join(directory_parts)

        with open(f'{directory}/Wasabi_UploadedPNS.txt', 'r') as f:
            x = len(f.readlines())
        print(f"{x} items in the part number log")
