# DPOPS Monitor For Delegates

# About
Discord Bot monitor which can be deployed by anyone on their private server. 


# Integrated functions

- [x] Voter 
    - [x] Management of own voter profile
        - [x] Apply public key for easier queries presented below
    - [x] Voter queries with or without registered profile
        - [x] Last 4 payments sent by delegate for voter
        - [x] Current state of the voter in delegate

- [x] Server owner
    - [x] block tracking
        - [x] Register for automatic notifications when delegate produces new block
    - [x] DPOPS Stats
        - [ ] Daily overall statistical snapshots of delegate

- [ ] X-Cash DPOPS network queries
    

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


## 2. Install requirements:

### 2.1. Mongo Database

[Mongo Installation Instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

when installation completed 

```shell script
$ sudo service mongod start
```

### 2.2. PIP installation 
[pip3/pip installation instructions](https://pip.pypa.io/en/stable/installing/) (Mandatory)**
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
- Create application and obtain bot token and ID ([How to](https://www.writebots.com/discord-bot-token/))
- Create Bot Invite link with with [Discord Permission Calculator](https://discordapi.com/permissions.html#0)

```text
# Permission code when creating invitation link
359489
```

- Invite bot to the community by clicking on link created through previous step
    - All necessary permissions will be set automatically once bot joins

#### 2.5. Bot Setup

go to main project folder and create file name:
```text
botSetup.json
```

with content:
```json
{
  "command": "COMMAND CHARACTER",
  "token": "BOT TOKEN OBTAINED IN STEP 2.4.1 ",
}

Example:
{
  "command": "!",  // Bot will listen to command string ! or @botTag
  "token": "cdscdscds.YAJ5uw.dockasmsdcasdcdascdasca",   // Bot token 
}
```

