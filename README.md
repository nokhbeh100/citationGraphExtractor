# CitationGraphExtractor
This is a python code that extracts citation graph around a single (or multiple) articles 
through [microsoft academic](https://academic.microsoft.com).

There are two versions, the first version is a simple crawler.
It goes article by article with a depth limit (hops) around a central article noted by paperid.
The second one expands whatever article that is mentioned that once, meaning that it is an important article and not an article that was only relevant to one work.
For this, you need at least two central articles and call the expand function on their IDs.
