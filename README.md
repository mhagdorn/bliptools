# bliptools
tools for handling blipfoto journals

## Configuration
The bliptools need a configuration file with an API access token which can be generated on the [blipfoto developer page](https://www.blipfoto.com/developer/apps). The configuration file should have the following entries:

```
[general]
accesstoken = SOME_LONG_HEX_STRING
client_id = ANOTHER_HEX_STRING
username = blipname
baseurl = https://api.blipfoto.com/4/
```

By default bliptools will look for the configuration in `~/.bliptools`.
