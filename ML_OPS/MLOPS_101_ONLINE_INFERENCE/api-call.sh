python access-via-keypair_cache.py \
  --account SFPSCOGS-SCS \
  --user ML_INFERENCE_SERVICE_USER \
  --role ML_INFERENCE_ROLE \
  --private_key_file_path ~/.snowflake/keys/rsa_key.p8 \
  --endpoint fdl4qlml-sfpscogs-scs.snowflakecomputing.app \
  --endpoint-path /predict \
  --snowflake_account_url https://SFPSCOGS-SCS.snowflakecomputing.com \
  --payload '{"data": [{"index": 0, "data": {"SIBSP": 1, "PARCH": 2, "FARE": 41.5792, "CLASS_SECOND": 1, "CLASS_THIRD": 0, "WHO_MAN": 0, "WHO_WOMAN": 1, "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 0}}]}'


python access-via-keypair.py \
  --account SFPSCOGS-SCS \
  --user CROMANO \
  --role sysadmin \
  --private_key_file_path ~/.snowflake/keys/rsa_key.p8 \
  --endpoint fdl4qlml-sfpscogs-scs.snowflakecomputing.app \
  --endpoint-path /predict-proba \
  --snowflake_account_url https://SFPSCOGS-SCS.snowflakecomputing.com \
  --payload '{"data": [{"index": 0, "data": {"SIBSP": 1, "PARCH": 2, "FARE": 41.5792, "CLASS_SECOND": 1, "CLASS_THIRD": 0, "WHO_MAN": 0, "WHO_WOMAN": 1, "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 0}}]}'


python access-via-keypair.py \
  --account SFPSCOGS-SCS \
  --user CROMANO \
  --role sysadmin \
  --private_key_file_path ~/.snowflake/keys/rsa_key.p8 \
  --endpoint fdl4qlml-sfpscogs-scs.snowflakecomputing.app \
  --endpoint-path /predict-proba \
  --snowflake_account_url https://SFPSCOGS-SCS.snowflakecomputing.com \
  --payload '{
    "data": [
      {
        "index": 0,
        "data": {
          "SIBSP": 1, "PARCH": 2, "FARE": 41.5792,
          "CLASS_SECOND": 1, "CLASS_THIRD": 0,
          "WHO_MAN": 0, "WHO_WOMAN": 1,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 0
        }
      },
      {
        "index": 1,
        "data": {
          "SIBSP": 0, "PARCH": 0, "FARE": 7.8958,
          "CLASS_SECOND": 0, "CLASS_THIRD": 1,
          "WHO_MAN": 1, "WHO_WOMAN": 0,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 1
        }
      },
      {
        "index": 2,
        "data": {
          "SIBSP": 1, "PARCH": 0, "FARE": 9.475,
          "CLASS_SECOND": 0, "CLASS_THIRD": 1,
          "WHO_MAN": 0, "WHO_WOMAN": 1,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 1
        }
      },
      {
        "index": 3,
        "data": {
          "SIBSP": 1, "PARCH": 0, "FARE": 53.1,
          "CLASS_SECOND": 0, "CLASS_THIRD": 0,
          "WHO_MAN": 0, "WHO_WOMAN": 1,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 1
        }
      },
      {
        "index": 4,
        "data": {
          "SIBSP": 0, "PARCH": 0, "FARE": 7.225,
          "CLASS_SECOND": 0, "CLASS_THIRD": 1,
          "WHO_MAN": 1, "WHO_WOMAN": 0,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 0
        }
      },
      {
        "index": 5,
        "data": {
          "SIBSP": 0, "PARCH": 1, "FARE": 16.1,
          "CLASS_SECOND": 0, "CLASS_THIRD": 1,
          "WHO_MAN": 1, "WHO_WOMAN": 0,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 1
        }
      },
      {
        "index": 6,
        "data": {
          "SIBSP": 1, "PARCH": 0, "FARE": 113.275,
          "CLASS_SECOND": 0, "CLASS_THIRD": 0,
          "WHO_MAN": 0, "WHO_WOMAN": 1,
          "EMBARK_TOWN_QUEENSTOWN": 0, "EMBARK_TOWN_SOUTHAMPTON": 0
        }
      }
    ]
  }'
