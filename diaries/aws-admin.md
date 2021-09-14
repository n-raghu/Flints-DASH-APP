# Amazon Control Tower
Automate the setup of your multi-account AWS environment with just a few clicks. The setup employs blueprints, which capture AWS best practices for configuring AWS security and management services to govern your environment and see Dashboards

In AWS Control Tower, Organizations helps centrally manage billing; control access, compliance, and security; and share resources across your member AWS accounts. Accounts are grouped into logical groups, called organizational units (OUs).

AWS Control Tower uses the following OUs:

**Root** – The parent container for all accounts and all other OUs in your landing zone.

**Security** – This OU contains the log archive account, the audit account, and the resources they own.

**Sandbox** – This OU is created when you set up your landing zone. It and other child OUs in your landing zone contain your member accounts. These are the accounts that your end users access to perform work on AWS resources

*For example, J2 Global is parent company which has 6 sister companies under it. Here, J2 has the Control Tower and all ENV(QA, PROD) accounts of a company is logically grouped as Organizations.*

# Amazon Organizations
AWS Organizations is an account management service that lets you consolidate multiple AWS accounts into an organization that you create and centrally manage. With Organizations, you can create member accounts and invite existing accounts to join your organization. You can organize those accounts into groups and attach policy-based controls.

# Regions and AZ

## Regions
 - Cross region data trasfer are happened through internet and charged for data transfer

## AZ
 - Amazon has Data centers in each region and few Data centers are termed as AZ
 - User is given an option to choose between AZ, however, the underlying the DC may vary.
 - Billing and data transfer is applicable as per the AZ chosen by user

## Best Practices:
 - Isolate accounts with department i.e. QA, DEV, PROD and services with VPC
 - Communication between services could be better if they are in same account because the underlying AZ is unchanged and could be much easier
 - If isolated with service, then each department should have access in each account which means you have almost all users in every account i.e. Production users are different from QA users
 - No restrictions to isolate based on service and use VPC to differentiate environments which boils down to the Organizational structure and architecture

# VPC, IG, RT & SG

**Amazon VPC** lets you provision a logically isolated section of the Amazon Web Services (AWS) cloud where you can launch AWS resources in a virtual network that you define. You have complete control over your virtual networking environment, including selection of your own IP address ranges, creation of subnets, and configuration of route tables and network gateways. You can also create a hardware Virtual Private Network (VPN) connection between your corporate datacenter and your VPC and leverage the AWS cloud as an extension of your corporate datacenter.

Amazon VPC comprises a variety of objects that will be familiar to customers with existing networks:

**A Virtual Private Cloud**: A logically isolated virtual network in the AWS cloud. You define a VPC’s IP address space from ranges you select.
Subnet: A segment of a VPC’s IP address range where you can place groups of isolated resources.

**Internet Gateway**: The Amazon VPC side of a connection to the public Internet.

**NAT Gateway**: A highly available, managed Network Address Translation (NAT) service for your resources in a private subnet to access the Internet.

**Virtual private gateway**: The Amazon VPC side of a VPN connection.

**Peering Connection**: A peering connection enables you to route traffic via private IP addresses between two peered VPCs.

**VPC Endpoints**: Enables private connectivity to services hosted in AWS, from within your VPC without using an Internet Gateway, VPN, Network Address Translation (NAT) devices, or firewall proxies.
Gateway type endpoints are available only for AWS services including S3 and DynamoDB. These endpoints will add an entry to your route table you selected and route the traffic to the supported services through Amazon’s private network.
 
Interface type endpoints provide private connectivity to services powered by PrivateLink, being AWS services, your own services or SaaS solutions, and supports connectivity over Direct Connect. More AWS and SaaS solutions will be supported by these endpoints in the future. Please refer to VPC Pricing for the price of interface type endpoints.

**Egress-only Internet Gateway**: A stateful gateway to provide egress only access for IPv6 traffic from the VPC to the Internet

A **security group** acts as a virtual firewall for your EC2 instances to control incoming and outgoing traffic. Inbound rules control the incoming traffic to your instance, and outbound rules control the outgoing traffic from your instance. When you launch an instance, you can specify one or more security groupsv

## Bites
1. Public subnet components like (Lambda) can connect to components like DynamoDB/RDS which are created in private subnet of same VPC without NAT Gateway, and a NAT Gateway/NAT Instance is necessary if they are in different VPC.

2. If you're pushing enough traffic, the cost of NAT instances will be less than the cost of NAT Gateway
NAT Gateway is managed by AWS and NAT Instance is managed by user.

# IAM
AWS Identity and Access Management (IAM) enables you to manage access to AWS services and resources securely. Using IAM, you can create and manage AWS users and groups, and use permissions to allow and deny their access to AWS resources.
IAM is a feature of your AWS account offered at no additional charge. You will be charged only for use of other AWS services by your users.

You can use temporary security credentials to make programmatic requests for AWS resources using the AWS CLI or AWS API (using the AWS SDKs). The temporary credentials provide the same permissions that you have with use long-term security credentials such as IAM user credentials. However, there are a few differences:

When you make a call using temporary security credentials, the call must include a session token, which is returned along with those temporary credentials. AWS uses the session token to validate the temporary security credentials.

The temporary credentials expire after a specified interval. After the credentials expire, any calls that you make with those credentials will fail, so you must get a new set of credentials.
