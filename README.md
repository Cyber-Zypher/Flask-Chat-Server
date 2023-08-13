
# Flask Chat Server with MySQL Integration
A Simple Flask chat server system made with Python and MySQL Database.
The Code uses PyMySQL Python Library to function. This code has a very simple syntax which makes it easy to understand and beginner friendly.
Users can simply type the IP of the Host system and Register/Login with their accounts to start chatting.
- Clear the chat once you done chatting.
- Mobile Optimized UI
- Export the chats to CSV File.


## Install the required Libraries.

Clone the project

```
pip install pymysql
```
or
```
python -m pip install pymysql
```

## Initialize the Database
```
CREATE DATABASE CHATSERVER;
USE CHATSERVER;
CREATE TABLE chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
```
## Authors

- [@sidharth_everett](https://github.com/Cyber-Zypher)

