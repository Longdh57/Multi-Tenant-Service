from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

vnlife_engine = create_engine(settings.VNLIFE_DATABASE_URL, pool_pre_ping=True)
pv_vnshop_ka_engine = create_engine(settings.PV_VNSHOP_KA_DATABASE_URL, pool_pre_ping=True)


def get_db(tenant: int = 0) -> Generator:
    try:
        if tenant == 1:
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pv_vnshop_ka_engine)
        else:
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=vnlife_engine)
        db = SessionLocal()
        yield db
    finally:
        db.close()
