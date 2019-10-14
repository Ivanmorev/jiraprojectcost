# jiraprojectcost
A simple script to calculate the cost of tasks by jql filter

## Install

```bash
$ git clone https://github.com/Ivanmorev/jiraprojectcost
$ mkvirtualenv jiraprojectcost
$ pip install -r requirements.txt
```

## Usage

The first thing you'll need to do is **get your Jira Username and Password**. 

 Once you have your username and password you can do:

```bash
$ speech_to_text -u <MY-USERNAME> -p <MY-PASSWORD> -f html -i <AUDIO-FILE> transcript.html
```

## Formatters

There are currently 4 formatters builtin: `html` (default), `markdown`, `json`, `original`. You can pass the `-f` option with any of those formatters in place.

## Examples



#### Jira JQL Documentation

https://www.atlassian.com/blog/jira-software/jql-the-most-flexible-way-to-search-jira-14