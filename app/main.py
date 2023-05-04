from fastapi import FastAPI
from app.api.users import routes as users_routes
from app.api.users import models as users_models
from app.api.training_types import routes as training_type_routes
from app.api.training_types import models as training_types_models
from app.api.admins import routes as admins_routes
from app.api.admins import models as admins_models
from .config.database import engine


users_models.Base.metadata.create_all(bind=engine)
admins_models.Base.metadata.create_all(bind=engine)
training_types_models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(users_routes.router)
app.include_router(training_type_routes.router)
app.include_router(admins_routes.router)
