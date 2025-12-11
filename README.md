# Slack

The task is to create an automatic connection
list to Slack via the WEB API

**How it work?**

The system connect to the slack by token and
slack-router and received all the items of
channels that in this slack.

**How to run?**

```bash
docker build -t <your image> .
```

and then

```bash
docker run -v .:/app <your image>
```

if you want to add user you need to run:

```bash
docker run -v .:/app python --user-id <user_id> --name <name> --email <user_email>
```

This command is to copy a file created in Docker to your folder!
