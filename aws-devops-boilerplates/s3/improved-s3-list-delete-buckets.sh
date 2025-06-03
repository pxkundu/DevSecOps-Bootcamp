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

# Function to empty a bucket (handles versioning and delete markers)
empty_bucket() {
    local profile=$1
    local bucket=$2
    local max_attempts=3
    local attempt=1

    echo "Emptying bucket: $bucket"

    # Check if bucket is versioned
    versioning=$(aws s3api get-bucket-versioning --profile "$profile" --bucket "$bucket" --query 'Status' --output text 2>/dev/null)
    if [ "$versioning" == "Enabled" ] || [ "$versioning" == "Suspended" ]; then
        echo "Bucket $bucket has versioning enabled or suspended. Deleting all versions and delete markers..."

        # Delete all object versions
        while [ $attempt -le $max_attempts ]; do
            versions=$(aws s3api list-object-versions --profile "$profile" --bucket "$bucket" --query 'Versions[].{Key:Key,VersionId:VersionId}' --output json 2>/dev/null)
            if [ -n "$versions" ] && [ "$versions" != "[]" ]; then
                aws s3api delete-objects --profile "$profile" --bucket "$bucket" --delete "{\"Objects\":$versions}" 2>/dev/null
                if [ $? -eq 0 ]; then
                    echo "Deleted object versions (attempt $attempt)"
                    break
                else
                    echo "Failed to delete object versions (attempt $attempt). Retrying..."
                    sleep 2
                    ((attempt++))
                fi
            else
                echo "No object versions found."
                break
            fi
        done

        # Delete all delete markers
        attempt=1
        while [ $attempt -le $max_attempts ]; do
            delete_markers=$(aws s3api list-object-versions --profile "$profile" --bucket "$bucket" --query 'DeleteMarkers[].{Key:Key,VersionId:VersionId}' --output json 2>/dev/null)
            if [ -n "$delete_markers" ] && [ "$delete_markers" != "[]" ]; then
                aws s3api delete-objects --profile "$profile" --bucket "$bucket" --delete "{\"Objects\":$delete_markers}" 2>/dev/null
                if [ $? -eq 0 ]; then
                    echo "Deleted delete markers (attempt $attempt)"
                    break
                else
                    echo "Failed to delete delete markers (attempt $attempt). Retrying..."
                    sleep 2
                    ((attempt++))
                fi
            else
                echo "No delete markers found."
                break
            fi
        done
    else
        # Non-versioned bucket: delete all objects
        attempt=1
        while [ $attempt -le $max_attempts ]; do
            objects=$(aws s3api list-objects-v2 --profile "$profile" --bucket "$bucket" --query 'Contents[].{Key:Key}' --output json 2>/dev/null)
            if [ -n "$objects" ] && [ "$objects" != "[]" ]; then
                aws s3api delete-objects --profile "$profile" --bucket "$bucket" --delete "{\"Objects\":$objects}" 2>/dev/null
                if [ $? -eq 0 ]; then
                    echo "Deleted objects (attempt $attempt)"
                    break
                else
                    echo "Failed to delete objects (attempt $attempt). Retrying..."
                    sleep 2
                    ((attempt++))
                fi
            else
                echo "No objects found."
                break
            fi
        done
    fi
}

# Function to delete a bucket
delete_bucket() {
    local profile=$1
    local bucket=$2
    local max_attempts=3
    local attempt=1

    echo "Deleting bucket: $bucket"
    while [ $attempt -le $max_attempts ]; do
        if aws s3 rb "s3://$bucket" --profile "$profile" --force 2>/dev/null; then
            echo "Bucket $bucket deleted successfully."
            return 0
        else
            echo "Failed to delete bucket $bucket (attempt $attempt). Retrying..."
            sleep 2
            ((attempt++))
        fi
    done
    echo "Failed to delete bucket $bucket after $max_attempts attempts. Possible dependencies (e.g., lifecycle policies, replication rules, or permissions)."
    return 1
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
read -p "WARNING: This will EMPTY and DELETE ALL listed S3 buckets, including Amplify, Glue, and CDK-generated buckets. Type 'YES' to continue: " confirmation
if [ "$confirmation" != "YES" ]; then
    echo "Operation cancelled."
    exit 1
fi

# Loop through each bucket to empty and delete
failed_buckets=""
while IFS= read -r bucket; do
    echo "Processing bucket: $bucket"
    
    # Empty the bucket
    empty_bucket "$profile" "$bucket"
    
    # Delete the bucket
    if ! delete_bucket "$profile" "$bucket"; then
        failed_buckets="$failed_buckets $bucket"
    fi
done <<< "$buckets"

# Summary
if [ -z "$failed_buckets" ]; then
    echo "All buckets processed successfully."
else
    echo "Operation completed with failures. The following buckets could not be deleted:"
    echo "$failed_buckets"
    echo "Please check for dependencies like lifecycle policies, replication rules, or insufficient permissions."
fi
