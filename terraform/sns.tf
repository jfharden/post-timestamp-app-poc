/** These are topics I would already expect in an environment set up for monitoring and alerting
* so I've just left the configuration of these extremely simple for now since they are not part
* of the proof of concept and normally I'd expect to be looking these up instead of creating
* new ones
*/

resource "aws_sns_topic" "alerts_low_priority" {
  name              = "${var.app_name}-alerts-low-priority"
  kms_master_key_id = aws_kms_key.app.id
  tags              = local.tags
}

resource "aws_sns_topic" "alerts_high_priority" {
  name              = "${var.app_name}-alerts-high-priority"
  kms_master_key_id = aws_kms_key.app.id
  tags              = local.tags
}
