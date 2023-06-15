from fastapi import APIRouter
from src.utils.hubspotClient import hubspotClient
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
from src.database.db import conn
from src.models.contactModel import contacts
from src.schemas.contactSchema import Contact
from decouple import config
import requests
import json


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
    

#Get all contacts
@contactRouter.get("/contacts")
async def get_all_contacts():
    try:
        all_contacts = hubspotClient.crm.contacts.get_all()
        contact_list = []
        for contact in all_contacts:
            contact_list.append(contact.properties)
        return contact_list   
    except ApiException as e:
        return ("Exception when requesting all contacts: %s\n" % e)


import requests


@contactRouter.get("/tasks")
async def get_all_tasks():
    list_id = config('CLICKUP_LIST_ID')
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    headers = {"Authorization": config('CLICKUP_TOKEN')}

    response = requests.get(url, headers=headers)

    data = response.json()
    return data

@contactRouter.post("/tasks")
async def create_task():
    list_id = config('CLICKUP_LIST_ID')
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    payload = {
    "name": "New Task Name",
    "description": "New Task Description",
    "assignees": [
        183
    ],
    "tags": [
        "tag name 1"
    ],
    "status": "Open",
    "priority": 3,
    "due_date": 1508369194377,
    "due_date_time": False,
    "time_estimate": 8640000,
    "start_date": 1567780450202,
    "start_date_time": False,
    "notify_all": True,
    "parent": None,
    "links_to": None,
    "check_required_custom_fields": True,
    "custom_fields": [
        {
        "id": "0a52c486-5f05-403b-b4fd-c512ff05131c",
        "value": "This is a string of text added to a Custom Field."
        }
    ]
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": config('CLICKUP_TOKEN')
    }

    response = requests.post(url, json=payload, headers=headers, params=query)

    data = response.json()
    print(data)
    return data
    





    
    





