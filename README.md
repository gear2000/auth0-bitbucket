**Description**

  - This is simply a step by step how to set up Bitbucket authentication with Auth0 as a broken.  In particular, this includes refresh token needed to renew the access token.

# Accounts:

Domain: 
    Auth0 account
    Bitbucket domain (main)

User Account:
    Bitbucket user accounts 

# Get Bitbucket client id/secret

   - We need to set up and acquire the main Bitbucket account (not user account) that will be used for Auth0 domain.
    
     * Login into the domain Bitbucket Account
     * Go to "Bitbucket settings" -> Access Management -> OAuth - OAuth consumer
     * Add consumer shown
     * Take note of the client id/secret as shown


     * We will export these environmental variables

     e.g.

       * export BITBUCKET_CLIENT_ID=KeyJx24sbQYxvXvpNeEg3
       * export BITBUCKET_SECRET=SecretwR8wxbcDNBWsku8qTqxU8RrRCubjpSP3
