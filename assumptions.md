---
AUTH TEST
---

# Auth_Register

- u_id will generate through UUID

# Test_auth_login

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

---

CHANNEL TEST

---
If a user leaves a channel, they will be removed as a member and owner (if they are an owner)

---

CHANNELS TEST

---

When user calls channels_create, they are automatically part of the channel as an owner and member
Making all channels public at the moment
