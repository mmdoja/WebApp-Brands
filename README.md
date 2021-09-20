## AMAZING BRANDS WEBAPP

The backend of the webapp has been built on Flask and frontend using basic HTML CSS. 
Install requirements using
```
pip3 install -r requirements.txt
```
To run it locally, use
```
python3 main.py
``` 
The port has been set to 5001 to avoid clashes between marketplace-api and marketplace-scraper.


**Basic endpoints:** 

- http://localhost:5001/  
- http://localhost:5001/home  
- http://localhost:50001/login 
  - Opens the login page
- http://localhost:5001/register
  - Opens the sign up page
- http://localhost:5001/reset_password
  - Reset password page
  

**Endpoints requiring login:**  

- http://localhost:5001/jobs
  - The main dashboard
- http://localhost:5001/forms/job
  - To add a brand to the dashboard
- http://localhost:5000/forms/query
  - A simple form to build a query
- http://localhost:5001/account
  - Account update option
- http://localhost:5001/logout
  - Logout from the session
