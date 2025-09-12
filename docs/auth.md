# SDTP / Galyleo REST API Authentication

## Authentication Overview

The SDTP protocol is designed for **maximum ease of adoption and integration** into modern web environments. In order to enable seamless interoperability with existing identity providers, document sharing platforms, and security infrastructures, SDTP builds   on standard web and REST authentication mechanisms such as HTTP Bearer tokens.

The protocol is designed to allow any web or REST server to implement the SDTP routes using the server's existing  authentication patterns (including OAuth2, JWTs, API keys, and more) without custom logic, and it's designed to give SDTP implementers the broadest possible choice of authentication mechanisms. 
The goal is to  allow organizations to integrate SDTP into their workflows—whether deploying a standalone SDTP server, building a sidecar service (for example, alongside JupyterHub), or embedding SDTP capabilities in other web service, and to use the authentication and authorization methods appropriate to their environment.

The **reference implementation** demonstrates protocol mechanics only and intentionally omits authentication, so integrators can layer on their preferred security model.
**Production deployments** should always use SDTP in conjunction with standard, proven authentication solutions.

The SDTP  client therefore offers  **standard HTTP Bearer token authentication**.

## SDTP Client: Bearer Token Support

The SDTP client is designed to fit naturally into standard web authentication flows, without dictating any specific policy or implementation. The client supports (but does not require or validate) Bearer token authentication as follows:

1. **Bearer Token Support**: If a Bearer token is set in the client, it will be included as an `Authorization: Bearer <token>` header in every request.

2. **Override on Request**: Users can override the Bearer token for any individual request (e.g., by passing a new token as an argument).

3. **Token Removal**: Setting `token=None` for a request omits the Authorization header entirely for that call.

4. **Automatic Configuration**: The client supports two environment variables so authentication can be auto-configured:

   * One for setting the token directly (e.g., `SDTP_CREDENTIAL_VAR`)
   * One for setting a file path to read the token from (e.g., `SDTP_CREDENTIAL_PATH`)

5. **No Token Issuance or Validation**: The SDTP protocol and reference implementation do not issue, validate, or inspect Bearer tokens. All authentication logic (validation, permissions, identity mapping) is the responsibility of the server or the environment in which SDTP is deployed.

For details of SDTP Client support for authentication, see [Overview](sdtp_client.md).

For practical details and examples of Bearer token authentication, refer to [standard web and REST authentication documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) or your organization’s security guidelines.
