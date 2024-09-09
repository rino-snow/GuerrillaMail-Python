 # GuerrillaMail
![46f9fd8911b3a915c1fec119e9062d00](https://github.com/user-attachments/assets/c05ec91b-25a9-4ef3-b054-102bb80325b3)

This is an unofficial API wrapper written in Python for www.guerrillamail.com

# Example
```Python
import asyncio
import secrets
import string
import re
from GuerrillaMail import Client

async def main():
    async with Client() as client:
        alias = "".join(secrets.choice(string.ascii_letters+string.digits) for _ in range(10))
        email = await client.create_email(alias=alias)
        ...
        messages = await client.get_messages(email)
        for message in messages:
            if message.mail_from == "XXX@mail.com":
                token = re.compile(r" (\w+) ",flags=re.A).findall(message.mail_excerpt)[0]
                print(token)
                break
        ...
        await client.delete_email(email)
        ...

if __name__ == "__main__":
    asyncio.run(main())
```
