from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# import needs to be here or crash 
from .routers import users, security, algos, quotes, backtests, comps 
app.include_router(users.router)
app.include_router(security.router)
app.include_router(algos.router)
app.include_router(quotes.router)
app.include_router(backtests.router)
app.include_router(comps.router)
