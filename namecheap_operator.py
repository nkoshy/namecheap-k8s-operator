import kopf
import os
import logging
from namecheap import Api as NamecheapApi

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Namecheap API client
try:
    namecheap_client = NamecheapApi(
        ApiUser=os.getenv('NAMECHEAP_API_USER'),
        ApiKey=os.getenv('NAMECHEAP_API_KEY'),
        UserName=os.getenv('NAMECHEAP_USERNAME'),
        ClientIP=os.getenv('NAMECHEAP_CLIENT_IP'),
        sandbox=False,
        debug=True
    )
    logger.info("Namecheap API client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Namecheap API client: {str(e)}")
    raise

@kopf.on.create('namecheap.com', 'v1', 'nameacheapdnsrecords')
@kopf.on.update('namecheap.com', 'v1', 'nameacheapdnsrecords')
def create_or_update_dns_record(spec, meta, status, **kwargs):
    domain = spec['domain']
    subdomain = spec['subdomain']
    record_type = spec['recordType']
    value = spec['value']
    ttl = spec.get('ttl', 1800)

    logger.info(f"Attempting to create/update DNS record: {subdomain}.{domain} ({record_type})")

    try:
        host_record = {
            "RecordType": record_type,
            "HostName": subdomain,
            "Address": value,
            "MXPref": 10 if record_type == "MX" else 0,
            "TTL": ttl
        }
        
        result = namecheap_client.domains_dns_addHost(domain, host_record)
        
        if not result:
            raise kopf.PermanentError(f"Failed to add/update Namecheap DNS record")
        
        logger.info(f"Successfully added/updated DNS record for {subdomain}.{domain}")
    except Exception as e:
        logger.error(f"Failed to add/update Namecheap DNS record: {str(e)}")
        raise kopf.PermanentError(f"Failed to add/update Namecheap DNS record: {str(e)}")

    return {'message': f"DNS record added/updated for {subdomain}.{domain} to {value}"}

@kopf.on.delete('namecheap.com', 'v1', 'nameacheapdnsrecords')
def delete_dns_record(spec, **kwargs):
    domain = spec['domain']
    subdomain = spec['subdomain']
    record_type = spec['recordType']

    logger.info(f"Attempting to delete DNS record: {subdomain}.{domain} ({record_type})")

    try:
        # Get existing hosts
        existing_hosts = namecheap_client.domains_dns_getHosts(domain)
        logger.debug(f"Existing hosts for {domain}: {existing_hosts}")

        # Remove the specified record
        updated_hosts = [
            host for host in existing_hosts
            if not (host['Name'] == subdomain and host['Type'] == record_type)
        ]

        if len(existing_hosts) == len(updated_hosts):
            logger.warning(f"Record {subdomain}.{domain} ({record_type}) not found, nothing to delete")
            return {'message': f"DNS record for {subdomain}.{domain} not found"}

        # Set updated hosts
        result = namecheap_client.domains_dns_setHosts(domain, updated_hosts)
        
        if not result:
            raise kopf.PermanentError(f"Failed to delete Namecheap DNS record")
        
        logger.info(f"Successfully deleted DNS record for {subdomain}.{domain}")
    except Exception as e:
        logger.error(f"Failed to delete Namecheap DNS record: {str(e)}")
        raise kopf.PermanentError(f"Failed to delete Namecheap DNS record: {str(e)}")

    return {'message': f"DNS record deleted for {subdomain}.{domain}"}
