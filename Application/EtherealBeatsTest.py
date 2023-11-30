import os
import json
from web3 import Web3
from bitarray import bitarray
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv("EtherealBeats.env")


st.title('Ethereal Beats Music Portal')

############## Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# @st.cache(allow_output_mutation=True) # This method has been deprecated and therefore commented out
def load_contract():

    # Load the contract ABI
    with open(Path('FinalMusicNFTV2.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

######## Load the contract
contract = load_contract()



# Sidebar Menu
st.sidebar.title("Ethereal Beats")
pages = ["Mint NFT", "My Inventory", "Royalties"]
page = st.sidebar.selectbox("Choose page", pages)



######### Mint music NFT
accounts = w3.eth.accounts
user = st.selectbox("Select Account", accounts)

selected_file = st.file_uploader("Choose file", type=['mp3', 'wav', 'm4a'])

if st.button("Mint NFT"):
    ipfs_cid = pin_file_to_ipfs(selected_file)
    tx = contract.functions.mint(ipfs_cid).transact({"from": user})
    st.write("Minted!")



# Display My Music

if st.button("Display Music"):
    token_uri = contract.functions.tokenId().call()
    #for token_id in tokens:
     #   token_uri = contract.functions.tokenURI(token_id).call()
    st.audio(f"https://ipfs.io/ipfs/{token_uri}")

#token_id = st.selectbox('Choose Token', tokens) 

# Set Rules
recipient = st.text_input('Reciepient Address')
access_rules = st.radio('Permissions', ['PLAY', 'REMIX', 'DOWNLOAD'])

def build_bitflags(flags):
   bits = bitarray(flags) 
   return bits.to01()

if st.button('Set Rules'):
    bytes_rule = build_bitflags(access_rules) 
    tx = contract.setAccessRules(token_id, recipient, bytes_rule)
    
    
# Check Permission 
check_address = st.text_input('Address')  
permission = st.radio('Permission', ['PLAY', 'REMIX', 'DOWNLOAD'])

if st.button('Check Access'):
    has_permission = contract.checkAccess(
         token_id, check_address, permission
    )
    
    st.write(has_permission)

#token_id = st.selectbox('Choose Token', my_tokens)

@st.cache
def permission_list(bitmask):
    permissions = []
    
    if (bitmask & 1) != 0:
       permissions.append("PLAY")
       
    if (bitmask & 2) != 0:
       permissions.append("DOWNLOAD")
       
    if (bitmask & 4) != 0:
       permissions.append("REMIX")
       
    return permissions

if st.button('Fetch Access Rules'):
    # Owner can view all rules
    rules = contract.getAccessPermissions(token_id) 
    st.write(f"There are {len(rules)} rules configured")
    
    for rule in rules:

       st.write(f"""
           Address: {rule.account}
           Permissions: {permission_list(rule.permissions)} 
       """)


## Pay Royalties Form (Smart Contract - Pay Royalties Function)
#token_id = st.selectbox('Choose NFT', my_nft_ids)
amount = st.number_input('Enter royalty amount')

if st.button('Pay Royalties'):
     tx = contract.functions.payRoyalties(
           token_id
        ).transact({"value": amount})


## Distribute Secondary Royalties  (Smart Contract - Distrubte Royalties Function)
@st.cache
def get_last_sale(token_id):

   # Fetch last Transfer event 
   sale_event = get_transfer_event(token_id)
   
   return sale_event['args']['price']

#sale_event = get_last_sale(token_id)
#sale_price = sale_event['price']

#if st.button('Distribute Royalties'):
     #tx = contract.functions.distributeRoyalties(
          # token_id, sale_price  
       # ).transact()


st.balloons()





















# ################################################################################
# # Helper functions to pin files and json to Pinata
# ################################################################################


# def pin_artwork(artwork_name, artwork_file):
#     # Pin the file to IPFS with Pinata
#     ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

#     # Build a token metadata file for the artwork
#     token_json = {
#         "name": artwork_name,
#         "image": ipfs_file_hash
#     }
#     json_data = convert_data_to_json(token_json)

#     # Pin the json to IPFS with Pinata
#     json_ipfs_hash = pin_json_to_ipfs(json_data)

#     return json_ipfs_hash, token_json


# def pin_appraisal_report(report_content):
#     json_report = convert_data_to_json(report_content)
#     report_ipfs_hash = pin_json_to_ipfs(json_report)
#     return report_ipfs_hash


# st.title("Art Registry Appraisal System")
# st.write("Choose an account to get started")
# accounts = w3.eth.accounts
# address = st.selectbox("Select Account", options=accounts)
# st.markdown("---")

# ################################################################################
# # Register New Artwork
# ################################################################################
# st.markdown("## Register New Artwork")
# artwork_name = st.text_input("Enter the name of the artwork")
# artist_name = st.text_input("Enter the artist name")
# initial_appraisal_value = st.text_input("Enter the initial appraisal amount")

# # Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
# file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

# if st.button("Register Artwork"):
#     # Use the `pin_artwork` helper function to pin the file to IPFS
#     artwork_ipfs_hash, token_json = pin_artwork(artwork_name, file)

#     artwork_uri = f"ipfs://{artwork_ipfs_hash}"

#     tx_hash = contract.functions.registerArtwork(
#         address,
#         artwork_name,
#         artist_name,
#         int(initial_appraisal_value),
#         artwork_uri,
#         token_json['image']
#     ).transact({'from': address, 'gas': 1000000})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write("Transaction receipt mined:")
#     st.write(dict(receipt))
#     st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
#     st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
#     st.markdown(f"[Artwork IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

# st.markdown("---")


# ################################################################################
# # Appraise Art
# ################################################################################
# st.markdown("## Appraise Artwork")
# tokens = contract.functions.totalSupply().call()
# token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
# new_appraisal_value = st.text_input("Enter the new appraisal amount")
# appraisal_report_content = st.text_area("Enter details for the Appraisal Report")

# if st.button("Appraise Artwork"):

#     # Make a call to the contract to get the image uri
#     image_uri = str(contract.functions.imageUri(token_id).call())
    
#     # Use Pinata to pin an appraisal report for the report content
#     appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content+image_uri)

#     # Copy and save the URI to this report for later use as the smart contract’s `reportURI` parameter.
#     report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

#     tx_hash = contract.functions.newAppraisal(
#         token_id,
#         int(new_appraisal_value),
#         report_uri,
#         image_uri

#     ).transact({"from": w3.eth.accounts[0]})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write(receipt)
# st.markdown("---")

# ################################################################################
# # Get Appraisals
# ################################################################################
# st.markdown("## Get the appraisal report history")
# art_token_id = st.number_input("Artwork ID", value=0, step=1)
# if st.button("Get Appraisal Reports"):
#     appraisal_filter = contract.events.Appraisal.createFilter(
#         fromBlock=0, argument_filters={"tokenId": art_token_id}
#     )
#     reports = appraisal_filter.get_all_entries()
#     if reports:
#         for report in reports:
#             report_dictionary = dict(report)
#             st.markdown("### Appraisal Report Event Log")
#             st.write(report_dictionary)
#             st.markdown("### Pinata IPFS Report URI")
#             report_uri = report_dictionary["args"]["reportURI"]
#             report_ipfs_hash = report_uri[7:]
#             image_uri = report_dictionary["args"]["artJson"]
#             st.markdown(
#                 f"The report is located at the following URI: "
#                 f"{report_uri}"
#             )
#             st.write("You can also view the report URI with the following ipfs gateway link")
#             st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
#             st.markdown("### Appraisal Event Details")
#             st.write(report_dictionary["args"])
#             st.image(f'https://ipfs.io/ipfs/{image_uri}')
#     else:
#         st.write("This artwork has no new appraisals")




