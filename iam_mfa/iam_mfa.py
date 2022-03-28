import json
import subprocess
import argparse

def main():
    # Declare and parse arguments
    parser = argparse.ArgumentParser(description="Prompts for an MFA token and then uses AWS STS to generate temporary MFA API credentials and save them to `dest_profile`")
    parser.add_argument("source_profile", help="The profile to use for calling `sts get-session-token`; this should contain your permanent AWS API credentials")
    parser.add_argument("dest_profile", help="The profile in which the temporary credentials will be saved; note that this profile will be overridden")
    parser.add_argument("username", help="The IAM username that owns the source_profile credentials")
    args = parser.parse_args()
    output = subprocess.check_output(["aws", "configure", "list-profiles"])
    
    # Check that the output profile doesn"t contain permanent credentials
    if args.dest_profile in output.decode().split("\n"):
        try:
            has_key = bool(subprocess.check_output(["aws", "configure", "--profile", args.dest_profile, "get", "aws_session_token"]))
        except subprocess.CalledProcessError:
            has_key = False
        if not has_key:
            confirm = input(f"WARNING: keys in {args.dest_profile} will be overwritten.  Do you want to proceed (yes/no)? ")
            if confirm.lower() != "yes":
                print("Update canceled")
                return

    # Prompt the user for an MFA token
    mfa_token = input("MFA Token: ")

    # Call `sts get-session-token` and save the result to dest_profile
    command = [
        "aws",
        "--profile", args.source_profile,
        "iam", "list-mfa-devices",
        "--user-name", args.username
    ]
    output = subprocess.check_output(command).decode()
    serial_number = json.loads(output)["MFADevices"][0]["SerialNumber"]
    command = [
        "aws",
        "--profile", args.source_profile,
        "sts", "get-session-token",
        "--serial-number", serial_number,
        "--token-code", mfa_token
    ]
    output = subprocess.check_output(command).decode()
    credentials = json.loads(output)["Credentials"]
    command = [
        "aws", "configure",
        "--profile", args.dest_profile,
        "set", "aws_access_key_id",
        credentials["AccessKeyId"]
    ]
    subprocess.check_output(command)
    command = [
        "aws", "configure",
        "--profile", args.dest_profile,
        "set", "aws_secret_access_key",
        credentials["SecretAccessKey"]
    ]
    subprocess.check_output(command)
    command = [
        "aws", "configure",
        "--profile", args.dest_profile,
        "set", "aws_session_token",
        credentials["SessionToken"]
    ]
    subprocess.check_output(command)
    print(f"{args.dest_profile} credentials valid until {credentials['Expiration']}")

if __name__ == "__main__":
    main()
