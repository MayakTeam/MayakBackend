#!/bin/env python3
# -*- coding: utf-8 -*-
# Created by MayakDefect team (drago) on 2026-10-05

from fastapi import FastAPI

from src.api import main_router

app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", reload=True)