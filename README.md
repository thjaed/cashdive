# CashDive
CashDive is a self-hosted personal finance app that can connect to your bank provider, and it runs locally in a Docker container!

> [!WARNING]
> CashDive is currently in early development and has only been tested with TrueLayer's sandbox and demo data.
> 
> **Do not use CashDive with real bank accounts or real financial data yet.**

> Live demo available here: [cashdive-demo.thlab.dev](https://cashdive-demo.thlab.dev)

## How to use
The main setup step is configuring TrueLayer, which CashDive uses to access your bank data:

1. You need to create a TrueLayer account and log in to [TrueLayer console](https://console.truelayer.com)
2. Then create an application. You can give it any name and Client ID.
3. Record the Client ID, you will need this!
4. Now, go to the settings tab and create a client secret. Keep this safe and record it, you will need it!
5. TrueLayer needs to know where to send users after they have authorised their bank account. This is called the redirect URI and must exactly match the URL you use to access CashDive, followed by /api/auth/callback. Here are some examples:
    - `http://192.168.1.50:3000/api/auth/callback`
    - `http://localhost:3000/api/auth/callback`
    - `https://cashdive.yourdomain.com/api/auth/callback`

**Now you have the Client ID and Client Secret, you can deploy the docker container!**

Make a `docker-compose.yml` file:

```yaml
services:
  cashdive:
    image: thjaed/cashdive:latest
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      - postgres

  postgres:
    image: postgres:17

    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}

    volumes:
      - postgres:/var/lib/postgresql/data

volumes:
  postgres:
```

And a `.env` file with it, modifiying the variables for your setup:
```
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
SESSION_SECRET=generate-a-random-secret

DB_NAME=cashdive
DB_USER=cashdive
DB_PASSWORD=your-database-password

PUBLIC_URL=http://localhost:3000

NEXT_PUBLIC_LOCALE=en-GB
```
`PUBLIC_URL` must match the URL you use to access CashDive. If you change the URL later, you will need to update it here and the redirect URI in your TrueLayer application.

You need to generate a random string for the session secret. You can do this by running:
```bash
openssl rand -base64 32
```

And now you can run it!
```bash
docker compose up -d
```