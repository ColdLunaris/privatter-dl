# privatter-dl
Python tool to download images from Privatter. Currently only tested on Linux.

## Requirements
Python 3

These pip modules:
```
requests
termcolor
beautifulsoup4
```

You can install them with this command:

`pip install requests termcolor beautifulsoup4`

If you still get an error for missing modules, that's when Google helps you out.


## How to use
| Argument | Description |
| --- | --- |
| `-v VALUE` | Output URLs while downloading. Either True or False. True if not specified |
| `-d PATH` | Specify output-directory. Current directory if not specified |
| `-U LOGIN_ID` **REQUIRED** | Specify username for Privatter-login |
| `-P PASSWORD` **REQUIRED** | Specify password for Privatter-login |
| `-u URL` **REQUIRED**| Specifies which link to look for images | 

`python ./privatter-dl.py [-v VALUE] [-d PATH] -U LOGIN_ID -P PASSWORD -u URL`

### Use with Login ID
1: Open [Privatter](https://privatter.net/) and login with your Twitter account.

2: After logging in, click the arrow in the top-right corner and open Settings.

3: Find the "Login ID setting" and set a username and password.

4: Use the same credentials when running privatter-dl.

### Example

`python ./privatter-dl.py -d '/mnt/tank/privatter-archive/' -U 'NotARealUsername' -P 'NotARealPassword' -u 'https://privatter.net/ID HERE/' -v True`
