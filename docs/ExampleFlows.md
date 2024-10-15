# API Spec Flow

1. Account Creation

    The API calls are made in this sequence when creating and editing an account:

1. `Register User`
2. `User Login`
3. `Update Account`

    User will come into the website and click create register account in order to use the provided services. In creation, they will provide their User ID, age, weight, and height. For reference, there will be no authorization to access the website.

    User starts by calling POST /RegisterUser/ 
    User passes in their values into the entries.
    User finalizes their entries with POST /RegisterUser/Create/

    If the user enters a wrong unit or they happen to change in weight/height, they can go to settings and edit the entries.

    User will start by calling POST /UserSettings
    User will pass new values via /UserSettings/UserAttributes
    User will save their new settings via /UserSettings/UserAttributes/Save

    