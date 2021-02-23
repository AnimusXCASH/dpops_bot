
# Installation
Note: Following installation steps assume that you are on a Linux environment.

## 1. Clone repo 
- **Update the system**

```shell script
$ sudo apt update
```

- **Clone this repo to your local machine using**

```shell script
$ git clone https://github.com/AnimusXCASH/dpops_bot.git
```


## 2. Install requirements and setup project:

### 2.1. Mongo Database

[Mongo Installation Instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

when installation completed 

```shell script
$ sudo service mongod start
```

### 2.2. PIP installation 
[pip3/pip installation instructions](https://pip.pypa.io/en/stable/installing/) (Mandatory)
```shell script
$ sudo apt install -y python3-pip
$ pip3 --version
```


### 2.3. Install package requirements for project:

- Install build tools  

```shell script 
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```

-  **CD to main project folder and install requirements.. this will install all required packages for x-payment to function
optimally (Mandatory)**
```shell script
$ pip3 install -r requirements.txt 
```


### 2.4. Discord part 
#### 2.4.1. Register developer account required for bot to operate
- [Register Discord developer account](https://discordapp.com/developers)
- Create application and obtain bot token, ID and activate Privileged gateway intents ([How to](https://www.writebots.com/discord-bot-token/))
```text
Be sure to activate on developer web page PRIVILEGED GATEWAY INTENTS

Presence Intent
Server Members Intent 

```
- Create Bot Invite link with with and check required permission for bot to operate normally bellow.
[Discord Permission Calculator](https://discordapi.com/permissions.html#0)

```text

Required permissions:
- Manager Server
- Manage Channels
- Read Messages
- Send Messages
- Manage Messages
- Embed Links
- Attach Files
- Read Message History
- Mention @everyone, @here, etc...
- Use External emojis
- Add Reactions

# Final Permission Code value when all activated 
518256
```

- Invite bot to the community by clicking on link created through previous step
    - All necessary permissions will be set automatically once bot joins

#### 2.4.2. Bot Setup

go to main project folder and create file name:
```text
botSetup.json
```

with content:
```json
{
  "command": "COMMAND CHARACTER",
  "token": "BOT TOKEN OBTAINED IN STEP 2.4.1 ",
  "dpopsApi": "dpops api link from dpops web page" 
}

Example:
{
  "command": "!",  // Bot will listen to command string ! or @botTag
  "token": "cdscdscds.YAJ5uw.dockasmsdcasdcdascdasca",   // Bot token 
  "dpopsApi": "http://xpayment.x-network.eu" 
}
```

## 3. Bring the bot to life
In main project folder run 

```
python3 main.py
```


