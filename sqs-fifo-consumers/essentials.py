import boto3
import yaml

with open('cfg.yml', 'r') as yfile:
    creds = yaml.safe_load(yfile)


sample_dict = {
        'opportunity_name': "SuperVipre's Opp",
        'opportunity_id': 'als-mock-2',
        'opportunity_isdeleted': False,
        'opportunity_accountid': 'als-mock-1',
        'opportunity_stagename': 'Closed Won',
        'opportunity_isclosed': False,
        'opportunity_iswon': False,
        'opportunity_lastmodifieddate':'2021-03-11T11:59:18.000+0000',
        'opportunity_createddate': '2021-03-11T11:54:16.000+0000',
        'opportunity_license_end_date__c': '2023-03-10',
        'opportunity_licensed_users__c': 100.0,
        'opportunity_license_start_date__c': '2021-03-11',
        'opportunity_datacenter__c': 'US',
        'opportunity_farm_instance_code__c': 'lmsdevqa',
        'opportunity_lms_org_id__c': None,
        'opportunity_lms_type__c': 'Hosted Dedicated Server',
        'opportunity_lms_org_name__c': None,
        'opportunity_org_name__c': None,
        'opportunity_org_create_date__c': None,
        'opportunity_license_period_months__c': 12.0,
        'opportunity_license_period_days__c': 364.0,
        'opportunity_is_active_contract__c': True,
        'opportunity_partner_admin__c': None,
        'opportunity_partner_farm__c': None,
        'opportunity_is_statzen_enabled__c': True,
        'opportunity_is_mobile_app_enabled__c': True,
        'opportunity_is_phishproof_enabled__c': False,
        'opportunity_is_icomposer_enabled__c': True,
        'opportunity_client_posted__c': False,
        'opportunity_statzen_type__c': 'Standard',
        'opportunity_learning_interval__c': None,
        'last_mod_owner': 'stack-mock-agent'
    }


def msg_model(rjson=sample_dict):
    return rjson


def sqs_client(creds=creds):
    return boto3.client(
        'sqs',
        region_name='us-east-1',
        aws_access_key_id=creds['access_key'],
        aws_secret_access_key=creds['secret_key'],
    )


def sqs_url(creds=creds):
    return creds['sqs_uri']


def customer_msg_grps(n):
    return [f'gid-customer-{x}' for x in range(n)]


def set_queue_props(**kwargs):
    client = sqs_client()
    sqs_uri = sqs_url()
    action = kwargs.pop('action', 'fetch')
    if not kwargs:
        kwargs = {
            "DelaySeconds": "1",
            "VisibilityTimeout": "369",
        }
    if action.lower() == 'set':
        client.set_queue_attributes(
            QueueUrl=sqs_uri,
            Attributes=kwargs
        )

    print(client.get_queue_attributes(
        QueueUrl=sqs_uri,
        AttributeNames=list(kwargs.keys())
    ))
