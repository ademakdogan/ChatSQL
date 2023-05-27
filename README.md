

<div style="display: flex; align-items: center;">
  <img src="images/logo.png" alt="Logo" width="120" height="120">
  <h1 style="margin-left: 20px;">ChatSQL</h1>
</div>




The plain text that it is given by the user is converted to mysql queries using ChatGPT in this project. 
We need to specify some information about our database from the beginning in order for Chatgpt to understand our database. The [info.json](info.json) file can be used for this process. The database information should be added in this file in detail. As the complexity of your database increases, you should provide more detailed information. After a certain level of complexity, this data must be kept by vectorization and autonomously extracting the specific information structure for each incoming prompt. This method will be more effective and more economical. For this reason, this project is more suitable for mid-small databases. If I have enough time in the future, I will do new project about large database. 

Openai api key and database informations should be added to the [conf.json](conf.json) file. You want to try the project, but you may not have a sample data set. You can use the [books.csv](data/books.csv) file for testing. 

All packages are installed before starting.  The following command is used for this installation process (python 3.8 is used in this project):

## Installation of Package
```
  make install
```
or

```
pip3 install --default-timeout=900 -r requirements.txt
```

## Data Insertion into Databse
Run [sample_data_creator.py](src/sample_data_creator.py) to insert the sample dataset into your own database. You can use following commands (default table name is "bt").

```
python3 sample_data_creator.py
```
## Usage

Now that our data is ready, so we can start using it. 
There are two different usage methods. The first of these is to run the [chatsql.py](src/chatsql.py) file. In this method, prompt is added as flag. In the second method, it is used via grpc server.

### 1- ChatSql

A sample of the database can be viewed below.

 ```
+-----+--------------------------------------------------------+------------------------+-------------------+--------+------------------+
| ID  | Title                                                  | Author                 | Genre             | Height | Publisher        |
+-----+--------------------------------------------------------+------------------------+-------------------+--------+------------------+
|   1 | Fundamentals of Wavelets                               | Goswami, Jaideva       | signal_processing |    228 | Wiley            |
|   2 | Data Smart                                             | Foreman, John          | data_science      |    235 | Wiley            |
|   3 | God Created the Integers                               | Hawking, Stephen       | mathematics       |    197 | Penguin          |
|   4 | Superfreakonomics                                      | Dubner, Stephen        | economics         |    179 | HarperCollins    |
|   5 | Orientalism                                            | Said, Edward           | history           |    197 | Penguin          |
|   6 | Nature of Statistical Learning Theory, The             | Vapnik, Vladimir       | data_science      |    230 | Springer         |
|   7 | Integration of the Indian States                       | Menon, V P             | history           |    217 | Orient Blackswan |
|   8 | Drunkard's Walk, The                                   | Mlodinow, Leonard      | science           |    197 | Penguin          |
|   9 | Image Processing & Mathematical Morphology             | Shih, Frank            | signal_processing |    241 | CRC              |
|  10 | How to Think Like Sherlock Holmes                      | Konnikova, Maria       | psychology        |    240 | Penguin          |
|  11 | Data Scientists at Work                                | Sebastian Gutierrez    | data_science      |    230 | Apress           |
|  12 | Slaughterhouse Five                                    | Vonnegut, Kurt         | fiction           |    198 | Random House     |
|  13 | Birth of a Theorem                                     | Villani, Cedric        | mathematics       |    234 | Bodley Head      |
|  14 | Structure & Interpretation of Computer Programs        | Sussman, Gerald        | computer_science  |    240 | MIT Press        |
|  15 | Age of Wrath, The                                      | Eraly, Abraham         | history           |    238 | Penguin          |
|  16 | Trial, The                                             | Kafka, Frank           | fiction           |    198 | Random House     |
|  17 | Statistical Decision Theory'                           | Pratt, John            | data_science      |    236 | MIT Press        |
|  18 | Data Mining Handbook                                   | Nisbet, Robert         | data_science      |    242 | Apress           |
|  19 | New Machiavelli, The                                   | Wells, H. G.           | fiction           |    180 | Penguin          |
|  20 | Physics & Philosophy                                   | Heisenberg, Werner     | science           |    197 | Penguin          |
|  21 | Making Software                                        | Oram, Andy             | computer_science  |    232 | O'Reilly         |
|  .  | .......                                                | .......                | ....              |    ... | ....             |
|  .  | .......                                                | .......                | ....              |    ... | ....             |
```

Here's our sample prompt : "Show me the book type fiction which they height bigger than 175 and smaller than 178. The author shoudn't be 'Doyle, Arthur Conan'."  
So the usage is:  

```
python3 chatsql.py -p 'Show me the book type fiction which they height bigger than 175 and smaller than 178. The author shouldn't be 'Doyle, Arthur Conan'. '
```
Result:
```
CHATGPT QUERY------------------:
SELECT * FROM bt WHERE Genre = 'Fiction' AND Height > 175 AND Height < 178 AND Author != 'Doyle, Arthur Conan'
RAW RESULT------------------:
[(32, 'Pillars of the Earth, The', 'Follett, Ken', 'fiction', 176, 'Random House'), (37, 'Veteran, The', 'Forsyth, Frederick', 'fiction', 177, 'Transworld'), (38, 'False Impressions', 'Archer, Jeffery', 'fiction', 177, 'Pan'), (72, 'Prisoner of Birth, A', 'Archer, Jeffery', 'fiction', 176, 'Pan'), (87, 'City of Joy, The', 'Lapierre, Dominique', 'fiction', 177, 'vikas'), (128, 'Rosy is My Relative', 'Durrell, Gerald', 'fiction', 176, 'nan')]
PROCESSED RESULT------------------ :
The books 'Pillars of the Earth, The' by Ken Follett, 'Veteran, The' by Frederick Forsyth, 'False Impressions' by Jeffery Archer, 'Prisoner of Birth, A' by Jeffery Archer, 'City of Joy, The' by Dominique Lapierre, and 'Rosy is My Relative' by Gerald Durrell are all fiction books with 176 or 177 pages published by Random House, Transworld, Pan, Vikas, and Nan, respectively.
```

As can be seen above, three different output results are obtained. The first result is the translation of the given prompt into a sql query. Raw result is the raw data returned from the database as a result of this query. Finally, processed data is the interpretation of the sql results as plain text by chatgpt.

### 2- Using via gRPC

gRPC server: 
```
python3 main.py -p 9001
```
After running the gRPC server, you can connect to this server with your own client and send a prompt. If you want to see an example, you can look at the [client.py](src/client.py) file.

```
python3 client.py
```
Result:
```
{'query': "SELECT * from bt WHERE Genre = 'Fiction' AND Height > 175 AND Height < 178 AND Author != 'Doyle, Arthur Conan'", 'raw_result': "[(32, 'Pillars of the Earth, The', 'Follett, Ken', 'fiction', 176, 'Random House'), (37, 'Veteran, The', 'Forsyth, Frederick', 'fiction', 177, 'Transworld'), (38, 'False Impressions', 'Archer, Jeffery', 'fiction', 177, 'Pan'), (72, 'Prisoner of Birth, A', 'Archer, Jeffery', 'fiction', 176, 'Pan'), (87, 'City of Joy, The', 'Lapierre, Dominique', 'fiction', 177, 'vikas'), (128, 'Rosy is My Relative', 'Durrell, Gerald', 'fiction', 176, 'nan')]", 'processed_result': "\n1. Ken Follett's 'Pillars of the Earth, The' is a fiction novel with 176 pages that was published by Random House.\n2. Frederick Forsyth's 'Veteran, The' is a fiction novel with 177 pages that was published by Transworld.\n3. Jeffery Archer's 'False Impressions' is a fiction novel with 177 pages that was published by Pan.\n4. Jeffery Archer's 'Prisoner of Birth, A' is a fiction novel with 176 pages that was published by Pan.\n5. Dominique Lapierre's 'City of Joy, The' is a fiction novel with 177 pages that was published by Vikas.\n6. Gerald Durrell's 'Rosy is My Relative' is a fiction novel with 176 pages that was published by Nan."}
Time: 10.407907724380493
```

### 3- Using via Docker - gRPC

If you want to create gRPC server via docker (default image name --> chatsql):
Install 
```
make docker
``` 
Usage:
``` 
make docker_run p=9001
```  
After that use your client: 
```
python3 client.py
```
and result: 
```
'query': "SELECT * FROM bt WHERE Genre = 'Fiction' AND Height > 175 AND Height < 178 AND Author != 'Doyle, Arthur Conan'", 'raw_result': "[(32, 'Pillars of the Earth, The', 'Follett, Ken', 'fiction', 176, 'Random House'), (37, 'Veteran, The', 'Forsyth, Frederick', 'fiction', 177, 'Transworld'), (38, 'False Impressions', 'Archer, Jeffery', 'fiction', 177, 'Pan'), (72, 'Prisoner of Birth, A', 'Archer, Jeffery', 'fiction', 176, 'Pan'), (87, 'City of Joy, The', 'Lapierre, Dominique', 'fiction', 177, 'vikas'), (128, 'Rosy is My Relative', 'Durrell, Gerald', 'fiction', 176, 'nan')]", 'processed_result': '\nThe books "Pillars of the Earth, The" by Ken Follet, "Veteran, The" by Frederick Forsyth, "False Impressions" by Jeffery Archer, "Prisoner of Birth, A" by Jeffery Archer, "City of Joy, The" by Dominique Lapierre and "Rosy is My Relative" by Gerald Durrell are all fiction books with page count 176 or 177 and published by Random House, Transworld, Pan, Vikas or Nan.'}
Time: 7.1615989208221436
```
Be careful !! -> If you want to use docker, you should configure network in docker. For example, if you are using a mac device and connecting to your mysql database via localhost, you should set **"host.docker.internal"** instead of **"localhost"** (in [conf.json](conf.json) file - **"HOST": "host.docker.internal"**) for docker.



### Extra Info

In the examples so far, the column names in the database were always meaningful. ChatGPT can generate queries by understanding the column names. However, in some cases, column names are meaningless or chatgpt may not understand them. If we add enough detailed information about the database to the [info.json](info.json) file, we will continue to get the results we want. For example, let's change the column names to be aa, bb, cc, dd, ee. 

```
+-----+--------------------------------------------------------+------------------------+-------------------+------+------------------+
| ID  | aa                                                     | bb                     | cc                | dd   | ee               |
+-----+--------------------------------------------------------+------------------------+-------------------+------+------------------+
|   1 | Fundamentals of Wavelets                               | Goswami, Jaideva       | signal_processing |  228 | Wiley            |
|   2 | Data Smart                                             | Foreman, John          | data_science      |  235 | Wiley            |
|   3 | God Created the Integers                               | Hawking, Stephen       | mathematics       |  197 | Penguin          |
|   4 | Superfreakonomics                                      | Dubner, Stephen        | economics         |  179 | HarperCollins    |
|   5 | Orientalism                                            | Said, Edward           | history           |  197 | Penguin          |
|  .  | .......                                                | .......                | ....              |    ... | ....           |
|  .  | .......                                                | .......                | ....              |    ... | ....           |
```

If we explain the column names in detail and run the client.py -->
```
{'query': "SELECT aa, bb, cc, dd FROM bt WHERE cc = 'fiction' AND dd > 175 AND dd < 178 AND bb != 'Doyle, Arthur Conan'", 'raw_result': "[('Pillars of the Earth, The', 'Follett, Ken', 'fiction', 176), ('Veteran, The', 'Forsyth, Frederick', 'fiction', 177), ('False Impressions', 'Archer, Jeffery', 'fiction', 177), ('Prisoner of Birth, A', 'Archer, Jeffery', 'fiction', 176), ('City of Joy, The', 'Lapierre, Dominique', 'fiction', 177), ('Rosy is My Relative', 'Durrell, Gerald', 'fiction', 176)]", 'processed_result': '\nThe books "Pillars of the Earth, The" by Ken Follett, "Veteran, The" by Frederick Forsyth, "False Impressions" by Jeffery Archer, "Prisoner of Birth, A" by Jeffery Archer, "City of Joy, The" by Dominique Lapierre and "Rosy is My Relative" by Gerald Durrell are all fiction and have page lengths of 176 or 177.'}
```

The next project could be on generating queries (mongo, sql) from prompts with free models (Llama).
