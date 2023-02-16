# HOWTO

This [docker-compose](https://docs.docker.com/compose/) file fires up an instance of Silicon Notes along with [Caddy](https://caddyserver.com) as a reverse proxy. Caddy will automatically fetch a TLS certificate from [Let's Encrypt](https://letsencrypt.org), so this compose file is fully suitable to deploy on the public Internet.

Before you start, you will need three pieces of information:

* A fully-qualified domain name for the service. (E.g., `silicon.example.com`)
* A username for authentication.
* A hashed password. You can generate one with:

```sh
docker run --rm -ti caddy caddy hash-password
```

1. Set up your DNS to point to your chosen FQDN.

2. Copy the sample environment variable file to `.env`. (Do NOT commit `.env` to version control!)

```sh
cp .env-example .env
```

3. Edit `.env` and fill in the necessary values.

4. Run: `docker compose up -d`
