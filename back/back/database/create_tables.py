from .models import Base
from .crud_database import engine

def start():
  Base.metadata.create_all(bind=engine)
