# server

## SETUP 

- Read through & complete tutorials @ https://fastapi.tiangolo.com/
- To deal with testing, you need to create a python virtual environment and instasll with requirements.txt
- Server depends on running DB instance, so best to run as entire stack with top-level scripts/setup.sh 
    - Due to this, the Dockerfile here may or may not be useful 
  
## TESTING

### Integration

Relies on running the docker-compose.
This WILL clear the local DB so do NOT under any circumstances run it in production or where the data is critical.

Test using 'pytest' with a targeted directory (integrations). Search this up for more information.