from mastodon import Mastodon

def account1Login():
    mastodon = Mastodon(
        access_token="lf_TsVX_Jo-hWnGiZ_Z1C1dSYGUGXoGdU0WRxYS0Muw",
        api_base_url="https://mastodon.social",
        client_id="iO7q2BWCTYnZ1w_xAVD3jmPHJWO7q-zmxM0oDBFocj0",
        client_secret="rodhS6aLzkG4VyOvRh6iP7_-WQXvDrzGscC-fhijP5Y",
    )

    print(mastodon.auth_request_url())

    mastodon.log_in(code=input("Enter OAutho code: "), to_file="pytooter_usercred.secret")

def account2Login():
    mastodon = Mastodon(
        access_token="obzneA4Wo7TbEjhAKGYHj0N5_mVdWUq8FSssCSrhz9A",
        api_base_url="https://mastodon.social",
        client_id="uuMZDvJocOd3gvwc88-OFPTVQUaZ-pfYMU6Xn-0FdiI",
        client_secret="tsAR_OdVFMNedRunN9NVtSZa8kezaMLr-5c4m8fAvz4",
    )

    print(mastodon.auth_request_url())

    mastodon.log_in(code=input("Enter OAutho code: "), to_file="pytooter_usercred.secret")


#Select account to be scraped with

account1Login()