## What is Remote Dev?

Container Runtime Remote Dev is a cloud-based development environment that runs inside Snowpark Container Services executing a Container Runtime image. This allows you to develop directly in the Container Runtime ecosystem with full access to your data, compute resources, and a persistent development environment, so you can leverage the full power of distributed ML, flexibility in packages and compute, and many other optimizations.

## Development Options

### Option 1: Stay in Your Local VS Code, Execute Remotely
Keep using your familiar local VS Code or Cursor, but execute code in Snowflake's cloud environment with full access to data and compute.

### Option 2: Spin Up On-Demand Web-based VS Code
Get a full VS Code environment running in your browser - no local setup required.

## Setup Instructions

### Step 1: Database and Infrastructure Setup

1. **Run the SQL Setup Script**
   
   Execute the `setup.sql` file in your Snowflake account.  You can replace the sysadmin role with whatever role will need the ability to leverage Remote Dev such as Data Scientist role. This script will:
   - Create network rules for external access
   - Set up external access integration
   - Create a dedicated compute pool for remote development
   - Configure the necessary stage for file storage for when the service is shut down

### Step 2: Local Environment Setup

1. **Install Required Tools**
   
   ```bash
   # Install websocat for WebSocket communication
   brew install websocat
   
   # Install uv (recommended Python package manager)
   brew install uv
   ```

2. **Navigate to Remote Setup Directory**
   
   ```bash
   cd Remote_setup
   ```

3. **Set Up Python Environment**
   
   ```bash
   # Sync dependencies (if using uv)
   uv sync
   
   # Activate virtual environment (Comes with the updated version of Snowflake-CLI)
   source .venv/bin/activate
   ```

4. **Configure Snowflake Connection**
   
   ```bash
   # List existing connections
   snow connection list
   
   # If you need to create a new connection
   snow connection add

   # Set your default connection to the one you need
   snow connection set-default <your_connection_name>
   ```

### Step 3: Start Remote Development Environment

1. **Launch Remote Development Session**
   
   ```bash
   snow remote start \
     my_remote_dev \
     --compute-pool <Your_Compute_Pool> \
     --eai-name pypi_access_integration \
     --stage <DB.SCHEMA.YOUR_STAGE_NAME> \
     --ssh
   ```

   This command will:
   - Create a remote development environment named `my_remote_dev`
   - Use the your compute pool
   - Apply the external access integration
   - Mount the specified stage for persistent storage
   - Enable SSH access

## Important Notes

**CRITICAL**: Make sure to suspend the service when done. There is no auto-suspend feature.

```bash
# To delete the remote environment
snow remote delete SNOW_REMOTE_CHASE_MY_REMOTE_DEV
```
