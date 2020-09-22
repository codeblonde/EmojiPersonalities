Research Project:
# Me, Myself & my Emojis: Do the Emojis We Use Reflect Who We Are?
## An Experimental Investigation of the Relation between Personality Type and Emoji Use in Instagram Posts
by Jana Germies Department of Linguistics, Ruhr-Universität Bochum, Germany

### Abstract
Human personalities are rather complex and made up of many fine facets, yet finding ways to predict these has gained much popularity within psychology and computational linguistics. Whereas much of the research has relied on cues within written text, such as linguistic style, gathered from clinical patients or social media platforms, present research wants to take a timelier approach and look closer at the usage of emojis, which have taken modern communication by storm and may hold great representative value. To this end, a controlled group of test subject was chosen and correlations between the big five traits and emojis found within their posts on a popular social media platform were investigated and in a second step added to a classification model. Further, the discrimniatory power of the images accompanying said posts were studied and a range of feature sets compared. Findings revealed some unique patterns for the test group and a positive effect on classification incorporating the additional features and especially the emojis. 


## Project
Current project is the practical implementation of the research project mentioned above.
It includes the script used to scrape the social media data, as well as all the code for processing the posts, computing correlations between emojis and personality types, and a scaffold of the model used for classification. 


## Requirements
Requirements can be taken from the requirements.txt file and mainly include:

'''bash
advertools==0.10.6
emoji==0.5.4
emojis==0.5.1
scikit-learn==0.23.1
scipy==1.4.1
sklearn==0.0
flair==0.6
tensorflow==2.3.0
Keras==2.4.3
'''

## Setting up a virtual environment
All code was executed within a controlled virtual envirnment, using python's native venv.

1. To set up your environment on a Linux machine use the following command or use other configurations:
'''bash
$python3 -m venv /path/to/venv/personality-venv
'''

2. activate the venv:
'''bash
$source personality-venv/bin/activate
'''

3. install requirements:
'''bash
pip3 install requirements.txt
'''

4. to exit the venv use:
'''bash
$deactivate
'''

Most scripts can be executed in the environment as well as from the shell (on Linux), once the the venv has been created.

## Data
The data provided includes gathered social media captions plus LIWC personality scores for each user within the dataset.
The image data will not be made available.
Further all data has been anonymized.

### Embedding models
The pre-trained Emoji Embedding Model (Emoji2Vec) can be downloaded from here:
https://github.com/uclnlp/emoji2vec/tree/master/pre-trained

## Correlations
Correlations between emojis and personality traits or among the traits can be computed directly using correlation_main.py
It encompasses all preprocessing steps and outputs summary dataframes as well as a heatmap of the correlations.


## Classification
For classification, first a dataset comprising of preprocessed embeddings must be created and saved using classifier_helper/create_dataset.py. Depending on your computational resources, this might take a few moments.
Next, the newly created dataset can be loaded and used for training in classification_main.py.


## Run from terminal (Linux)
Make sure to make the file executable using:
'''bash
sudo chmod +x file.py
'''

then execute file by running:
'''bash
./file.py
'''