# Python3 Google Cloud DNS Updater

This utility runs in Google Cloud Functions and allows for the remote update of DNS records from dynamic clients using a key.



## Basic usage

Configure the application using ENV variables (Preferably with Secrets mounted at runtime)  
The following configuration is required:
```
  app:
    0:
      apiKey: <API service key>
      hostname: <hostname associated to apiKey>
    1:
      apiKey: <API Service Key>
      hostname: <hostname associated to apiKey>

    project: <project name>
    authKeyJsonFile: <auth json file path>
    dns:
      zone: <zone name>
      domain: <domain>
```

Call the function using the below format (example.sh):  
```
#!/bin/sh

IPADDRESS_V4=`curl https://api.ipify.org/?format=plain` &&
IPADDRESS_V6=`curl https://api64.ipify.org/?format=plain` &&


# toenniges.net
curl -X POST <Function URL> -H "Content-Type:application/json" --data '{"host":"exaple.com.", "ipv4":"'$IPADDRESS_V4'", "ipv6":"'$IPADDRESS_V6'", "key":"<API service key>"}'

```
