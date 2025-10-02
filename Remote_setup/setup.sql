-- For this demo we have a database called adminstration and schema public to store account level rules
use role accountadmin;

-- Need Bind Service Endpoint to sysadmin so sysadmin can access service endpoints
GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE sysadmin;

-- Create network rule for external access
CREATE NETWORK RULE administration.public.allow_all_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('0.0.0.0:443', '0.0.0.0:80');

-- Create external access integration
CREATE EXTERNAL ACCESS INTEGRATION ALLOW_ALL_INTEGRATION
ALLOWED_NETWORK_RULES = (allow_all_rule)
ENABLED = true;

grant usage on INTEGRATION ALLOW_ALL_INTEGRATION to role sysadmin;

use role accountadmin;

-- create the dedicated compute pool for the remote setup
CREATE COMPUTE POOL remote_pool
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;

  grant usage on compute pool remote_pool to role sysadmin;

  use role sysadmin;

CREATE STAGE ADMINISTRATION.PUBLIC.REMOTE
ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE' );


/*
  Now open a terminal and run the following command to connect to the remote setup
If you do not have uv run 'brew install uv' uv is not required but recommended
cd Remote_setup
brew install websocat
uv sync
source .venv/bin/activate
snow connection list
# You can edit your connection cursor ~/.snowflake/config.toml (replace cursor with code for vscode)

snow remote start \
  my_remote_dev \
  --compute-pool remote_pool \
  --eai-name ALLOW_ALL_INTEGRATION \
  --stage ADMINISTRATION.PUBLIC.REMOTE \
  --ssh

MAKE SURE TO SUSPEND THE SERVICE WHEN DONE THERE IS NO AUTO SUSPEND
snow remote delete SNOW_REMOTE_CHASE_MY_REMOTE_DEV
alter service demo.public.SNOW_REMOTE_CHASE_MY_REMOTE_DEV suspend;

Some other useful commands

describe service demo.public.SNOW_REMOTE_CHASE_MY_REMOTE_DEV;
drop service demo.public.SNOW_REMOTE_CHASE_MY_REMOTE_DEV;
alter service demo.public.SNOW_REMOTE_CHASE_MY_REMOTE_DEV suspend;
alter service demo.public.SNOW_REMOTE_CHASE_MY_REMOTE_DEV resume;
*/
