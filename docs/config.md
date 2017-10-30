# Configurations overview

## YouTube OAuth2

To interact with the YouTube channel, OAuth2 is required. The OAuth2 credentials file `client_secrets.json` should be downloaded from [Google's API console](https://console.developers.google.com/apis/credentials) (you'll need to create a project if you haven't already done so) and placed in `config/`.

Actual client credentials are generated automatically at `config/credentials-<scope>[,<another scope>,...].json`. Whenever a client with a new set of scopes is initialized for the first time, a browser session will open up to let you authorize the client. If you're on a headless server, this is apparently a problem since a browser window would not open up there, in which case you should use the `--noauth_local_webserver` command line option, e.g.,

```console
$ upload --noauth_local_webserver sample.mp4
.../lib/python3.6/site-packages/oauth2client/_helpers.py:255: UserWarning: Cannot access .../config/credentials-youtube.upload.json: No such file or directory
  warnings.warn(_MISSING_FILE_MESSAGE.format(filename))

Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/...

Enter verification code:
```

Now you can paste that link into your local GUI browser, finish the authorization, and paste the verification code back to complete the flow.


## `main.yml`

`config/main.yml` is used to customize the behavior of certain tools. Currently available customizations:

```yaml
notifications: on
mailto: webmaster@example.com
```

Explanations:
- `notifications`: `on` or `off`. Default is `off`. If turned on, `download` and `upload` will send email notifications after the completion of key operations, or when an uncaught exception has crashed the script. The recipient is specified in `mailto`. Emails are sent using Gmail's API from the account that owns `client_secrets.json`.
- `mailto`: an email address, e.g. `webmaster@example.com`. Required if notifications are turned on, in which case it is used as the recipient; unnecessary otherwise.
