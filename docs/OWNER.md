# OWNER 

Commands available for owner of the Discord Community. This area of commands can be accessed
 only throught the public channels of the server so ownership rights can be verified

## Access entry command

```text
@botTag sys
```

### Set/ apply for various services
```text
@botTag sys set
```

### Delegate block tracking 
Bot monitors for new blocks every 2 minutes.

```text
@botTag sys set block
```
#### Set Starting blockheight 
```text
@botTad sys set block height <block number>
```

#### Set Channel where notifications will be sent
```text
@botTad sys set block chn <#discord.Channel>
```
Note: channel needs to be visible to bot and tagged when executing command, so appropriate
channel id can be obtained

#### Turn the service ON/OFF
```text
@botTad sys set block monitor <ON/OFF>
```

Before you turn on the monitor you MUST set starting block height as well as channel where bot has access to, otherwise the block monitor service will NOT wwork. 



