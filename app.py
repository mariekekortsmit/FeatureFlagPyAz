# app.py
import os
from azure.appconfiguration import AzureAppConfigurationClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure App Configuration connection string
connection_string = os.environ.get("AZURE_APP_CONFIG_CONNECTION_STRING")

# Function to check the status of a feature flag
def is_feature_flag_enabled(feature_flag_name, env):
    with AzureAppConfigurationClient.from_connection_string(connection_string) as client:
        feature_flag = client.get_configuration_setting(key=f".appconfig.featureflag/{feature_flag_name}", label=env)
        if feature_flag.enabled:
            return True
        return False

# Function to list all feature flags
def list_feature_flags(env):
    with AzureAppConfigurationClient.from_connection_string(connection_string) as client:
        feature_flags = []
        # Retrieve all keys that start with the feature flag prefix
        feature_flag_settings = client.list_configuration_settings(label_filter=env, key_filter=".appconfig.featureflag/*")
        for setting in feature_flag_settings:
            feature_flags.append({
                'key': setting.key,
                'label': setting.label,
                'enabled': setting.enabled
            })
        return feature_flags

def get_environment_label():
    # Custom logic to determine environment
    # Example: Check a specific environment variable
    if os.environ.get("ENVIRONMENT") == "prod":
        return "prod"
    else:
        return "dev"

def main():
    # Feature flag name
    feature_flag_name = "BetaFeature"
    env = get_environment_label()

    # Check if feature flag is enabled for this env
    if is_feature_flag_enabled(feature_flag_name, env):
        print("Hello World from the Beta Feature!")
    else:
        print("Hello World!")
    
    #Print all available tags:
    print(f"All available flags for this env are: {list_feature_flags(env)}")

if __name__ == "__main__":
    main()
