# prompt-organizer
A Python utility that helps to organize prompts for LLM's when you are dealing with multiple files.

Often, when you are using an LLM to help with coding, you may have multiple file contents in different locations that need to paste into the prompt. I've found that models get easily confused unless you are very organized. 

But being organized gets really tedious. I often have to manually make a prompts like: 
```
Please find the errors in these files:
<filename 1>
```
file 2 contents
```

<filename 2>
```
file 2 contents
```
```

This utility streamlines that process by organizing numerous files for you into a single prompt for cutting and pasting. 

## Usage
Clone the repository to your desired location, and run it using the form `python3 prompt-organizer.py -d <my_directory> -f <my_file>`

This script can be triggered from any location.

### Options



Example Usage 2:
- You clone this repository at: `/Users/my-user/GitHub/prompt-organizer`
- The code you need help with is in two locations:
  - `/Users/my-user/GitHub/config/apps` (This has 4 files that you need the contents of)
  - `/Users/my-user/Documents/test.js`
- Your current working directory is: `/Users/my-user`
- Run `python3 ./GitHub/prompt-organizer/prompt-organizer.py -d /Users/my-user/GitHub/config/apps -f /Users/my-user/Documents/test.js`
- Your results will be created at `/Users/my-user/GitHub/prompt-organizer/outputs/gpt-prompt-code-YYYY-MM-DD-HH-MM-SS.txt`

