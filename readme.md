# Laboratory App

The service allows you to manage laboratory tests. 

It is divided into two parts:

- Patient panel - which allows to:
    - check list with surveys and parameters attached to them, which are currently provided by the laboratory
    - add many orders with selected parameters to the basket and submit order
    - check current status and the results of ordered surveys
- Laboratory Specialist panel - which allows to:
    - add new surveys to the laboratory offer
    - add new survey parameters and attach/detach them to the surveys
    - check list with pending surveys
    - fill results to the surveys

## Models
![](dbschema.jpg)



## Installation
Database file with some example data is already in the repository, so all you need to do is:
```bash
pip install -r requirements.txt
cd medical_app && python manage.py runserver
```

### TODO
- Send to patient notification with the link, when their results will be ready
- Show patients unordered items from their baskets in the last time (as CART model holds patient ID), to let them continue ordering them
- Improve table with pending surveys at laboratory specialist panel
- Clean fields at models, work on auto-removing unnecessary records from database
- Tests



