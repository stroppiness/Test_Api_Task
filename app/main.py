from api.v1.wallet import router as wallet_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(wallet_router, prefix='/api/v1/wallets', tags=['Wallet'])
