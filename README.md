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

Call the function using the below format:  
```
curl -X POST \
    -d 'host=<Host name>&ip=<IP Address>&key=<API service key>' \
    http://localhost:8080/records
```
