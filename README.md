## Organization Managment: Auto-monitoring Member Account

**Introduction**

When using AWS Organization, monitoring member account status from management account especially the link between with management account is hard by using exsiting cloud monitoring components like cloudtrail and cloudwatch alert. In order to implement member account monitoring automation, we created following pattern to implement the auto monitoring and send notification when such event occurs. In this example,we are monitoring the "Leave Organization" Event. For other event cannot be auto-tracked by cloudtrail and cloudwatch, you can use this pattern to implement the monitoring and alerts. 

**Pre-Requests:**

1. Create lambda funtion
2. Create a json file ("record.json") in S3
3. Set up SNS for notification
4. Set up EventBridge to trigger lambda hourly
5. Set up Role for lambda with following persiminsions
    - S3: Write and Read access to the Json file in step 2
    - Organizations:add AWSOrganizationsReadOnlyAccess permission
    - SNS: add AmazonSNSFullAccess permission

**Implementation**

Upload the code in lambda_funtion.py to leaveOrgAlert function code. and run a test once with 2 function-parameters.
- logs_bucket (bucket where you put the record.json)
- SNS_ARN (the arn for your SNS in pre-request)
