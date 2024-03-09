# custom-gpt

CUSTOM GPT

Product Description:
This project is intended to provide a framework for using an LLM (ChatGPT) to navigate any dataset that's fed to it. It's intended to be used as a cusom AI that can be fed specific datasets to fill various end-user needs. For instance, if you work in a large organization, and you want an advisor that has the most up-to-date policy and regulations, you could feed live up-to-date information to this custom AI and it would be able to feed you back relevant and accurate responses.

# ------------------------------------------------------ #
v1.0

Features ->
-Dark mode UI (prepped for toggle/menu option)
-Quick AI word fill response (similar to Chat-GPT's)
-Auto scroll that follows word population
-Tie-in for providing AI context

Features to come ->
-Ability to pull data from another file (JSON, CSV, etc.)
-Working memory
-Conversation storage

Identified issues that need to be resolved->

Programming:
-LLM has no working memory
-Current code structure does not scale
-No error handling
-No tests
-No response limit
-Program continues to run when closed

UI:
-No options menu
-Only dark mode
-Dark mode scrollbar and entry colors are default colors
-Submit button is vanilla
-User input into the entry and message window is hidden
    when reaches a certain length

Would be nice-to-haves ->
-User profiles
-Web interface (web-scraping plug-in?)
-Installable to the Desktop (pyinstall...)