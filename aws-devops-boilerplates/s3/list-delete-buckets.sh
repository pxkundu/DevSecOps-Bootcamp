#!/bin/bash

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Function to list AWS profiles from ~/.aws/credentials
list_aws_profiles() {
    echo "Available AWS profiles:"
    grep -E '^\[.*\]$' ~/.aws/credentials | tr -d '[]' | nl
}

# Function to validate AWS profile
validate_profile() {
    local profile=$1
    aws configure list-profiles | grep -w "$profile" > /dev/null
    return $?
}

# Prompt user to select an AWS profile
list_aws_profiles
read -p "Enter the number of the AWS profile to use: " profile_number

# Get the profile name based on the number
profile=$(grep -E '^\[.*\]$' ~/.aws/credentials | tr -d '[]' | sed -n "${profile_number}p")

if [ -z "$profile" ]; then
    echo "Invalid profile selection."
    exit 1
fi

# Validate the selected profile
if ! validate_profile "$profile"; then
    echo "Profile '$profile' is not valid."
    exit 1
fi

echo "Using AWS profile: $profile"

# List all S3 buckets
buckets=$(aws s3 ls --profile "$profile" | awk '{print $3}')

if [ -z "$buckets" ]; then
    echo "No S3 buckets found in the account."
    exit 0
fi

echo "Found the following S3 buckets:"
echo "$buckets"
echo

# Prompt for confirmation before proceeding
read -p "WARNING: This will EMPTY and DELETE ALL listed S3 buckets. Type 'YES' to continue: " confirmation
if [ "$confirmation" != "YES" ]; then
    echo "Operation cancelled."
    exit 1
fi

# Loop through each bucket to empty and delete
while IFS= read -r bucket; do
    echo "Processing bucket: $bucket"
    
    # Empty the bucket (delete all objects and versions if versioned)
    echo "Emptying bucket: $bucket"
    aws s3api delete-objects --profile "$profile" --bucket "$bucket" \
        --delete "$(aws s3api list-object-versions --profile "$profile" --bucket "$bucket" \
        --query='{Objects: Versions[].{Key:Key,VersionId:VersionId}}')" 2>/dev/null

    # Delete all delete markers (if any)
    aws s3api delete-objects --profile "$profile" --bucket "$bucket" \
        --delete "$(aws s3api list-object-versions --profile "$profile" --bucket "$bucket" \
        --query='{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}')" 2>/dev/null

    # Delete the bucket
    echo "Deleting bucket: $bucket"
    if aws s3 rb "s3://$bucket" --profile "$profile" --force 2>/dev/null; then
        echo "Bucket $bucket deleted successfully."
    else
        echo "Failed to delete bucket $bucket. It may have dependencies or access issues."
    fi
done <<< "$buckets"

echo "Operation completed."
