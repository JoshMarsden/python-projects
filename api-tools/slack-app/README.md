# Daily VIM Tips

A Slack app bot that posts a new tip or trick daily (07:00 PST) about using
VIM.

## How to make your own Slack app
1. You have to be an admin or have the admin's permission to add an app to a
   Slack workspace
1. In a web browser, visit https://api.slack.com/apps and click "Start
   Building"
1. Enter the required Basic Information and the look for _Incoming Webhooks_
   under the **Features** header
1. Activate incoming webhooks by clicking the on/off slider
1. At the bottom of the page, click "Add New Webhook to Workspace" to reveal
   a new webhook url that you can save for later

## Files that make the app work
| Filename | Description |
| -------- | ----------- |
| vimtips.py | Main Python script that handles the features |
| tips.txt | Input file containing a starter list of VIM tips |
| linecount.py | Mutable file to keep track of last processed tip in _tips.txt_ |
| sample-creds.py | Holds the webhook URL for the Slack app. Rename this to creds.py once you input your webhook URL |
