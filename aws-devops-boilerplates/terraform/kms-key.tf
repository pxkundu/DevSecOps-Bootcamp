resource "aws_kms_key" "custom_key" {
  description             = "KMS key for encryption"
  enable_key_rotation     = true
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "key_alias" {
  name          = "alias/{{KMS_ALIAS}}"  # Replace with your KMS alias (e.g., my-key)
  target_key_id = aws_kms_key.custom_key.key_id
}
