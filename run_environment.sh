#!/usr/bin/env bash
#
#
# Draw attention to some environment assumptions
#
cat <<EOF

The scripts make several assumptions about the AWS environment:

1.  Python3 is installed

2.  Assumes all scripts are in current directory.

3.  Assumes the region is us-west-2

4.  Assumes the .war file to be launched is in the same folder as the scripts and is named ROOT.war

5.  Assumes an email address for Simple Notification Service notifications: rcoaic at gmail dot com

6.  The AWS CLI must be installed. Refer to: http://docs.aws.amazon.com/cli/latest/userguide/installing.html

7.  The aws configure command must be run to store/configure an API key/secret that can be accessed via commands.

8.  No API keys or account credentials are stored in the scripts or repository.

9.  The development environment is currently Mac OS command line.

10. Various packages not provided via Mac OS have been installed with Homebrew. Refer to http://brew.sh

11. There is a reliance on AWS Elastic Beanstalk to create an initial bucket to maintain configuration data needed by
    the service in the region being used.

12. Assumes an EC2 key pair exists for the region, assumes shelde-test-us-west-2.

13. Assumes default roles have been created by Elastic Beanstalk named: aws-elasticbeanstalk-ec2-role and aws-elasticbeanstalk-service-role
    -- this is a one time requirement, roles are not region specific.

14. The EC2s launched by Elastic Beanstalk have public IPs assigned -- public internet connectivity is required for the EC2s to access
    Elastic Beanstalk API end points.

15. An alternative would be to modify the VPC creation script to create a NAT Service in a public subnet to allow instances with only
    private IPs to have AWS API access to the NAT service.

16. If you want to rerun ./create_beanstalk_with_eb_api.py from console, please ensure you terminate the environment followed by deleting the
    application in the AWS Console.

17. Prior to deployment the .war file it is unpacked to ./tmp, the .ebextensions folder in the root of the .war is removed and seeded with configured
    .ebextensions folder to allow configuring launched Ec2s with access to the Elastic File System File at /efs on the EC2


EOF

while true; do
    read -p "Do you wish to run the Elastic Beanstalk Environment?" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 1;;
        * ) echo "Please answer yes or no.";;
    esac
done
#
# Create VPC environment to run beanstalk
#
echo "Now creating VPC"
python3 ./create_eb_vpc_with_ec2_api.py
#
#
while true; do
    read -p "Do you wish to run the next step in the environment setup?" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 1;;
        * ) echo "Please answer yes or no.";;
    esac
done

read -p "Copy and from terminal and paste command to run: " command

(
    echo "Now creating Elastic Beanstalk and launch default Java application"
    eval $command
)

echo "Here Here"