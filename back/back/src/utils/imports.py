# Common imports

# Config
from back.src.database.config import DATABASE_URL

# Sqlalchemy Imports
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Fastapi imports
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Request, Body, Cookie

# Typing
from typing import Dict, List, Literal, Optional, Any, overload, Type
