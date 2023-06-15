from fastapi import FastAPI,Request
import time
from src.database.db import conn
from src.models.recordModel import records
from src.routes.contactRoute import contactRouter
from src.schemas.recordSchema import Record
app = FastAPI()
import json
import uuid

app.include_router(contactRouter)

# @app.middleware("http")
# async def database_logging_middleware(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)

#     try:

#         record = Record(
#             id=str(uuid.uuid4()),
#             timestamp=str(start_time),
#             method=request.method,
#             path=request.url.path,
#             query_params=json.dumps(dict(request.query_params)),
#             request_body=(await request.body()).decode("utf-8"),
#             response=json.dumps({
#                 "status_code": response.status_code,
#                 "headers": dict(response.headers),
#                 "body": (await request.body()).decode("utf-8"),
#             })
#         )
#         conn.execute(records.insert().values(record.dict()))
#     except Exception as e:
#         print(e)

#     return response
