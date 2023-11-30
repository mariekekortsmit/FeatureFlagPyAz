# app.py
import os
from azure.appconfiguration import AzureAppConfigurationClient
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Azure App Configuration connection string from environment variables
connection_string = os.environ.get("AZURE_APP_CONFIG_CONNECTION_STRING")

# Function to check if a specific feature flag is enabled in a given environment
def is_feature_flag_enabled(feature_flag_name, env):
    with AzureAppConfigurationClient.from_connection_string(connection_string) as client:
        # Fetch the configuration setting for the specified feature flag and environment
        feature_flag = client.get_configuration_setting(key=f".appconfig.featureflag/{feature_flag_name}", label=env)
        # Return True if the feature flag is enabled, False otherwise
        return feature_flag.enabled

# Function to list all feature flags for a given environment
def list_feature_flags(env):
    with AzureAppConfigurationClient.from_connection_string(connection_string) as client:
        feature_flags = []
        # Retrieve all configuration settings that start with the feature flag prefix
        feature_flag_settings = client.list_configuration_settings(label_filter=env, key_filter=".appconfig.featureflag/*")
        for setting in feature_flag_settings:
            # Add each feature flag's details to the list
            feature_flags.append({
                'key': setting.key,
                'feature_id': setting.feature_id,
                'label': setting.label,
                'enabled': setting.enabled
            })
        return feature_flags

# Function to filter and return only enabled feature flags from a list
def list_enabled_feature_flags(feature_list):
    # Using list comprehension to filter out items with 'enabled': True
    return [feature for feature in feature_list if feature.get('enabled')]

# Function to get the label of the current environment
def get_environment_label():
    # Determine the environment label (e.g., 'prod' or 'dev') based on environment variables
    return "prod" if os.environ.get("ENVIRONMENT") == "prod" else "dev"

# Example function for BetaFeature
def BetaFeature():
    # Implement the behavior for when BetaFeature is enabled
    print("Hello, world BetaFeature!")

# Example function for TestFeature
def TestFeature():
    # Implement the behavior for when TestFeature is enabled
    print("Goodbye, world TestFeature!")

# Main function to execute the script
def main():
    # Determine the current environment
    env = get_environment_label()

    # Example usage: check if a specific feature flag is enabled in the current environment
    feature_flag_name = "BetaFeature"
    if is_feature_flag_enabled(feature_flag_name, env):
        print(f"{feature_flag_name} is enabled for this env!\n")
    else:
        print(f"{feature_flag_name} is DISabled for this env!\n")
    
    # Print all available feature flags for the current environment
    all_tags = list_feature_flags(env)
    print("All available flags for this env are:")
    for flag in all_tags:
        print(flag)
    print()

    # Execute functions corresponding to the enabled feature flags
    print("Run only the enabled functions for this env:")
    for flag in list_enabled_feature_flags(all_tags):
        func_name = flag['feature_id']

        # Check if the function name exists and is callable
        if func_name in globals() and callable(globals()[func_name]):
            globals()[func_name]()
        else:
            print(f"Function '{func_name}' not found.")

# Entry point of the script
if __name__ == "__main__":
    main()
