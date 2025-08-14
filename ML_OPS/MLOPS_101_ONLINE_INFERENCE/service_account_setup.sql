/*
If you would like to use a service account to hit the end point
the following script walks you through how to create the service account
and add the required privileges 
 */

use role accountadmin;

use database CROMANO;
use schema DEMO;
SET database_name = 'CROMANO';  -- Replace with your database name
SET schema_name = 'DEMO';       -- Replace with your schema name
SET db_schema = 'CROMANO.DEMO'; -- Combined for easier reference


CREATE ROLE IF NOT EXISTS ML_INFERENCE_ROLE
    COMMENT = 'Role for ML inference service account with minimal required permissions';

CREATE USER IF NOT EXISTS ML_INFERENCE_SERVICE_USER
    DISPLAY_NAME = 'ML Inference Service Account'
    COMMENT = 'Service account for calling ML inference endpoints'
    -- Password is not set - will use keypair authentication only
    MUST_CHANGE_PASSWORD = FALSE
    DEFAULT_WAREHOUSE = 'COMPUTE_WH'  -- Adjust as needed
    DEFAULT_ROLE = 'ML_INFERENCE_ROLE';

GRANT USAGE ON DATABASE IDENTIFIER($database_name) TO ROLE ML_INFERENCE_ROLE;
GRANT USAGE ON SCHEMA IDENTIFIER($db_schema) TO ROLE ML_INFERENCE_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA IDENTIFIER($db_schema) TO ROLE ML_INFERENCE_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA IDENTIFIER($db_schema) TO ROLE ML_INFERENCE_ROLE;

GRANT READ ON MODEL TITANIC_SERVICE TO ROLE ML_INFERENCE_ROLE;

GRANT USAGE, MONITOR ON COMPUTE POOL titanic_compute_pool TO ROLE ML_INFERENCE_ROLE;

GRANT USAGE ON SERVICE TITANIC_PREDICTION_SERVICE TO ROLE ML_INFERENCE_ROLE;

GRANT SERVICE ROLE TITANIC_PREDICTION_SERVICE!all_endpoints_usage TO ROLE ML_INFERENCE_ROLE;

GRANT READ ON IMAGE REPOSITORY tutorial_repository TO ROLE ML_INFERENCE_ROLE;

GRANT ROLE ML_INFERENCE_ROLE TO USER ML_INFERENCE_SERVICE_USER;


ALTER USER ML_INFERENCE_ROLE SET RSA_PUBLIC_KEY='<Enter Your Public Key>';