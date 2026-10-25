from fastapi import FastAPI

from api.v1.wallet import router as wallet_router

app = FastAPI()

app.include_router(wallet_router, prefix='/api/v1/wallets', tags=['Wallet'])
