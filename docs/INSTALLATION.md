
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

### 2.4. Wallet RPC setup 
Running wallet CLI RPC is required since the bot checks for outgoing payments to voters and send notification 
to channel. 

```text
Steps:
1. Download XCASH Cli wallet 2.0 or greater for operating system
2. Import delegate wallet through  mnemonic seed
3. Download the blockchain to computer or use remote daemon to connect to RPC wallet (see command bellow for remote)

```

#### Local daemon

```text
# Run on ubuntu in separated terminal
./xcashd

# Windows  in CMD terminal
xcashd.exe 
```

Activate RPC

Switch WALLET_NAME and PASSWORD with exact details used when importing to wallet

```text
# Ubuntu
./xcash-wallet-rpc --wallet-file WALLET_NAME --password PASSWORD --rpc-bind-port 18285 

#Windows
xcash-wallet-rpc.exe --wallet-file WALLET_NAME --password PASSWORD --rpc-bind-port 18285
```

#### Remote Daemon

Switch WALLET_NAME and PASSWORD with exact details used when importing to wallet and ADDRESS_OF_YOUR_NODE (Example: xpayment.x-network.eu:18281)
```text
# Ubuntu
./xcash-wallet-rpc --wallet-file WALLET_NAME --password PASSWORD --rpc-bind-port 18285 --disable-rpc-login --confirm-external-bind --trusted-daemon --daemon-address ADDRESS_OF_YOUR_NODE:18281

#Windows
xcash-wallet-rpc.exe --wallet-file WALLET_NAME --password PASSWORD --rpc-bind-port 18285 --disable-rpc-login --confirm-external-bind --trusted-daemon --daemon-address ADDRESS_OF_YOUR_NODE:18281
```


### 2.5. Discord part 
#### 2.5.1. Register developer account required for bot to operate
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

### 2.6. Twitter  integration (optional)
Register Twitter profile on https://twitter.com/ and create [developer account through](https://developer.twitter.com/en)

Once if developer interface, create new application and obtain: api key, api secret, access token and access seccret. 

#### 2.5.2. Bot Setup 

go to main project folder and create file name:
```text
botSetup.json
```

By default, Twitter notifications are deactivated. If you would like to activate them please chanhe the status to true
and provide all required details obtained through step 
you 

with content:
```json
{
  "command": "BOT COMMAND",
  "token": "DISCORD BOT TOKEN",
  "dpopsApi": "http://DPOPSAPI.LINK",
  "delegateName": "DELEGATE NAME",
  "voteString": "EXACT VOTE STRING BY NAME NOT PUBLIC ADD FOR DELEGATE ",
  "discordInvite": "DISCORD INVITE TO YOUR SERVER TO BE SENT TO TWITTER RANDOMLY",
  "delegatePublicKey": "PUBLIC KEY OF DELEGATE",
  "twitter": {
    "status": false,  
    "apiKey": "DEV ACC API KEY",
    "apiSecret": "DEV ACCC API SECRET",
    "accessToken": "DEV ACC PROJECT TOKEN",
    "accessSecret": "DEV ACC PROJECT SECRET"
  }
}

Example:
{
  "command": "!",  // Bot will listen to command string ! or @botTag
  "token": "cdscdscds.YAJ5uw.dockasmsdcasdcdascdasca",   // Bot token 
  "dpopsApi": "http://xpayment.x-network.eu",
  'delegateName':"X-Payment-World"  // Exact name as written on DPOPS web page
  "delegatePublicKey": "XCA1kLpg7A9c919tsQZBDYPHoLSZgCzihZPgP569CtFpJvAvQrpqW72HZzLKHRRLpSQzpdKBwJeTaUXGco7E4tHr9TynMN5yfi",
  "voteString": "vote X-Payment-World",
  "discordInvite": "https://discord.gg/qwuMhE68PG",
  "twitter": {
    "status": false,  
    "apiKey": "DEV ACC API KEY",
    "apiSecret": "DEV ACCC API SECRET",
    "accessToken": "DEV ACC PROJECT TOKEN",
    "accessSecret": "DEC ACC PROJECT SECRET"
  }
}
```
#### 2.5.2. Notification times
All notifications are based on the system time when bot is deployed in format HH:MM:SS. 
Create a new file in the main project directory called snapshotTimes.json and copy/paste data bellow for system 
default settings.


```json

{
  "delHourly": {
    "second": "00",
    "minute": "00"
  },
  "delThreeHour": {
    "hour": "00,03,06,09,12,15,18,21",
    "minute": "00",
    "second": "02"
  },
  "delFourHour":{
    "hour": "00,04,08,12,16,20",
    "minute": "00",
    "second": "02"
  },
    "delSixHour":{
    "hour": "00,06,12,18",
    "minute": "00",
    "second": "12"
  },
    "delTwelveHour":{
    "hour": "00,12",
    "minute": "00",
    "second": "10"
  },
    "delDaily": {
      "hour": "23",
      "minute": "59",
      "second": "59"
    },
    "delPaymentChk": {
      "minute": "05,10,15,20,25,30,35,40,45,50,55",
      "second": "05"
    },
    "paymentDms": {
      "minute": "05,10,15,20,25,30,35,40,45,50,55",
      "second": "10"
    },
    "delLastBlock": {
      "minute": "05,10,15,20,25,30,35,40,45,50,55",
      "second": "15"
    }
}
```

## 3. Bring the bot to life
In main project folder run 

```
python3 main.py
```


