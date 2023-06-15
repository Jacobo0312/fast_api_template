from fastapi import APIRouter
from src.utils.hubspotClient import hubspotClient
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
from src.database.db import conn
from src.models.contactModel import contacts
from src.schemas.contactSchema import Contact


contactRouter = APIRouter()

# Create a contact in hubspot client
@contactRouter.post("/contacts")
async def create_contact(contact:Contact):
    try:
        contact = SimplePublicObjectInput(
            properties={
                "email": contact.email,
                "firstname": contact.firstname,
                "lastname": contact.lastname,
                "phone": contact.phone,
                "website": contact.website,
            }
        )
        response = hubspotClient.crm.contacts.basic_api.create(contact)
        return response.body
    except ApiException as e:
        print("Exception when calling basic_api->create: %s\n" % e)
        return "Error" + str(e)

#Get contacts by id
@contactRouter.get("/contacts/{id}")
async def get_contact(id:str):
    try:
        contact_fetched = hubspotClient.crm.contacts.basic_api.get_by_id(id)
        return contact_fetched.properties
    except ApiException as e:
        return ("Exception when requesting contact by id: %s\n" % e)


    
    





