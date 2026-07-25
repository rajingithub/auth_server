we will be supporting user level authentication(where user gives username/email and password) and get authenticated and 
machine level authenitcaton (like background workers like AWS Lambda, application details like client_id and client_secret)
and provides access token (with expiry )which will be used in subsequent API calls to identify user/application.


we have 2 types of application types in OAuth2 implementation.
confidential : Applications which can maintain client_secrets confidentially (used mainly in M2M Authentication)
public : Application which cannot main client_secret confidentially (User Facing Applications username&password)

-> client_secret is generate and shown only once and its hash is stored in DB. if lost we need to generate new client_secret,retrieving existing token from hash is not standard practise/not possible.

we will be using 2 grant types.
1. password : if the client app is internal and user gives username and password directly 
    then we can use this grant type
2. client_credentials : Machine to Machine authentication (done by client_secrets)

