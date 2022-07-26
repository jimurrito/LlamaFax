![Logo](https://pbs.twimg.com/profile_images/1550147959379021824/EE1vU4LG_400x400.jpg)

# LlamaFax
### Llama "Fact" Generation Engine
The LlamaFax engine uses machine learning to generate statments about Llamas.

## Overview
The LlamaFax engine is comprised of 4 base components.
- Ingress
- Lexor
- Render
- MongoDB

There is also an expanding list of complementary services.
- ScaleWeb
- Tweetbot**
- ManageWeb**
- Generation/Rating Engine***

**In developement  
***In Planning

All services are ran in independant docker containers

## Architecture

![High Level Design](https://github.com/jimurrito/LlamaFax/blob/main/assets/llamafax_highlevel.drawio.png?raw=true)

## In-depth Overview
### Core Services


### Ingress                                                     
The primary focus is pulling raw, or known, facts from the internet, and structuring them for further processing.
The main source used is API Ninjas, but I plan on expanding the list of sources as I scale out the engine.

A big part of this service is inserting the data into a dtcionary class object.
Statments are compared against the Archive Collection to ensure duplicate statments arent proccessed.
This object is inserted into the MongoDB Collection "Raw"; one of many that are used as a queue.


### Lexor
This focuses on understanding the sentence from a linguistical standpoint.
It uses a natural language processing tool called [NLTK](https://www.nltk.org/). 
This tool allows Lexor to process the "Raw" statments as follows:
 - Tokenizing | 
 Produces a similar effect to spiting the string into a list, by using the whitespaces. 
 - Tagging |
 Consumes the Tokenized string, and attaches a POS, or part of speech, type to each word.
 An example of this would be the word "Llama". During tagging, the tool should recognize this as a noun, and attach the approriate Abbreviation.
 In this case, it would be "NN" for a singular noun.
 - Chunking |
 Chunking takes the tagged words, and tries to find patterns in the statment, based on these parts of speech.
 It utilizes regex patterns for parsing. An example of this would be: __"NP: {<DT.?>*<JJ.?>*<VB.?>?<NN.?>+}"__. 
 This is actually the primary pattern I use for Llamafax at the time of writing this. Chunks parsed with this pattern are called Noun Phrases.
 
 The Process pulls raw facts from the Raw Queue. Statments are Tokenized, Tagged, and Chunked.
 Output is appended to a dictionary object that holds the orginal raw statment, and pushed to the Chunk Queue.


### Render
This compenent intakes the raw statments, and the Chunks, from the Chunk Queue. 
The service takes this message from the queue, and inserts Llama related Nouns (Llama(s)) into the statment, where parsed nouns are found.
This process generates all possible outcomes of replacing ONLY nouns found in nouns phrases. 

Once generated, any duplicate statments are pruned, using sets.
Generated statments are added to the previous set of data, and pushed to the Render queue.


### MongoDB (My Implementation)
I designed a class, "MongoDB", where the core concept is to streamline the use of MongoDB. The class creates an object that has the database connection string and assigned database collection. The base object is a [pymongo](https://pypi.org/project/pymongo/) object, and most of the methods are just simplier then the ones implemented into pymongo.

The best part of this implementation is the ability to easily use MongoDB Collections as Message Queues.
The subclass, Queue, creates a capped collection, with no configurable indexes. The major diffrence between the MongoDB class, and this subclass, is the Pull() Method. When declared using a Queue class, the message pulled from the Queue will be removed. Capped collections also have the benifit of following F.I.F.O. or "First in, First Out", which ensures messages are proccessed in the correct order.


### Core Service Considerations
#### Throttling
- The throughput of the services are throttled via a configurable message threshold variable. At the moment of writing, the threshold is 100 messages per queue.
- If raised, the throughput of services like Ingress, and Render, should increase. Lexor is likely already running as fast as possible for the thread assoicated to the scipt.
#### Horizontal Scaling
- A key reason for the choosen architecture, is to allow for horizatonal scaling. Each service is independant, and only needs access to its respective queues.
- Services like Lexor, are already running at near capacity for the thread allocated. So, increasing the number of nodes running that service, should allow the service to scale scale quickly.
- The throttling threshold for the queues should be raised in accordance with scaling. If not, the scaling will not be effective.


### [ScaleWeb](https://www.llamafax.com)
This compent is a web-interface, used to rate the generations within the Render Queue.
When a user signs in, they are greeted with a freshly pulled fact from Render Queue.
When the rating is input, the statments become rated with either "good" or "bad" tags.
This output is appended to the previous data set, and stored within the Archive Collection.


























