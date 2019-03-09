#!/usr/bin/python3

# Built-in imports
import sys       # for sys.exit()
import requests	 # for POST requests
import time      # for schedule timing

# Third party imports
import schedule  # to replace dumb crontab

# Local imports
import creds     # for webhook URL
import linecount # to keep track of unprocessed lines


def log_write(text, fname='logvimtips.log'):
    """Writes the given text to a log file."""

    with open(fname, 'a') as app_log:
        app_log.write(text)


def slack_tip(tip):
    """Uses a pre-defined webhook to send a tip to the Slack channel."""

    text = tip
    json_data = '{{"text": "{}"}}'.format(text)
    # Send the request
    r = requests.post(url=creds.webhook, data=json_data)
    
    # Log status and returned text
    log_write('Status: {}\tText: {}\n'.format(r.status_code, r.text))


def read_line(filename='tips.txt'):
    """Returns next unprocessed line from input file."""

    new_tip = ''
    temp_count = 0
    with open('tips.txt', 'r') as tip_file:
        for line in tip_file:
            temp_count += 1

            try:
                new_tip = line
                # Break the loop when an unprocessed line is found
                if temp_count > linecount.count:
                    with open('linecount.py', 'w') as lcpy:
                        # Update variable for next time
                        lcpy.write('count = %s\n' % temp_count)
                    break
            except Exception as e:
                # Log any errors for future reference
                log_write('Exception: {}\nwhile trying to read line from file "{}"'.format(e, tip_file.name))
                return ''

    if temp_count == linecount.count:
        # If true, no new tips have been found, so quit
        # In the future, send text to notify me to add more tips
        sys.exit(1)

    return new_tip


def main():
    """Wrapper for the main application code."""
    new_tip = read_line()

    try:
        slack_tip(new_tip)
    except Exception as e:
        # Log any errors for future reference
        log_write('Exception: {}\nwhile trying to send string "{}"'.format(e, new_tip))


# Replacement for the stupid crontab. Why no work???
schedule.every().day.at('15:00').do(main)


if __name__ == "__main__":
    #log_write('testing, testing\n', fname='test.log')
    #main()
    while True:
        schedule.run_pending()
        time.sleep(1)
