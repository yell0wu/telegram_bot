# telegram_bot

A python bot for [CoderInc's telegram channel](https://t.me/codercoin) that answers questions about the Coder platform.

Uses [python telegram wrapper](https://github.com/python-telegram-bot/python-telegram-bot).

## Installation
You can install the wrapper with:
```
pip install python-telegram-bot --upgrade
```

# Usage
The bot is built for Python 3.7.0 and can be run by doing
```
python coderbot.py
```

## Changing FAQ or Links
Changing FAQ or Link values can be done simply by editing the respective json files.

### faq.json
**Adding or Removing Sections**

This is a section containing all of the sections and questions listed in the /faq command.

To add a section, follow the same format and naming pattern, and create section_#, where # is the next numerically increasing number.
1. **ID** should be the same as the section name.
2. **Label** is the text to be displayed on the button.
3. **Content** is a dictionary of the questions.

**Changing Questions**
- The name of each question should be the same as the **ID**, as shown below.
- Change the **ID** of a json entry to change the #command that responds with the answer to the FAQ. Change the name of the entire question element as well.
- Change the **LABEL** of a json entry to change the question displayed when the faq command is called.
- Change the **RESPONSE** of a json entry to change the response for the respective question.


Place the questions in the appropriate section.


**Example:**
```json
{
  "section_24": {
    "id": "section_24",
    "label": "Questions about Coder",
    "content": {
      "about": {
        "id": "about",
        "question": "What is Coder?",
        "response": "Coder is a platform for accelerating the development and growth of innovative new ventures."
      }
    }
  }
}
```

This is **SECTION_24**, which appears as a button that is labelled "**Questions about Coder**".
Upon entering the section, the user is presented with the question: "**What is Coder?**".
Once the question is selected, the answer "**Coder is a platform...**" is displayed, which can be quickly accessed by using the hashtag **#about**.

Tip: Be careful of trailing commas! Adding questions in the middle will help.


### links.json
- Change the **ID** of a json entry to change the #command that responds with the appropriate link. Make sure you change the name of the entire section as well.
- Change the **LABEL** of an entry to change the title displayed when the command is called.
- Change the **RESPONSE** of a json entry to change the response for the respective #command.


**Example**:

```json
{
  "coder": {
    "id": "coder",
    "label": "What is Coder?",
    "response": "Coder is a platform ..."
  }
}
```

This can be accessed by using the hashtag command "**#coder**".
The bot then responds with "**What is Coder?**" in bold and right below: "**Coder is a platform..***"

## Features
#### /faq:
- Presents the user with a menu of commonly asked questions using an inline keyboard.
  - When a question is selected, the bot will answer appropriately.

#### /help:
- Lists all commands.
- Access faq answers quickly or get links to Coder's social media using # commands.

**Available links**

Command | Response
---|---
`#website`|https://www.codercoin.io/
`#whitepaper`|https://www.codercoin.io/whitepaper
`#twitter`|https://twitter.com/coderinc
`#telegram`|...
`#slack`|...
`#reddit`|...
`#medium`|...
`#video`|...

In addition, **each faq question** has its own id, which can be prefixed with a hashtag to get the answer immediately.

#### Welcome:
- Displays a welcome message when the user joins the room.
- Can be edited by changing the file /data/welcome.txt.
  - {name} represents the user's first name, and will display their name in the welcome message.
