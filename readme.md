# Discord Reminder Bot

## Usage

Reminder Bot is a simple Discord bot that allows you to set a reminder for later.

To use it, put a command in a text channel. Commands start with the `$rm` prefix.

Examples : 
```
$rm add 30/1/2021 20:30:45
$rm add 20:30
$rm add 30/1/2021
```

To get help, use the prefix without parameter : 
```
$rm
```

Update :

This also tells you when a new video is published on a youtube channel.

To use it, put a command in a text channel. Commands start with the `$ytb listen` prefix. Then, add the youtube channel Id (through the youtube url or via https://commentpicker.com/youtube-channel-id.php)

Example :
```
$ytb listen add UC1KxoDAzbWOWOhw5GbsE-Bw
```

To get help, use the prefix without parameter : 
```
$ytb listen
```


## Install
Clone the repository. Then copy the `.env.dist` file as `.env`, and fill variables : 
```
BOT_TOKEN=insert_here_your_bot_secret_token
UTC_OFFSET=insert_offset_with_utc_time_in_hours
```
`UTC_OFFSET` parameter can be removed. In that case, the system's timezone will be used.

In order to execute queries on youtube API, you need to reference your Google account.
If you already have a code secret client file, just put its name in the `.env` file.
If you don't, create your own project through Google API console, then create an `ID client OAuth` creditential and download the file with your creditentials.