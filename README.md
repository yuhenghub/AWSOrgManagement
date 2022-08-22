## Sample of tracking Leave Org Events

**Introduction**
When using AWS Organization, "Leave Organization" Event cannot be tracked from managment account, in order to implement this, this sample  function and addionally add notification when such event occurs. Besides the "Leave Organization" Event, other event cannot be auto-tracked by cloudtrail and cloudwatch, you can try the this solution to implement the monitor and alerts. 
**Pre-Requests:**
1. Create Lambda Funtion, named "leaveOrgAlert"
2. Create a json file ("record.json") in S3
3. Set Up SNS for notification
4. Set up EventBridge to trigger lambda hourly
5. Set Up Role for lambda with
- S3: Write and Read access to the Json file in step 2
- Organizations:add AWSOrganizationsReadOnlyAccess permission
- SNS: add AmazonSNSFullAccess permission

**Implementation**
Upload the code in lambda_funtion.py to leaveOrgAlert function code. and run a test once with 2 function-parameters.
- logs_bucket (bucket where you put the record.json)
- SNS_ARN (the arn for your SNS in pre-request)