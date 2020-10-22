# global dict that will be populated as functions are called
data = {
    "users": [],
    "channels": [],
}

num_messages = 0
'''
An example of how data would look like when populated
data = {
    "users": [
        {
            "u_id": 0,
            "email": "test@gmail.com",
            "first_name": "Test",
            "last_name": "Hu",
            "status": "active",
            "password": "test@12345",
        },
        {
            "u_id": 1,
            "email": "testDummy@gmail.com",
            "first_name": "Test",
            "last_name": "Hu",
            "status": "inactive",
            "password": "test@12345",
        },
    ],
    "channels": [
        {
            "name": "channel_name",
            "channel_id": 1,
            "is_public": True,
            "owner_members": [
                {
                    "u_id": 1,
                },
            ],
            "all_members": [
                {
                    "u_id": 1,
                },
            ],
            "messages": [
                {
                    "u_id": 1,
                    "message_id": 1,
                    "message": "Hello world",
                    "time_created": 1582426789,
                },
            ],
            "start": 0,
            "end": 50,
        },
    ],
}
'''
