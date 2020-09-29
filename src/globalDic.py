data = {
    "users": [
        {
            "user_id" : 0,
            "email": "test@gmail.com",
            "first_name": "Test",
            "last_name": "Hu",
            "status": "active",
            "password": "test@12345",
        },
        {
            "user_id" : 1,
            "email": "testDummy@gmail.com",
            "first_name": "Test",
            "last_name": "Hu",
            "status": "inactive",
            "password": "test@12345",
        },
    ],
     "Channel": [
        {
            "name": "channel_name",
            "channel_id": 1,
            "owner_members": [
                {
                    "user_id": 1,
                },
            ],
            "all_members": [
                {
                    "user_id": 1,
                },
            ],
            "messages": [
                {
                    "user_id": 1,
                    "message_id": 1,
                    "message": "Hello world",
                    "time_created": 1582426789,
                },   
            ],
            "start": 0,
            "end": 50,
        },
    ],
    "Channels": [
        {
            "public": [
                {
                    "channel_id": 0,
                }, 
            ],
            "private": [
                {
                    "channel_id": 1,
                },
            ],
        },
    ], 
}
 

