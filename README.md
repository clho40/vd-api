# API

A version controlled key-value store with a HTTP API we can query that from. The API is able to:

  - Accept a key(string) and value(some json blob/string) and store them. If an existing key is sent, the value should be updated
  - Accept a key and return the corresponding latest value
  - When given a key AND a timestamp, return whatever the value of the key at the time was.

Assume only GET and POST requests for simplicity.
Example:

> Method: POST
> Endpoint: /object
> Body: JSON: {mykey : value1}
> Time: 6pm

> Method: GET
> Endpoint: /object/mykey
> Response: value1

> Method: POST
> Endpoint: /object
> Body: JSON: {mykey : value2}
> Time: 6.05 pm

> Method: GET
> Endpoint: /object/mykey
> Response: value2

> Method: GET
> Endpoint: /object/mykey?timestamp=1440568980 [6.03pm]
> Response: value1

All timestamps are unix timestamps according UTC timezone.
