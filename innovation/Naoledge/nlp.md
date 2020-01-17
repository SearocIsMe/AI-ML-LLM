Natural language processing (NLP) is an area of  concerned with the interactions between computers and human (natural) languages, in particular how to program computers to process and analyze large amounts of natural language data. 
An easy introduction to Natural Language Processing
Using computers to understand human language
Computers are great at working with standardised and structured data like database tables and financial records. They are able to process that data much faster than we humans can. But us humans don’t communicate in “structured data” nor do we speak binary! We communicate using words, a form of unstructured data.
Unfortunately, computers suck at working with unstructured data because there’s no standardised techniques to process it. When we program computers using something like C++, Java, or Python, we are essentially giving the computer a set of rules that it should operate by. With unstructured data, these rules are quite abstract and challenging to define concretely.

There’s a lot of unstructured natural language on the DBS; sometimes even Google doesn’t know what you’re searching for!
Human vs Computer understanding of language
Human’s have been writing things down for thousands of years. Over that time, our brain has gained a tremendous amount of experience in understanding natural language. When we read something written on a piece of paper or in a blog post on the internet, we understand what that thing really means in the real-world. We feel the emotions that reading that thing elicits and we often visualise how that thing would look in real life.
Natural Language Processing (NLP) is a sub-field of Artificial Intelligence that is focused on enabling computers to understand and process human languages, to get computers closer to a human-level understanding of language. Computers don’t yet have the same intuitive understanding of natural language that humans do. They can’t really understand what the language is really trying to say. In a nutshell, a computer can’t read between the lines.
That being said, recent advances in Machine Learning (ML) have enabled computers to do quite a lot of useful things with natural language! Deep Learning has enabled us to write programs to perform things like language translation, semantic understanding, and text summarization. All of these things add real-world value, making it easy for you to understand and perform computations on large blocks of text without the manual effort.
Let’s start with a quick primer on how NLP works conceptually. Afterwards we’ll dive into some Python code so you can get started with NLP yourself!
The real reason why NLP is hard
The process of reading and understanding language is far more complex than it seems at first glance. There are many things that go in to truly understanding what a piece of text means in the real-world. For example, what do you think the following piece of text means?
“Steph Curry was on fire last nice. He totally destroyed the other team”
To a human it’s probably quite obvious what this sentence means. We know Steph Curry is a basketball player; or even if you don’t we know that he plays on some kind of team, probably a sports team. When we see “on fire” and “destroyed” we know that it means Steph Curry played really well last night and beat the other team.
Computers tend to take things a bit too literally. Viewing things literally like a computer, we would see “Steph Curry” and based on the capitalisation assume it’s a person, place, or otherwise important thing which is great! But then we see that Steph Curry “was on fire”…. A computer might tell you that someone literally lit Steph Curry on fire yesterday! … yikes. After that, the computer might say that Mr. Curry has physically destroyed the other team…. they no longer exist according to this computer… great…

Steph Curry literally on fire!
But not all is grim! Thanks to Machine Learning we can actually do some really clever things to quickly extract and understand information from natural language! Let’s see how we can do that in a few lines of code with a couple of simple Python libraries.
Doing NLP — with Python code
For our walk through of how an NLP pipeline works, we’re going to use the following piece of text from Wikipedia as our running example:
Amazon.com, Inc., doing business as Amazon, is an American electronic commerce and cloud computing company based in Seattle, Washington, that was founded by Jeff Bezos on July 5, 1994. The tech giant is the largest Internet retailer in the world as measured by revenue and market capitalization, and second largest after Alibaba Group in terms of total sales. The amazon.com website started as an online bookstore and later diversified to sell video downloads/streaming, MP3 downloads/streaming, audiobook downloads/streaming, software, video games, electronics, apparel, furniture, food, toys, and jewelry. The company also produces consumer electronics — Kindle e-readers, Fire tablets, Fire TV, and Echo — and is the world’s largest provider of cloud infrastructure services (IaaS and PaaS). Amazon also sells certain low-end products under its in-house brand AmazonBasics.
A few dependencies
First we’ll install a few useful Python NLP libraries that will aid us in analysing this text.
 - Installing spaCy, general Python NLP lib pip3 install spacy
 - Downloading the English dictionary model for spaCy python3 -m spacy download en_core_web_lg
 - Installing textacy, basically a useful add-on to spaCy pip3 install textacy
Entity Analysis
Now that everything is installed, we can do a quick entity analysis of our text. Entity analysis will go through your text and identify all of the important words or “entities” in the text. When we say “important” what we really mean is words that have some kind of real-world semantic meaning or significance.
Check out the code below which does all of the entity analysis for us:
We first load spaCy’s learned ML model and initialise the text want to process. We run the ML model on our text to extract the entities. When you run that code you’ll get the following output:

Amazon.com, Inc. ORG Amazon ORG American NORP Seattle GPE Washington GPE Jeff Bezos PERSON July 5, 1994 DATE second ORDINAL Alibaba Group ORG amazon.com ORG Fire TV ORG Echo - LOC PaaS ORG Amazon ORG AmazonBasics ORG
The 3 letter codes beside the text are labels which indicate the type of entity we are looking at. Looks like our model did a pretty good job! Jeff Bezos is indeed a person, the date is identified correctly, Amazon is an organisation, and both Seattle and Washington are Geopolitical entities (i.e countries, cities, states, etc). The only tricky ones it got wrong were that things like Fire TV and Echo are actually products, not organisations. It also missed out on the other things that Amazon sells “video downloads/streaming, MP3 downloads/streaming, audiobook downloads/streaming, software, video games, electronics, apparel, furniture, food, toys, and jewelry,” probably because they were in a big, uncapitalised list and thus looked fairly unimportant.
Overall our model has accomplished what we wanted to. Imagine we had a huge document full of hundreds of pages of text. This NLP model could quickly get you an overview of what the document is about and what the key entities in it are.
Operating on entities
Let’s try and do something a bit more applicable. Let’s say you have the same block of text as above, but you would like to remove the names of all people and organisations automatically, for privacy concerns. The spaCy library has a very useful scrub function which we can use to scrub away any entity categories we don’t want to see. Here’s what that would look like:
[PRIVATE] , doing business as [PRIVATE] , is an American electronic commerce and cloud computing company based in Seattle, Washington, that was founded by [PRIVATE] on July 5, 1994. The tech giant is the largest Internet retailer in the world as measured by revenue and market capitalization, and second largest after [PRIVATE] in terms of total sales. The [PRIVATE] website started as an online bookstore and later diversified to sell video downloads/streaming, MP3 downloads/streaming, audiobook downloads/streaming, software, video games, electronics, apparel, furniture, food, toys, and jewelry. The company also produces consumer electronics - Kindle e-readers, Fire tablets, [PRIVATE] , and Echo - and is the world's largest provider of cloud infrastructure services (IaaS and [PRIVATE] ). [PRIVATE] also sells certain low-end products under its in-house brand [PRIVATE].

That worked great! This is actually an incredibly powerful technique. People use the ctrl + f function on their computer all the time to find and replace words in their document. But with NLP, we can find and replace specific entities, taking into account their semantic meaning and not just their raw text.
Extracting information from text
The library the we installed previously textacy implements several common NLP information extraction algorithms on top of spaCy. It’ll let us do a few more advanced things than the simple out of the box stuff.
One of the algorithms it implements is called Semi-structured Statement Extraction. This algorithm essentially parses some of the information that spaCy’s NLP model was able to extract and based on that we can grab some more specific information about certain entities! In a nutshell, we can extract certain “facts” about the entity of our choice.
Let’s see what that looks like in code. For this one, we’re going to take the entire summary of Washington D.C’s Wikipedia page.

## Common Applications of NLP
### Text Matching
Article Recommendation Task: Given a trade commodity, find similar articles to be recommended to user Module used: word2vec
Name Standardization Task: Standardize DBS brand names from card generated free text information, as brand name free text may not be same for a particular merchant. How can we utilize string matching to find similar brands.  Module used: String similarity functions like Edit Distance, Greatest Common Prefix
Name Matching Task: Identify if particular customer (free text) is a DBS customer by doing fuzzy name matching/string matching against a list of names
Module used: regex_fuzzy_matching
Document similarity Given an article / document based on a product, find similar articles. 

### Supervised Learning

Text Classification Task: Classify if given email (sent to external email address) is suspicious Module used: bag of words, Tf-Idf, word clustering module
Task: Given a voice conversation transcript, classify conversation intent Module: 

### Unsupervised Learning
Topic Modelling Task: Identify latent topics from DBS articles/voice transcript data Module used: Latent Dirichlet Allocation (LDA), Non-Negative Matrix Factorization (NMF)
Text Summarization Task: Summarize long text into short sentence by capturing important words Module used: Gensim summarizer
Question Answering Building Chatbot based on customer and service agent conversations Module - seq2seq module

## Standard NLP Workflow
