# server

* On a high-level consists of the FastAPI web framework and sqlalchemy for ORM 
* server should ideally be deployed with a running db instance as it is dependent on the db
* <u>To see detailed endpoint information run the server & db together with defaults and go to (server URL)/docs, where server URL is typically localhost:80</u>



## Notice

**<u>init.sh may fail in docker setup, locally on a Windows 11 machine the solution we found was to copy + paste the init.sh code, delete the init.sh, make a new init.sh, copy + paste code back in. It has to do with Windows line endings and such that aren't necessarily compatible with Linux distros (ie Ubuntu)</u>**



## Structure

* /app/config.py
  * central place for dynamic configurations / settings 

* /app/db.py 
  * shared database-related functions using ORM library 

* /app/main.py
  * main deployment point as specified with FastAPI 

* /app/backtest_engine
  * code for executing backtests submitted by user after OK response has been sent 

* /app/models
  * contains database object representations using an ORM, and models, inspired by Django, contain the bulk of the logic 

* /app/routers
  * 'thin' views wherever possible in relation to Django, holds the endpoints and are divided into distinct root endpoints (ie user vs backtest)

* /app/schemas
  * introduced by FastAPI for validation on inputs and/or responses on endpoints 

* /app/utils
  * small utilities shared across modules

* /app/tests 
  * contains test information, notably <u>real_stress_generate.py</u> for stress testing
  * <u>as of 11/18/2021 the only thing guaranteed to work is real_stress_generate.py</u>. Other tests have been abandoned and are likely to be outdated, but their code clearly shows how to create integration tests (tests which run with the actual running db instance and modify it, so these should only be run locally or on a test instance). Test using 'pytest'. 



## Development

* Read through & complete tutorials @ https://fastapi.tiangolo.com/
* To deal with testing, you need to create a python virtual environment and install with requirements.txt
* Server depends on running DB instance, so best to run as entire stack as in top-level repository README.md 

