from fastapi import FastAPI
import asyncpg

app = FastAPI()

# Create a connection pool to the database
pool = None


@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(
            dsn="postgresql://febridev:Febr11yant!@174.138.23.44:10432/berapanih"
    )


@app.on_event("shutdown")
async def shutdown():
    global pool
    await pool.close()


@app.get("/")
async def get_public_page():
    return {"message": "Welcome to the public page!"}


@app.get("/bbm/{table_name}")
async def get_data_from_table(table_name: str):
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT * FROM {table_name}")
        return rows

