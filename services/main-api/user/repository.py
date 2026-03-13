from psycopg import Connection
from auth.schemas import UserSignUpIn, UserSignUpOut
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

async def retrive_unique_email_and_username(conn: Connection, user: UserSignUpIn) -> str:
    async with conn.cursor() as acur:
        await acur.execute(
            "SELECT user_name, email FROM users WHERE user_name = %s OR email = %s",
            (user.user_name, user.email)
        )
        result = await acur.fetchone()
        return result

async def add_user(conn: Connection, user: UserSignUpIn) -> UserSignUpOut:
    async with conn.cursor() as acur:
        await acur.execute(
            "INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)",
            (user.user_name, user.email, password_hash.hash(user.password.get_secret_value()))
        )