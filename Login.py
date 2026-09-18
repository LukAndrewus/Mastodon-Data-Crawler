from mastodon import Mastodon

mastodon = Mastodon(
    access_token="lf_TsVX_Jo-hWnGiZ_Z1C1dSYGUGXoGdU0WRxYS0Muw",
    api_base_url="https://mastodon.social",
    client_id="iO7q2BWCTYnZ1w_xAVD3jmPHJWO7q-zmxM0oDBFocj0",
    client_secret="rodhS6aLzkG4VyOvRh6iP7_-WQXvDrzGscC-fhijP5Y",
)

print(mastodon.auth_request_url())

mastodon.log_in(code=input("Enter OAutho code: "), to_file="pytooter_usercred.secret")
