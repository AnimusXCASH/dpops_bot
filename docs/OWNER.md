# OWNER 

Commands available for owner of the Discord Community. This area of commands can be accessed only throughout the public 
channels of the server so ownership rights can be verified

## Access entry command
Returns all available commands
```text
@botTag owner
```

## Delegate new block monitor
Bot monitors for new blocks every 2 minutes.

### Overview of all sub-commands and instructions

```text
@botTag blocks
```

#### Set Discord Channel for New Block Notifications
```text
@botTad blocks chn <#discord.TextChannel>
```

#### Set starting height
```text
@botTad blocks height <height as INT>
```

#### Turn the service ON/OFF
```text
@botTad blocks monitor on
@botTad blocks monitor off
```

Before you turn on the monitor you MUST set starting block height as well as channel where bot has access to, 
otherwise the block monitor service will NOT work. 

### Delegates snapshots/stats tracking

```text
@botTag stats
```

#### Daily stats snapshot reports 
You are required to tag the channel when setting up the tracker
```text
# Activate stats 
@botTag stats daily #discord.TextChannel on

# Deactivate
@botTag stats daily #discord.TextChannel off
```

#### Hourly stats snapshot reports 
You are required to tag the channel when setting up the tracker
```text
# Activate stats 
@botTag stats daily #discord.TextChannel on

# Deactivate
@botTag stats daily #discord.TextChannel off
```


## Payment Notifications

### Initial requirements
Bot send the notification to public channel when batch of payments is successfully sent out to voters. 
In order for this to work, you are required to have Wallet RPC running on the same computer where Discord bot 
is running as it takes details straight from delegate wallet.

```text
Steps:
1. Download XCASH Cli wallet 2.0 or greater for operating system
2. Import delegate wallet through  mnemonic seed
3. Download the blockchain to computer or use remote daemon to connect to RPC wallet (see command bellow for remote)

```

#### RPC Wallet setup 

##### Local daemon

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

##### Remote Daemon

Switch WALLET_NAME and PASSWORD with exact details used when importing to wallet and ADDRESS_OF_YOUR_NODE (Example: xpayment.x-network.eu:18281)
```text
# Ubuntu
./xcash-wallet-rpc --wallet-file WALLET_NAME --password PASSWORD --rpc-bind-port 18285 --disable-rpc-login --confirm-external-bind --trusted-daemon --daemon-address ADDRESS_OF_YOUR_NODE:18281

#Windows
xcash-wallet-rpc.exe --wallet-file WALLET_NAME --password PASSWORD --rpc-bind-port 18285 --disable-rpc-login --confirm-external-bind --trusted-daemon --daemon-address ADDRESS_OF_YOUR_NODE:18281
```

#### Discord Setup
Instruction how to setup can be obtained through

```text
@botTag payments
```
##### Apply a channel for payments notification
```text
# Activate stats 
@botTag payments apply <#Discord Text Channel>
```
Same command is used as well to change the channel 
##### Activate/Deactivate service
```text
# Activate notifications
@botTag payments on

# Deactivate notifications
@botTag payments off
```