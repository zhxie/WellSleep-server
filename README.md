# WellSleep Server

Wish you a well sleep. This is the server for [WellSleep](https://github.com/zhxie/WellSleep).

## API

URI             | Method | Operation                     |
----------------|--------|-------------------------------|
/register       | POST   | Register a user               |
/update_profile | POST   | Update the profile for a user |
/check          | POST   | Check in and out              |
/follow         | POST   | Follow a user                 |
/unfollow       | POST   | Unfollow a user               |
/user           | GET    | Get the profile of a user     |
/activities     | GET    | Get the activities of a user  |
/followers      | GET    | Get the followers of a user   |
/timeline       | GET    | Get the timeline              |
