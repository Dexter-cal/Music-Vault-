# SSL Certificate for Local Development

The MusicVault API server runs over HTTPS to ensure secure communication with the mobile client. For local development, a self-signed SSL certificate is used.

## Generating the Certificate and Key

The private key (`key.pem`) is not committed to the repository for security reasons. To run the server, you must generate your own certificate and key by running the following command from the root of the project:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out certs/cert.pem -keyout certs/key.pem -days 365 -subj "/C=US/ST=CA/L=SF/O=MusicVault/CN=localhost"
```

This will create two files in this directory:
- `cert.pem`: The public certificate, which is included in the repository.
- `key.pem`: The private key, which is ignored by Git.

You only need to do this once. After generating the files, you can start the API server with the `serve` command.
