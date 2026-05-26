import json
import boto3
from botocore.exceptions import ClientError

# Initialize the programmatic AWS resource client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Automated CSPM Event Handler.
    Triggered by AWS EventBridge when an S3 bucket configuration drift occurs.
    Instantly strips public access and enforces strict private boundaries.
    """
    print(f"Received infrastructure event: {json.dumps(event)}")
    
    # Extract the target bucket name safely from the incoming event data
    try:
        bucket_name = event['detail']['requestParameters']['bucketName']
    except KeyError:
        print("Error: Event structure did not contain target bucket configuration parameters.")
        return {'statusCode': 400, 'body': 'Invalid event routing structure'}

    print(f"CRITICAL DRIFT DETECTED: Remediating public access rules on bucket: {bucket_name}")

    try:
        # 1. Idempotently apply absolute Public Access Block configurations
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print(f"SUCCESS: Applied structural Public Access Block to {bucket_name}")

        # 2. Revert bucket access control list back to secure Private containment
        s3_client.put_bucket_acl(
            Bucket=bucket_name,
            ACL='private'
        )
        print(f"SUCCESS: Overwrote bucket ACL parameters to private on {bucket_name}")
        
        return {
            'statusCode': 200,
            'body': f'Successfully isolated and remediated configuration drift on bucket: {bucket_name}'
        }

    except ClientError as e:
        print(f"EXECUTION FAILURE: Automation script failed to alter bucket permissions: {e}")
        return {
            'statusCode': 500,
            'body': f'Remediation pipeline error: {str(e)}'
        }
