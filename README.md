# Pwncat-cs-Modules
Base path : `~/.local/lib/pythonX.XX/site-packages/pwncat`

## upload_tools.py
Put this into the commands folder ( /pwncat/commands )
Pwncat has a hard time uploading zip files so when you see "Draining buffer" you can CTRL+C to stop the command.

You can change the default path ( to avoid having to specify it everytime ) on line 27 ( same for destination )

```
upload_tools 
upload_tools destination
```