#!/usr/local/bin/python3
#
# Create application and launch environment with dummy application running
#
import boto3
import time
import webbrowser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('region')
parser.add_argument('vpcid')
parser.add_argument('security_group')
parser.add_argument('subnets')
args = parser.parse_args()

region = args.region
vpc_id = args.vpcid
instance_security_group = args.security_group
webserver_subnets = ','.join(eval(args.subnets))

# account_id = boto3.resource('iam').CurrentUser().arn.split(':')[4]


instance_type = 't2.micro'
healthcheck_url ='/'
#
# Number of minutes to wait for beanstalk to go green
#
wait_for_green = 5
cool_down = str(60 * 6)
autoscale_max_instance = '4'
autoscale_min_instance = '1'
rolling_update_batch_percent = '30'
#
# Managed updates
#
update_level = 'patch'
managed_actions_enabled ='true'
preferred_starttime = "Sun:10:00"
#
#
#
ssh_key_name = 'shelde-test-us-west-2'
ssh_restrictions = 'tcp,22,22,124.149.49.200/32'
instance_profile = 'aws-elasticbeanstalk-ec2-role'
service_role = 'aws-elasticbeanstalk-service-role'
#
#
#
application_name = 'shelde01'
application_description = 'Test application for Shelde demo'
environment_name = "%s-blue" % (application_name)
notification_email = 'rcoaic@gmail.com'
#
# notification_topic = "arn:aws:sns:%s:%s:ElasticBeanstalkNotifications-Environment-%s" % (region, account_id, environment_name)
#
environment_description = 'shelde01 blue environment'
template_name = 'blue_v1'
solution_stack = '64bit Amazon Linux 2016.03 v2.2.0 running Tomcat 8 Java 8'
template_description = 'shelde01 blue environment'
option_settings = [
    {
        "OptionName": "IamInstanceProfile",
        "Namespace": "aws:autoscaling:launchconfiguration",
        "Value": "aws-elasticbeanstalk-ec2-role"
    },
    {
        "OptionName": "VPCId",
        "Namespace": "aws:ec2:vpc",
        "Value": vpc_id
    },
    {
        "OptionName": "Subnets",
        "Namespace": "aws:ec2:vpc",
        "Value": webserver_subnets
    },
    {
        "OptionName": "ELBSubnets",
        "Namespace": "aws:ec2:vpc",
        "Value": webserver_subnets
    },
    {
        "OptionName": "AssociatePublicIpAddress",
        "ResourceName": "AWSEBAutoScalingLaunchConfiguration",
        "Namespace": "aws:ec2:vpc",
        "Value": "true"
    },
    {
        "OptionName": "ELBScheme",
        "Namespace": "aws:ec2:vpc",
        "Value": "public"
    },
    {
        "OptionName": "Availability Zones",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:asg",
        "Value": "Any"
    },
    {
        "OptionName": "Cooldown",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:asg",
        "Value": cool_down
    },
    {
        "OptionName": "MaxSize",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:asg",
        "Value": autoscale_max_instance
    },
    {
        "OptionName": "MinSize",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:asg",
        "Value": autoscale_min_instance
    },
    {
        "OptionName": "BlockDeviceMappings",
        "ResourceName": "AWSEBAutoScalingLaunchConfiguration",
        "Namespace": "aws:autoscaling:launchconfiguration"
    },
    {
        "OptionName": "EC2KeyName",
        "ResourceName": "AWSEBAutoScalingLaunchConfiguration",
        "Namespace": "aws:autoscaling:launchconfiguration",
        "Value": ssh_key_name
    },
    {
        "OptionName": "IamInstanceProfile",
        "ResourceName": "AWSEBAutoScalingLaunchConfiguration",
        "Namespace": "aws:autoscaling:launchconfiguration",
        "Value": instance_profile
    },
    {
        "OptionName": "ServiceRole",
        "Namespace": "aws:elasticbeanstalk:environment",
        "Value": service_role
    },
    {
        "OptionName": "SSHSourceRestriction",
        "Namespace": "aws:autoscaling:launchconfiguration",
        "Value": ssh_restrictions
    },
    {
        "OptionName": "SecurityGroups",
        "ResourceName": "AWSEBAutoScalingLaunchConfiguration",
        "Namespace": "aws:autoscaling:launchconfiguration",
        "Value": instance_security_group
    },
    {
        "OptionName": "JDBC_CONNECTION_STRING",
        "Namespace": "aws:elasticbeanstalk:application:environment",
        "Value": ""
    },
    {
        "OptionName": "DeploymentPolicy",
        "Namespace": "aws:elasticbeanstalk:command",
        "Value": "Rolling"
    },
    {
        "OptionName": "LogPublicationControl",
        "Namespace": "aws:elasticbeanstalk:hostmanager",
        "Value": "true"
    },
    {
        "OptionName": "JVMOptions",
        "Namespace": "aws:cloudformation:template:parameter",
        "Value": "XX:MaxPermSize=64m,Xmx=256m,JVM Options=,Xms=256m"
    },
    # {
    #     "OptionName": "MaxBatchSize",
    #     "ResourceName": "AWSEBAutoScalingGroup",
    #     "Namespace": "aws:autoscaling:updatepolicy:rollingupdate",
    #     "Value": "1"
    # },
    {
        "OptionName": "BatchSize",
        "Namespace": "aws:elasticbeanstalk:command",
        "Value": rolling_update_batch_percent
    },
    {
        "OptionName": "BatchSizeType",
        "Namespace": "aws:elasticbeanstalk:command",
        "Value": "Percentage"
    },
    {
        "OptionName": "MinInstancesInService",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:updatepolicy:rollingupdate",
        "Value": "1"
    },
    {
        "OptionName": "JVM Options",
        "Namespace": "aws:elasticbeanstalk:container:tomcat:jvmoptions",
        "Value": ""
    },
    {
        "OptionName": "XX:MaxPermSize",
        "Namespace": "aws:elasticbeanstalk:container:tomcat:jvmoptions",
        "Value": "64m"
    },
    {
        "OptionName": "Xms",
        "Namespace": "aws:elasticbeanstalk:container:tomcat:jvmoptions",
        "Value": "256m"
    },
    {
        "OptionName": "Xmx",
        "Namespace": "aws:elasticbeanstalk:container:tomcat:jvmoptions",
        "Value": "256m"
    },
    {
        "OptionName": "PauseTime",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:updatepolicy:rollingupdate"
    },
    {
        "OptionName": "RollingUpdateEnabled",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:updatepolicy:rollingupdate",
        "Value": "true"
    },
    {
        "OptionName": "RollingUpdateType",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:updatepolicy:rollingupdate",
        "Value": "Health"
    },
    {
        "OptionName": "Timeout",
        "ResourceName": "AWSEBAutoScalingGroup",
        "Namespace": "aws:autoscaling:updatepolicy:rollingupdate",
        "Value": "PT30M"
    },
    {
        "OptionName": "HealthCheckSuccessThreshold",
        "Namespace": "aws:elasticbeanstalk:healthreporting:system",
        "Value": "Ok"
    },
    {
        "OptionName": "SystemType",
        "Namespace": "aws:elasticbeanstalk:healthreporting:system",
        "Value": "enhanced"
    },
    {
        "Namespace": "aws:autoscaling:launchconfiguration",
        "OptionName": "InstanceType",
        "Value": instance_type
    },
    {
        "OptionName": "CrossZone",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:loadbalancer",
        "Value": "true"
    },
    {
        "OptionName": "Application Healthcheck URL",
        "Namespace": "aws:elasticbeanstalk:application",
        "Value": healthcheck_url
    },
    {
        "OptionName": "HealthyThreshold",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:healthcheck",
        "Value": "3"
    },
    {
        "OptionName": "Interval",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:healthcheck",
        "Value": "10"
    },
    {
        "OptionName": "Notification Endpoint",
        "Namespace": "aws:elasticbeanstalk:sns:topics",
        "Value": notification_email
    },
    {
        "OptionName": "Notification Protocol",
        "Namespace": "aws:elasticbeanstalk:sns:topics",
        "Value": "email"
    },
    #
    # Let Elastic Beanstalk create topic for email notifications
    #
    # {
    #     "OptionName": "Notification Topic ARN",
    #     "Namespace": "aws:elasticbeanstalk:sns:topics",
    #     "Value": notification_topic
    # },
    # {
    #     "OptionName": "Notification Topic Name",
    #     "Namespace": "aws:elasticbeanstalk:sns:topics"
    # },
    {
        "OptionName": "Target",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:healthcheck",
        "Value": "HTTP:80" + healthcheck_url
    },
    {
        "OptionName": "Timeout",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:healthcheck",
        "Value": "5"
    },
    {
        "OptionName": "UnhealthyThreshold",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:healthcheck",
        "Value": "5"
    },
    {
        "OptionName": "ConnectionDrainingEnabled",
        "ResourceName": "AWSEBLoadBalancer",
        "Namespace": "aws:elb:policies",
        "Value": "true"
    },
    {
        "OptionName": "ManagedActionsEnabled",
        "Namespace": "aws:elasticbeanstalk:managedactions",
        "Value": managed_actions_enabled
    },
    {
        "OptionName": "PreferredStartTime",
        "Namespace": "aws:elasticbeanstalk:managedactions",
        "Value": preferred_starttime
    },
    {
        "OptionName": "InstanceRefreshEnabled",
        "Namespace": "aws:elasticbeanstalk:managedactions:platformupdate",
        "Value": "false"
    },
    {
        "OptionName": "UpdateLevel",
        "Namespace": "aws:elasticbeanstalk:managedactions:platformupdate",
        "Value": update_level
    }
]
client = boto3.client('elasticbeanstalk', region)

response = client.check_dns_availability(CNAMEPrefix=environment_name)
if not response['Available']:
    print("ERROR: Environment name: %s already in use." % environment_name)
    exit(1)

#
# Create application if not already created
#
response = client.describe_applications(ApplicationNames=[application_name])
if not response['Applications'] or response['Applications'][0]['ApplicationName'] != application_name:
    response = client.create_application(ApplicationName=application_name, Description=application_description)

#
# Create configuration template if not already created
#
response = client.describe_applications(ApplicationNames=[application_name])
if not template_name in response['Applications'][0]['ConfigurationTemplates']:
    response = client.create_configuration_template(
        ApplicationName=application_name,
        TemplateName=template_name,
        SolutionStackName=solution_stack,
        Description=template_description,
        OptionSettings=option_settings
    )

#
# Create environment with dummy application running
#
response = client.create_environment(
    ApplicationName=application_name,
    EnvironmentName=environment_name,
#    GroupName='string',
    Description=environment_description,
    CNAMEPrefix=environment_name,
    Tier={
        'Name': 'WebServer',
        'Type': 'Standard'
    },
    Tags=[
        {
            'Key': 'name',
            'Value': environment_name
        },
    ],
    # VersionLabel='string',
    TemplateName=template_name,
    SolutionStackName=solution_stack
    # OptionSettings=[
    #     {
    #         'ResourceName': 'string',
    #         'Namespace': 'string',
    #         'OptionName': 'string',
    #         'Value': 'string'
    #     },
    # ],
    # OptionsToRemove=[
    #     {
    #         'ResourceName': 'string',
    #         'Namespace': 'string',
    #         'OptionName': 'string'
    #     },
    # ]
)

url = response['CNAME']
environment_id = response['EnvironmentId']

#
# Open AWS Console to observe Environment progress
#
webbrowser.open_new("https://us-west-2.console.aws.amazon.com/elasticbeanstalk/home?region=us-west-2#/environment/dashboard?applicationName=%s&environmentId=%s" % (application_name, environment_id))

healthy_environment = False
#
#  Wait for environment to become healthy
#
for __ in range(0, wait_for_green):
    time.sleep(60)
    response = client.describe_environment_health(EnvironmentId=environment_id, AttributeNames=['Color'])
    if response['Color'] == 'Green':
        healthy_environment = True
        break

#
# Display application in browser
#
if healthy_environment:
    webbrowser.open_new("http://%s" % (url))
    exit(0)
else:
    print("ERROR: environment %s failed to transition to healthy state" % (environment_name))
    exit(1)