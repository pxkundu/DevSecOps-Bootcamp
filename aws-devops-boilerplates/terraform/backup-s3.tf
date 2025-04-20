resource "aws_s3_bucket" "backup" {
  bucket = "{{S3_BACKUP_BUCKET_NAME}}"  # Replace with your backup S3 bucket name
  acl    = "private"
  versioning {
    enabled = true
  }
}
resource "aws_s3_bucket_replication_configuration" "replication" {
  bucket = aws_s3_bucket.bucket.id
  role   = aws_iam_role.replication.arn
  rule {
    id     = "backup-rule"
    status = "Enabled"
    destination {
      bucket = aws_s3_bucket.backup.arn
      storage_class = "STANDARD"
    }
  }
}
resource "aws_iam_role" "replication" {
  name = "s3-replication-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
      }
    ]
  })
}
resource "aws_iam_role_policy" "replication" {
  name   = "s3-replication-policy"
  role   = aws_iam_role.replication.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.bucket.arn,
          "${aws_s3_bucket.bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateTags"
        ]
        Resource = "${aws_s3_bucket.backup.arn}/*"
      }
    ]
  })
}
