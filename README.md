# Pwncat-cs-Modules
Base path : `~/.local/lib/pythonX.XX/site-packages/pwncat`

## upload_tools.py
Put this into the commands folder ( /pwncat/commands )
Pwncat has a hard time uploading zip files so when you see the first progress bar at 100%, you can CTRL+C to stop the command.

You can change the default path ( to avoid having to specify it everytime ) on line 27 ( same for destination )

```
upload_tools 
upload_tools localPath
upload_tools localPath remotePath
```

<img width="1904" height="842" alt="image" src="https://github.com/user-attachments/assets/976fcdcb-3952-4e5a-b706-5616caa7224d" />
