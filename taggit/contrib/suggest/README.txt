
taggit.contrib.suggest 
======================

This add on module allows you to easily associate keywords and regular 
expressions with a Tag object. This is useful to help keep your database
getting filled up with several similar tags that really represent the same thing.

For example, if your site is a humor site you might want to collapse all of 
#fun, #funny, #funnies, #hilarious, #rofl, and #lol into one tag #funny.  The
suggest_tags() function in taggit.contrib.suggest.utils will give you a list
of tags that seem appropriate for the text content given to it.  

It will also do some basic stemming of the keywords for you! Which requires the 
Python NLTK. 

In a later version I hope to a simple way to help determine keywords for you
automatically, by learning from your past tags and content. 

