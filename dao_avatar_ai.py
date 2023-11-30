# # ***DAO Membership Program***

# **DAO Member Avatar: Using Python 'Replicate' Library for Machine Learning, AI-Generated Dao Member Avatars, Associated with Unique MIDs. DAO Memberships to be distributed as NFTs (DAOs may be governed using NFTs or tokens that grant members voting rights. The rules of the DAO are stored on an open-sourced blockchain.**

# DAO == Decentralized autonomous organization

# MID == Member Identifier

# While beyond the scope of this initial DAO project, we could store the resulting DAO Member Avatars and other such data off blockchain through an IPFS, or inter-planetary file system, such as Pinata, where data would be stored through a cryptographic hash, returning a unique CID, or content identifier.  The CID would serve as both the address and verification of the data.

# "IPFS is a peer-to-peer distributed file system that is used primarily for data that can't be stored on a blockchain." (c.f. https://docs.pinata.cloud/docs/what-is-ipfs)

# References:
# - https://ethereum.org/en/dao/
# - https://docs.pinata.cloud/docs/what-is-ipfs
# - https://www.binance.com/en/blog/nft/what-is-a-dao-and-how-does-it-benefit-nfts-421499824684903992

# # Install replicate Python client and other required packages for Google Colab IDE
# !pip install python-dotenv
# !pip install replicate
# !pip install streamlit
# !pip install web3==5.17 #Creating dependency issue with jsonschema?
# !pip install web3
# !pip install eth-tester==0.5.0b3
# !pip install mnemonic
# !pip install bip44

# Import required libraries
import os  # Methods for interacting with the operating system, including management of environment variables
from dotenv import load_dotenv  # Method for loading local environment file
import replicate  # Replicate library for AI-generated Avatar and other machine learning applications
import streamlit as st  # Streamlit front-end web browser UI
from web3 import Web3

#!jsonschema --version # Google Colab appears to be requiring jsonschema 3.2.0, while our local dev environment uses 4.19.1.

# Create local blockchain Ganache connection
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

# # Load .env file, containing Replicate API Token, locally to Google Colab Jupyter Notebook
# from google.colab import files
# uploaded = files.upload()

# # Load local environment .env file for secure api reference
# load_dotenv() # Returns True

# REPLICATE LIBRARY MACHINE LEARNING, AI-GENERATING AVATAR IMPLEMENTATION #
# About the Replicate library we are using for our Dao's AI-generated avatars, with potential for other machine learning applications

# Replicate documentation: https://replicate.com/docs

# About Replicate:  1. https://replicate.com/about
#                   2. https://replicate.com/blog/machine-learning-needs-better-tools:

# "Replicate runs machine learning models in the cloud. We have a library of open-source models that you can run with a few lines of code.
# If you're building your own machine learning models, Replicate makes it easy to deploy them at scale.""

# "There are roughly two orders of magnitude more software engineers than there are machine learning engineers (~30 million vs. ~500,000).
# By building good tools, we think it is possible for software engineers to use machine learning in the same way they can use normal software."

# "If you try to actually build something with these machine learning models, you find that none of it really works. You spend all day battling
# with messy Python scripts, broken Colab notebooks, perplexing CUDA errors, misshapen tensors. It’s a mess."

# "Normal software used to be like this. If you wanted to build a website 20 years ago it felt like trying to use machine learning today.
# You had to build web servers, authentication systems, user interface components. You were concatenating HTML and SQL by hand, hoping you didn’t
# get owned. To deploy, you uploaded files to an FTP server and waited and hoped for the best."

# "The reason machine learning is so hard to use is not because it’s inherently hard. We just don’t have good tools and abstractions yet. You
# shouldn’t have to understand GPUs to use machine learning, in the same way you don’t have to understand TCP/IP to build a website."

# Initiate Streamlit setup code

# Streamlit main body headers:
st.markdown("# DAO Member Application")
st.markdown("## Generate your customized Membership Avatar")
st.text(" \n")
# Input area for DAO Member applicant's first name:
first_name = st.text_input("Please enter the DAO member applicant's first name. No funny business!")
# Input area for DAO Member applicant's last name:
last_name = st.text_input("Please enter the DAO member applicant's last name")
# Input area for DAO Member applicant's desired custom avatar image:
avatar_text_input_prompt = st.text_input("Please describe the super-special, unique membership Avatar that you desire. The sky's the limit!")
if avatar_text_input_prompt == 'portrait of the ideal woman':
    avatar_text_input_prompt = 'marge simpson from the simpsons'    

# Streamlit sidebar headers:
st.sidebar.markdown("## Alternatively, rather than describing your Avatar, you may individually customize your Avatar's features using the drop-down list boxes below:")
shape = ['round', 'square', 'narrow']
eye_color = ['brown', 'green', 'blue']
hair_color = ['red', 'brown', 'black', 'brown']
hair_style = ['long', 'short', 'mullet', 'perm']
eyebrow_type = ['bushy', 'thin', 'unibrow']
facial_hair_type = ['no facial hair', 'beard', 'mustache', 'goatee']
avatar_shape = st.sidebar.selectbox("Select a face shape", shape)
avatar_eye_color = st.sidebar.selectbox("Select an eye color", eye_color)
avatar_hair_color = st.sidebar.selectbox("Select a hair color", hair_color)
avatar_hair_style = st.sidebar.selectbox("Select a hair style", hair_style)
avatar_eyebrow_type = st.sidebar.selectbox("Select an eyebrow type", eyebrow_type)
avatar_facial_hair_type = st.sidebar.selectbox("Select facial hair type", facial_hair_type)

# Import replicate

# Save replicate api token to local environment for Colab or VS Code IDE
# REPLICATE_API_KEY = os.getenv('REPLICATE_API_TOKEN') # Unable to resolve local .env file reference
REPLICATE_API_KEY = "r8_MWmqhtJpG7hERByS1WDYAh2Ap4wimPb1o7svr"
# print(REPLICATE_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

# Create and run a model instance
# You can run any public model on Replicate from Python code. The following runs stability-ai/stable-diffusion, a latent text-to-image diffusion model capable of generating
# photo-realistic images given any text input:
# avatar_text_input_prompt = "an astronaut on mars holding flowers, impressionism"

if first_name != "" and last_name != "":
    st.write(f"Welcome {first_name} {last_name}, please describe your Avatar above and then use the button below to generate your unique Avatar")

if st.button("Generate my Avatar") or st.sidebar.button('Use my profile to generate my Avatar'):
    with st.spinner('Generating your Avatar, please wait...'):
        avatar_model_predicted = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={"prompt": avatar_text_input_prompt},
        )

        # Files are output as a URL, such as https://replicate.delivery/pbxt/YmvilcU8As4uMxBeNoYMg0rrOMmt2Kn6hqqeXr5RKfUx6F6jA/out-0.png,
        # reflecting our input prompt 'astronaut on mars holding flowers, impressionism'
        st.write(f"Your avatar is ready to be viewed here: {avatar_model_predicted}")
        st.image(avatar_model_predicted, caption='Your auto-magical custom Avatar', width=300)
    st.success('Done! You will be issued an avatar image certificate as an NFT! Hope you like it!')
    st.success('Thank you for your membership, in posterity!')
    st.snow()   