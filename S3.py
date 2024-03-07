import boto3
import openpyxl
from openpyxl import Workbook

class S3BucketChecker:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "BucketsWithPublicAccess"
        self.sheet.append(["Bucket Name", "Public Access Blocks Enabled"])

    def check_and_save_public_access_blocks(self, excel_file="buckets_with_public_access.xlsx"):
        # List all S3 buckets
        response = self.s3.list_buckets()

        # Check public access block settings for each bucket
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            public_access_block = self.get_public_access_block(bucket_name)

            if not public_access_block:
                print(f"The bucket {bucket_name} does not have public access blocks enabled.")
            else:
                print(f"The bucket {bucket_name} has public access blocks enabled.")
                self.sheet.append([bucket_name, "Yes"])

        # Save the Excel workbook
        self.workbook.save(excel_file)

    def get_public_access_block(self, bucket_name):
        try:
            response = self.s3.get_public_access_block(Bucket=bucket_name)
            return response['PublicAccessBlockConfiguration']
        except self.s3.exceptions.NoSuchPublicAccessBlockConfiguration:
            return None


