# Online Inference with Snowpark Container Services

This repo is an example of how to create a real time inference endpoint for an ML model using Snowpark Container Services. 

When running the notebook in your Snowflake account, be sure to add the `titanic_snowflake.csv` to your notebook environment. 

Run the notebook to train a model, register it in Snowflake Model Registry, and create an inference service for that model that runs on SPCS. 

## Inference from Local Machine
Once you've run the notebook, you can test out online inference from you local machine. Expect sub-second latency from your inference endpoint.

### Prerequisites
To set up, make sure you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/)

### Setup
Run the following commands
```
chmod +x create-keys.sh 
sh create-keys.sh
```
This will create a public and private key pair on your local machine. 

Next, you'll need to associate your Snowflake user with your public key. Open up your public key (ending in .pub, likely located at ~/.snowflake/keys). Select the text before and after the long dashes, and run the command below in your Snowflake account.
```
ALTER USER <YOUR_USER> SET RSA_PUBLIC_KEY = 'MI...'
```

Next, we'll create a virtual environment from which to run the python request code. Run the following in your terminal.
```
uv init
uv sync
source .venv/bin/activate
uv add requests pyJWT cryptography
```

### Running inference
Make sure your inference endpoint is live. Then, open up `api-call.sh`. Change the account, user, role, endpoint, and snowflake account url on the first command. You can find your inference endpoint url by running the `mv.list_services()` cell in the notebook.

If you are wanting to use a service account which is much more real world please use service_account_setup.sql to create the service account to hit the API.

Copy and paste the edited first command into your terminal (lines 1-9), and you should get a response back!
```
Response: {"data":[[0,{"output_feature_0":1}]]}
```

## Running inference from Postman
To run in Postman, run the `jwt_to_oauth.py` file. Something like the following
```
python jwt_to_oauth.py \
  --account <account> \
  --user <user> \
  --private_key_file_path ~/.snowflake/keys/rsa_key.p8 \
  --endpoint <container endpoint>
```
This will output an OAuth token. Put this into a header in Postman with the key `Authorization` and the value `Snowflake Token="ey..."`. 

Make sure you have `Content-Type` set to `application/json` and `Content-Length` enabled. Paste in the request body from the `api-call.sh` python examples as raw JSON body. 

Set the url to your container endpoint url and make sure the method is POST. Don't forget to add https:// and /predict at the end. 

Send the request and you should see a response!
```
Response: {"data":[[0,{"output_feature_0":1}]]}
```
