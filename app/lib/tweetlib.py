# libarary for llamafax twitter bot
import os
import tweepy


def startUp():
    print(
        f"""
       _  _  _  _  _                                             _        _  _  _  _                      _            
      (_)(_)(_)(_)(_)                                           (_)      (_)(_)(_)(_) _                  (_)           
            (_) _             _   _  _  _  _     _  _  _  _   _ (_) _  _  (_)        (_)    _  _  _    _ (_) _  _      
            (_)(_)           (_) (_)(_)(_)(_)_  (_)(_)(_)(_)_(_)(_)(_)(_) (_) _  _  _(_) _ (_)(_)(_) _(_)(_)(_)(_)     
            (_)(_)     _     (_)(_) _  _  _ (_)(_) _  _  _ (_)  (_)       (_)(_)(_)(_)_ (_)         (_)  (_)           
            (_)(_)_  _(_)_  _(_)(_)(_)(_)(_)(_)(_)(_)(_)(_)(_)  (_)     _ (_)        (_)(_)         (_)  (_)     _     
            (_)  (_)(_) (_)(_)  (_)_  _  _  _  (_)_  _  _  _    (_)_  _(_)(_)_  _  _ (_)(_) _  _  _ (_)  (_)_  _(_)    
            (_)    (_)   (_)      (_)(_)(_)(_)   (_)(_)(_)(_)     (_)(_) (_)(_)(_)(_)      (_)(_)(_)       (_)(_)      

            Component of Llamafax

            Build v{os.getenv("BUILDVER", "0.0")}
        """
    )


def TweetConfig():
    # Twitter Config
    #   APIKey
    APKey = "RONFnj4FkEAbmKkDLeYrcoLXo"
    #   API key Secret
    APKeySec = "sszPWRvxTP0eslCaG7DrMTTLm0yaMW6H6nJ6beRUJMFA43yYu5"
    #   Access Token
    ACTok = "1545325066602156033-EFRXUkbYRfxZzepJWAh2Plu4CMeTo6"
    #   Access Token secret
    ACTokSec = "ueowEhiWGPlvoxue0y34eU3qQquqVwdPyntkuh4d6Zz6p"
    auth = tweepy.Client(
        consumer_key=APKey,
        consumer_secret=APKeySec,
        access_token=ACTok,
        access_token_secret=ACTokSec,
    )
    # Tweet
    # auth.create_tweet(text="HelloWorld")


def main():
    startUp()


if __name__ == "__main__":
    main()
