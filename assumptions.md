---
AUTH TEST
---

# Auth_Register

- u_id will generate through UUID

# Test_auth_login

- Token generated will be valid for 30mins
- Email address must exist
- Email address username, domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed.
- Email address first character of username must be an ascii letter (a-z) or number (0-9)
- Email address must contain 1 "@"
- Email address cannot contain more than 1 "@"
- Email address must have a domain after "@"
- Email address cannot have space in between
- Email address cannot contain consecutive periods (.)
- Email address domain cannot be localhost
- Email address cannot have a leading space
- Email address cannot have a trailing space
- Email address cannot exceed 254 characters
- Password cannot be empty
- Password entered has to be correct
- Multiple login connection is allowed
- None of the fields can be empty

# Test_auth_register

- Email address must not already exist
- Email address username, domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed.
- Email address first character of username must be an ascii letter (a-z) or number (0-9)
- Email address must contain 1 "@"
- Email address cannot contain more than 1 "@"
- Email address must have a domain after "@"
- Email address cannot have space in between
- Email address cannot contain consecutive periods (.)
- Email address domain cannot be localhost
- Email address cannot have a leading space
- Email address cannot have a trailing space
- Email address cannot exceed 254 characters
- First and Last name does not contain symbols
- First and Last name cannot be empty
- Password maximum size is 18
- Password minimum size is 6
- Password cannot be empty
- None of the fields can be empty

# Auth_logout

-User must be login to logout
-Logout token must exist in the dictionary
-Token removed once user logs out

---

CHANNEL TEST

---

# all functions

- comparing u_id with token for iteration 1

# channel_invite

- invitee becomes apart of all_members, but not owner_members

# channel_details

# channel_messages

- only passing through values that would result in input/acccess errors as sending messages not implemented yet for iteration 1

# channel_leave

- If a user leaves a channel, they will be removed as a member and owner (if they are an owner)

---

CHANNELS TEST

---

# all functions

- u_id == token for iteration 1

# channels_list

# channels_listall

- Returns all public channels plus any private channels the user is part of

# channels_create

- Channel name is limited to 20 character including spaces
- Channel name cannot be empty or blank spaces
- The user that calls channels_create is automatically an owner and member

---

OTHER TEST

---

# users_all

- user calling function must have valid token
- Returns the u_ids of all users including the u_id of the person calling it

# admin_userpermission_change

- Owner cannot remove their own permission
- Member cannot grant or remove other users permission changes
- Owner must promote member to owner to then remove their own ownership
- Permission id's include 1 and 2. 1 being owner, and 2 being member
- Permission id's cannot be strings or empty
- u_id of user to promote/demote must be filled with a valid token and cannot be empty

# search

- user calling function must have a valid token
- seach query must be filled and cannot be None or NULL