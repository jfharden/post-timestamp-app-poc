resource "aws_s3_bucket" "dead_letters" {
  // I've used a prefix and not a flat name since these are globally unique and I don't want my test and yours to clash
  bucket_prefix = "${var.name}-dead-letters-"
  acl           = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = var.kms_key_id
        sse_algorithm     = "aws:kms"
      }
    }
  }

  force_destroy = true // Normally I wouldn't have this on, but during a POC it makes it much easier to recreate it

  versioning {
    enabled = false // In production, not a POC, I would expect this to be enabled
  }

  // In production, not a POC, I would expect logging to be enabled and delivering to a centralised log bucket

  tags = var.tags
}

resource "aws_s3_bucket_public_access_block" "dead_letters" {
  bucket = aws_s3_bucket.dead_letters.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
