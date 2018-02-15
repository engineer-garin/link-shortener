

# So, I know I'm using multiple case conventions in here.
# Seems random, really isn't.
# I wouldn't use a dash in an attribute name, only an index name.
# lower_snake_case is more readable than CamelCase, so I prefer that for attribute names
# because a table is analogous to a class in OO, I use CamelCase for table name.
# use <namespace>-<TableName> convention here to allow for namespace scoping of tables (in case I want to have multiple link shortener environments running simultaneously)
resource "aws_dynamodb_table" "url_mappings" {
  name           = "${env_name}-URLShortenerMappings"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "short_id"

  attribute {
    name = "short_id"
    type = "N"
  }

  attribute {
    name = "url"
    type = "S"
  }

  global_secondary_index {
    name               = "url-index"
    hash_key           = "url"
    write_capacity     = 5
    read_capacity      = 5
    projection_type    = "ALL"
  }

  tags {
    Name        = "URLShortenerMappings"
    Environment = "${env_name}"
  }
}
