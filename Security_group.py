import boto3
import openpyxl
from openpyxl import Workbook

class SecurityGroupChecker:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "SecurityGroupsAllowing0.0.0.0"
        self.sheet.append(["Security Group ID", "Security Group Name", "Inbound Rule"])

    def check_and_save_security_groups(self):
        # Describe all security groups
        response = self.ec2.describe_security_groups()

        # Check each security group
        for security_group in response['SecurityGroups']:
            group_id = security_group['GroupId']
            group_name = security_group['GroupName']
            
            # Check inbound rules for the security group
            for ingress_rule in security_group.get('IpPermissions', []):
                for ip_range in ingress_rule.get('IpRanges', []):
                    if ip_range['CidrIp'] == '0.0.0.0/0':
                        rule_description = f"{ingress_rule['IpProtocol']} from {ip_range['CidrIp']}"

                        # Add information to the Excel sheet
                        self.sheet.append([group_id, group_name, rule_description])

                        print(f"Security Group {group_name} ({group_id}) allows {rule_description}.")

        # Save the Excel workbook
        self.workbook.save("security_groups_allowing_0.0.0.0.xlsx")

