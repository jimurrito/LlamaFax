![Logo](https://pbs.twimg.com/profile_images/1550147959379021824/EE1vU4LG_400x400.jpg)

# LlamaFax
### Llama "Fact" Generation Engine
The LlamaFax engine uses machine learning to generate statements about Llamas.

## Overview
The LlamaFax engine is comprised of 4 base components.
- Ingress
- Lexor
- Render
- MongoDB

There is also an expanding list of complementary services.
- [ScaleWeb](https://github.com/jimurrito/LlamaFax_Web)
- Tweetbot
- [ManageWeb](https://github.com/jimurrito/LlamaFax_Management)
- Generation/Rating Engine**

**In development  
***In Planning

All services are ran in independent docker containers

## Architecture

![High Level Design](https://github.com/jimurrito/LlamaFax/blob/main/assets/llamafax_highlevel.drawio.png?raw=true)

## In-depth Overview
### Core Services


### Ingress                                                     
The primary focus is pulling raw, or known, facts from the internet, and structuring them for further processing.
The main source used is API Ninjas, but I plan on expanding the list of sources as I scale out the engine.

A big part of this service is inserting the data into a dictionary class object.
Statements are compared against the Archive Collection to ensure duplicate statements aren't processed.
This object is inserted into the MongoDB Collection "Raw"; one of many that are used as a queue.


### Lexor
This focuses on understanding the sentence from a linguistic standpoint.
It uses a natural language processing tool called [NLTK](https://www.nltk.org/). 
This tool allows Lexor to process the "Raw" statements as follows:
 - Tokenizing | 
 Produces a similar effect to spiting the string into a list, by using the whitespace. 
 - Tagging |
 Consumes the Tokenized string, and attaches a POS, or part of speech, type to each word.
 An example of this would be the word "Llama". During tagging, the tool should recognize this as a noun, and attach the appropriate Abbreviation.
 In this case, it would be "NN" for a singular noun.
 - Chunking |
 Chunking takes the tagged words, and tries to find patterns in the statement, based on these parts of speech.
 It utilizes regex patterns for parsing. An example of this would be: __"NP: {<DT.?>*<JJ.?>*<VB.?>?<NN.?>+}"__. 
 This is actually the primary pattern I use for Llamafax at the time of writing this. Chunks parsed with this pattern are called Noun Phrases.
 
 The Process pulls raw facts from the Raw Queue. Statements are Tokenized, Tagged, and Chunked.
 Output is appended to a dictionary object that holds the original raw statement, and pushed to the Chunk Queue.


### Render
This component intakes the raw statements, and the Chunks, from the Chunk Queue. 
The service takes this message from the queue, and inserts Llama related Nouns (Llama(s)) into the statement, where parsed nouns are found.
This process generates all possible outcomes of replacing ONLY nouns found in nouns phrases. 

Once generated, any duplicate statements are pruned, using sets.
Generated statements are added to the previous set of data, and pushed to the Render queue.


### MongoDB (My Implementation)
I designed a class, "MongoDB", where the core concept is to streamline the use of MongoDB. The class creates an object that has the database connection string and assigned database collection. The base object is a [pymongo](https://pypi.org/project/pymongo/) object, and most of the methods are just simpler then the ones implemented into pymongo.

The best part of this implementation is the ability to easily use MongoDB Collections as Message Queues.
The subclass, Queue, creates a capped collection, with no configurable indexes. The major difference between the MongoDB class, and this subclass, is the Pull() Method. When declared using a Queue class, the message pulled from the Queue will be removed. Capped collections also have the benefit of following F.I.F.O. or "First in, First Out", which ensures messages are processed in the correct order.


### Core Service Considerations
#### Throttling
- The throughput of the services are throttled via a configurable message threshold variable. At the moment of writing, the threshold is 100 messages per queue.
- If raised, the throughput of services like Ingress, and Render, should increase. Lexor is likely already running as fast as possible for the thread associated to the script.
#### Horizontal Scaling
- A key reason for the chosen architecture, is to allow for horizontal scaling. Each service is independent, and only needs access to its respective queues.
- Services like Lexor, are already running at near capacity for the thread allocated. So, increasing the number of nodes running that service, should allow the service to scale scale quickly.
- The throttling threshold for the queues should be raised in accordance with scaling. If not, the scaling will not be effective.


### [ScaleWeb](https://github.com/jimurrito/LlamaFax_Web)
This component is a web-interface, used to rate the generations within the Render Queue.
When a user signs in, they are greeted with a freshly pulled fact from Render Queue.
When the rating is input, the statements become rated with either "good" or "bad" tags.
This output is appended to the previous data set, and stored within the Archive Collection.

### [Management Interface](https://github.com/jimurrito/LlamaFax_Management)
This component is a web-interface that is used to get a single plane of glass look, into the LlamaFax Service. With this, we can get insights into the current status of the service Queues. Run Database Queries, and handle ticketing.

























