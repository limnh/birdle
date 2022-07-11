resource "aws_s3_bucket" "birdle" {
  bucket = "s3-birdle-images"
}

resource "aws_s3_bucket_acl" "birdle" {
  bucket = aws_s3_bucket.birdle.id
  acl    = "public-read"
}