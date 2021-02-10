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

## Install
Clone the repository. Then copy the `.env.dist` file as `.env`, and fill variables : 
```
BOT_TOKEN=insert_here_your_bot_secret_token
```