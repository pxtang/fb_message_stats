# Facebook Message History Statistics
By @pxtang

## What is it?
I was curious about my message history - character statistics, message statistics, visual history, etc. I decided to download my Facebook Messenger history and analyze it.

## Requirements
I developed this on Python 3.6. A requirements.txt is also included, but all you need is `matplotlib`.

## How do I use it? 
1. Go to [https://facebook.com/dyi]() and click "Download a copy of your Facebook data"
2. Download your message information. Format: JSON. Media quality: Low (makes it faster to download). Date range should be the date range you're interested in.
3. Deselect everything but messages.
4. Click "Create File" and wait for it to finish! ⏳ Download the .zip file.
5. Put message_stats.py in the same directory as the messages.py extracted from the .zip - this is hacky but ¯\\\_(ツ)_/¯

## Usage
`python3 message_stats.py -file messages.json -stat [stat_option] -name "Foo Bar"`

`stat_option` options:  
`lengths`: Tells you about the character and word counts per message, totals, std dev, etc.  
`history`: Plots a history of all the data it can find. Attempts to do months but just does an okay job at it.

The name after -name needs to fully match the Facebook name of the person you're chatting with as of the date you downloaded info. It is not the nickname you may have given them.

## Your code could improve
I agree! Please help me :)

## Something threw an exception! Your code is horrible!
File an issue with a stacktrace and I'll probably not get around to fixing it