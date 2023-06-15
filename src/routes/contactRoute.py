from fastapi import APIRouter,BackgroundTasks
from src.utils.hubspotClient import hubspotClient
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
from src.schemas.contactSchema import Contact
from src.schemas.taskSchema import Task
from decouple import config
import requests

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
                "estado_clickup": "pending"
            }
        )
        response = hubspotClient.crm.contacts.basic_api.create(contact)
        return response.properties
    except ApiException as e:
        print("Exception when calling basic_api->create: %s\n" % e)
        return "Error" + str(e)

#Get contacts by id
@contactRouter.get("/contacts/{id}")
async def get_contact(id:str):
    try:
        contact_fetched = hubspotClient.crm.contacts.basic_api.get_by_id(contact_id=id,properties=['estado_clickup'])
        return contact_fetched.properties
    except ApiException as e:
        return ("Exception when requesting contact by id: %s\n" % e)
    

#Update contact by id
@contactRouter.put("/contacts/{id}")
async def update_contact_to_added(id:str):
    try:
        contact_to_update = SimplePublicObjectInput(
            properties={
                "estado_clickup": "added"
            }
        )
        contact_updated = hubspotClient.crm.contacts.basic_api.update(id,contact_to_update)
        return contact_updated.properties
    except ApiException as e:
        return ("Exception when requesting contact by id: %s\n" % e)
    

#Get all contacts
@contactRouter.get("/contacts")
async def get_all_contacts():
    try:
        all_contacts = hubspotClient.crm.contacts.get_all(properties=['firstname','lastname','email','phone','website','estado_clickup'])
        contact_list = []
        for contact in all_contacts:
            print(contact)
            contact_list.append(contact.properties)
        return contact_list   
    except ApiException as e:
        return ("Exception when requesting all contacts: %s\n" % e)


@contactRouter.get("/tasks")
async def get_all_tasks():
    list_id = config('CLICKUP_LIST_ID')
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    headers = {"Authorization": config('CLICKUP_TOKEN')}

    response = requests.get(url, headers=headers)

    data = response.json()
    return data

@contactRouter.post("/tasks")
async def create_task(task:Task):
    list_id = config('CLICKUP_LIST_ID')
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    payload = {
    "name": task.name,
    "description": task.description,
    "status": "to do",
    "priority": 3,
    "due_date": 1508369194377,
    "due_date_time": False,
    "time_estimate": 8640000,
    "start_date": 1567780450202,
    "start_date_time": False,
    "notify_all": True,
    "parent": None,
    "links_to": None,
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": config('CLICKUP_TOKEN')
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    return data


#Sync tasks using background tasks
@contactRouter.get("/sync-tasks")
async def sync_tasks(background_tasks: BackgroundTasks):
    all_contacts = hubspotClient.crm.contacts.get_all(properties=['firstname','lastname','email','phone','website','estado_clickup'])
    pending_contacts = []
    for contact in all_contacts:
        if contact.properties['estado_clickup'] == 'pending':
            pending_contacts.append(contact.properties)
    
    for contact in pending_contacts:
        task = Task(
            name = contact['firstname'] + ' ' + contact['lastname'],
            description = contact['email'] + ' ' + contact['phone'] + ' ' + contact['website']
        )
        background_tasks.add_task(create_task, task)
        background_tasks.add_task(update_contact_to_added, contact['hs_object_id'])
    
    return {"message": "Synchronization process started"}

        

        


    





    
    





