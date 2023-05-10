# The One API Python SDK

## Auth

API key handling is inspired by Stripe's Python SDK and offers a global variable to store the
user's key.

* The `api_key` global variable is intended to be set once and then left alone.
* As a global variable, it's storage agnostic. The user is free to store the key in an environment variable, 
  a secrets manager, a database (hopefully encrypted), etc.
