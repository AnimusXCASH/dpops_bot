# VOTER

Commands availabale for all voters who have voted so far for your delegate


## Access entry command

```text
@botTag voter
```

## Voter management and registrations (Opional)
No more copy pasting of your public key.

### Register yourself as voter
```text
@botTag voter management register <public address from where votes have come from>
```

### Delete/Remove voter profile from system
```text
@botTag voter management remove
```

### Review voter details
```text
@botTag boter management me
```

## Voter Status commands from voting
If voter has not registered himself into the system, a public address is required param 
to be provided, otherwise data is pulled automatically from the database. 

### Check last 4 payments
```text
@botTag voter payments <public address from where votes have come from >
```

### Check current pending payments
```text
@botTag voter payments <public address from where votes have come from>
```
