from decouple import config
from hubspot import HubSpot


hubspotClient = HubSpot()
hubspotClient.access_token = config('HUBSPOT_ACCESS_TOKEN')
