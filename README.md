# IAM MFA

This command line tool helps you manage AWS CLI credentials with MFA (multi-factor authentication).

This is intended as a companion to an IAM policy that requiring MFA everywhere, including on API access.  One such policy is inculded in this readme.

The tool takes a source IAM profile (which should store your permanent credentials) and an MFA code and outputs API AWS credentials to a destination IAM profile.  The output credentials are valid for 24 hours and are blessed with MFA (and thus can be used on APIs that require MFA). 

## Instalation

It's a pip library, installed by `pip install iam-mfa`.

It requires the AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html


## Usage

`iam-mfa <source_profile> <dest_profile> <username>`

Arguments:

* **source_profile**:  The profile to use for calling `sts get-session-token`; this should contain your permanent AWS API credentials
* **dest_profile**:    The profile in which the temporary credentials will be saved; note that this profile will be overridden
* **username**:        The IAM username that owns the source_profile credentials

The MFA code is provided as an input to the script running so that it isn't stored in bash history.

## AWS IAM Policy

It is recommended that you have an IAM policy on your AWS account that enforces the use of multi-factor authentication for all access.

Below is a policy that does the following:

* Allow users to change their own password
* Allow users to view and edit their own MFA devices (a necessary component to requiring them to have MFA)
* Prevent users from doing most things if they logged in to the console without MFA
* Still allow users to set up MFA if they logged in without it
* Enforce these rules for both console and API aceess

It is best to create this as an IAM policy, and then attach it to any user groups that have human users.  You can also attach the policy to a user directly, but that's harder to manage.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:ChangePassword",
                "iam:CreateVirtualMFADevice",
                "iam:EnableMFADevice",
                "iam:ResyncMFADevice",
                "iam:DeleteVirtualMFADevice",
                "iam:DeactivateMFADevice",
                "iam:ListMFADevices",
                "iam:ListVirtualMFADevices",
                "iam:ListAccessKeys",
                "iam:GetAccessKeyLastUsed",
                "iam:GetUser"
            ],
            "Resource": [
                "arn:aws:iam::*:mfa/${aws:username}",
                "arn:aws:iam::*:user/${aws:username}"
            ]
        },
        {
            "Sid": "BlockMostAccessUnlessSignedInWithMFA",
            "Effect": "Deny",
            "NotAction": [
                "iam:CreateVirtualMFADevice",
                "iam:ListVirtualMFADevices",
                "iam:EnableMFADevice",
                "iam:ResyncMFADevice",
                "iam:DeleteVirtualMFADevice",
                "iam:DeactivateMFADevice",
                "iam:ListAccountAliases",
                "iam:ListUsers",
                "iam:ListSSHPublicKeys",
                "iam:ListAccessKeys",
                "iam:GetAccessKeyLastUsed",
                "iam:ListServiceSpecificCredentials",
                "iam:ListMFADevices",
                "iam:GetAccountSummary",
                "iam:ChangePassword",
                "iam:GetUser",
                "sts:GetSessionToken"
            ],
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```
