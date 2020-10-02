---
AUTH TEST
---

# Auth_Register

- u_id will generate through UUID

# Test_auth_login

- Token will be the same as u_id for iteration 1
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

Making all channels public at the moment

- The user that calls channels_create is automatically an owner and member
- The 20 character name limit includes white spaces
- Channels_listall will also include private channels
- Channel names cannot be empty or blank spaces
