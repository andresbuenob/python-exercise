from requests_oauthlib import OAuth2Session

# Credentials you get from registering a new application
client_id = "10363d4146502e4319c1"
client_secret = "c89cd5647f21cd9f0d90470030bdad61f140cf04"

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"


github = OAuth2Session(client_id)

print("before go to url")
scope = ["user"]
# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print("state: ", state)
print("Please go here and authorize,", authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input()

print("fetching token", redirect_response)
# Fetch the access token
github.fetch_token(
    token_url, client_secret=client_secret, authorization_response=redirect_response
)
print("get response")
# Fetch a protected resource, i.e. user profile
r = github.get("https://api.github.com/user")
print(r.content)
