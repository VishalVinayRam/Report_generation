import boto3
import csv

def get_iam_users_and_permissions():
    # Create an IAM client
    iam_client = boto3.client('iam')

    # Create a CSV file to store the results
    csv_file = "iam_users_permissions.csv"
    csv_writer = csv.writer(open(csv_file, 'w', newline=''))
    csv_writer.writerow(["IAM User", "Attached Policy", "Inline Policy"])

    try:
        # List IAM users
        response = iam_client.list_users()

        for user in response['Users']:
            user_name = user['UserName']
            attached_policies = []
            inline_policies = []

            # List attached IAM policies
            attached_policies_response = iam_client.list_attached_user_policies(UserName=user_name)
            for attached_policy in attached_policies_response['AttachedPolicies']:
                attached_policies.append(attached_policy['PolicyName'])

            # List IAM user inline policies
            inline_policies_response = iam_client.list_user_policies(UserName=user_name)
            for inline_policy_name in inline_policies_response['PolicyNames']:
                inline_policies.append(inline_policy_name)

            # Write the information to the CSV file
            csv_writer.writerow([user_name, ', '.join(attached_policies), ', '.join(inline_policies)])

    except Exception as e:
        print(f"Error: {e}")


get_iam_users_and_permissions()
