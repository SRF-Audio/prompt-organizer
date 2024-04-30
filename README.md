# prompt-organizer
A Python utility that helps to organize prompts for LLM's when you are dealing with multiple files.


## Background
Often, when you are using an LLM to help with coding, you may have multiple file contents in different locations that need to paste into the prompt. I've found that models get easily confused unless you are very organized. 

But being organized gets really tedious. I often have to manually make a prompts like: 

> Please help me debug the errors in these files:
> Error message:
> ```
> Some error message.
> ```
>
> <filename 1>
> ```
> file 1 contents
> ```
> 
> <filename 2>
> ```
> file 2 contents
> ```

This utility streamlines that process by organizing numerous files for you into a single prompt for cutting and pasting. 

## Usage
Clone the repository to your desired location, and run it using the form: 
- `python prompt-organizer.py -d <path_to_my_directory>`
- `python prompt-organizer.py -f <path_to_my_file>`

Paths can be: 
- absolute `/Users/MyUser/myDirectory/myfile.json`
- or relative `./myfile.json`

Flags can be combined:
- `python prompt-organizer.py -d <path_to_my_directory_1> -d <path_to_my_directory_2>`
- `python prompt-organizer.py -d <path_to_my_directory> -f <path_to_my_file_1> -f <path_to_my_file_2>`

This script can be triggered from any location in your terminal, so you can pass the `.` argument:
- Suppose you are in `~/GitHub/my-project`, and you need all the files in your current directory to be in the prompt
- the script lives in `~GitHub/prompt-organizer`
- run `python ../prompt-organizer/prompt-organizer.py -d .`

By default, the script outputs results directly to the console, with the intent being to pipe it directly into your clipboard, like so:

### Windows PowerShell
`python prompt-organizer.py -d <path_to_my_directory> | Set-Clipboard`
### MacOS
`python prompt-organizer.py -d <path_to_my_directory> | pbcopy`
### Linux
`python prompt-organizer.py -d <path_to_my_directory> | xclip -selection clipboard`



### Options
Run `python prompt-organizer.py -h` for the full list of help options.

Example Usage with file output:
- You clone this repository at: `/Users/my-user/GitHub/prompt-organizer`
- The code you need help with is in two locations:
  - 4 files under `/Users/my-user/GitHub/config/apps`
  - the file `/Users/my-user/Documents/test.js`
- Your current working directory is: `/Users/my-user`
- Run `python ./GitHub/prompt-organizer/prompt-organizer.py -d /Users/my-user/GitHub/config/apps -f /Users/my-user/Documents/test.js -o`
- Your results will be created at `/Users/my-user/GitHub/prompt-organizer/outputs/gpt-prompt-code-YYYY-MM-DD-HH-MM-SS.txt`

