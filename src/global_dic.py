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
     "Channels": [
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
 