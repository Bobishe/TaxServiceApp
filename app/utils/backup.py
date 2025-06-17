import os
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import Base, engine

async def export_table_csv(db: AsyncSession, model, path: str) -> None:
    result = await db.execute(select(model))
    rows = result.scalars().all()
    df = pd.DataFrame([r.__dict__ for r in rows])
    df.pop('_sa_instance_state', None)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

async def import_table_csv(db: AsyncSession, model, path: str) -> None:
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        obj = model(**row.to_dict())
        db.merge(obj)
    await db.commit()


def export_sql_dump(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    dump_cmd = (
        f"mysqldump -h {db_host} -P {db_port} -u {db_user} -p{db_pass} {db_name} > {path}"
    )
    os.system(dump_cmd)


def import_sql_dump(path: str) -> None:
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    cmd = f"mysql -h {db_host} -P {db_port} -u {db_user} -p{db_pass} {db_name} < {path}"
    os.system(cmd)

