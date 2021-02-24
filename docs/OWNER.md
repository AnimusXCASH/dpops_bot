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
