# Libarry to handles gathering external data, Ingresses Data to database
import json
from enum import Enum
import requests
import random
import sys
import getopt
import os


def startUp():
    print(
        f"""
        ██╗███╗   ██╗ ██████╗ ██████╗ ███████╗███████╗███████╗
        ██║████╗  ██║██╔════╝ ██╔══██╗██╔════╝██╔════╝██╔════╝
        ██║██╔██╗ ██║██║  ███╗██████╔╝█████╗  ███████╗███████╗
        ██║██║╚██╗██║██║   ██║██╔══██╗██╔══╝  ╚════██║╚════██║
        ██║██║ ╚████║╚██████╔╝██║  ██║███████╗███████║███████║
        ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

            Component of Llamafax

            Build v{os.getenv("BUILDVER", "0.0")}

        """
    )


class CATSch(Enum):
    """Schema for API Categories"""

    fact = "facts?limit="
    quote = "quotes?category="
    quoteCats = ["happiness", "education"]
    allCats = ["fact"]  # "quote"


def getAPINinja(
    Key: str, Category: str = "fact", Limit: str = ..., catCat: str = "fact"
) -> list:
    """Queries an API Ninja API to get back the requested data
    \nCATEGORY OPTIONS (Defaults)
    \n-> fact ; Limit (20) (**30)
    \n QUOTE REMOVED AS THE OUTPUT WAS UNDESIREABLE
    \n-> quote : Limit (10) ; Categories[catCat] (random)
    \nReturns response from API in json"""

    def ifNoLimit(Category: str):
        if Category == "fact":
            return 20  # 30
        elif Category == "quote":
            return 10
        else:
            raise Exception(f"Category '{Category}' is undefined.")

    def buildSuffix(Category: str, Limit: int = ..., catCat: str = ...):
        # Ensures Category has a Limit
        if Limit == Ellipsis:
            Limit = ifNoLimit(Category)
        # build suffix
        if Category == "fact":
            return CATSch.fact.value + str(Limit)
        elif Category == "quote":
            if (
                catCat == Ellipsis
            ):  # if no quote category is provided, a random one will be asigned
                catCat = random.choice(CATSch.quoteCats.value)
            return CATSch.quote.value + catCat + "&limit=" + str(Limit)
        else:
            raise Exception(f"Category '{Category}' is undefined.")

    def getRequest(Suffix: str, Key: str = Key) -> json:
        return json.loads(
            requests.get(
                "https://api.api-ninjas.com/v1/" + Suffix,
                headers={"X-Api-Key": f"{Key}"},
            ).content
        )

    return getRequest(buildSuffix(Category, Limit, catCat))


def strip(Input: dict) -> dict:
    """Intakes raw data from API Injest, returns data as a Dictionary"""
    for Cat, Data in Input.items():
        if Cat in CATSch.allCats.value:
            return {"data": Data}


def getArgs():
    argList = sys.argv[1:]
    optS = "k:"
    optL = ["APIKey="]
    try:
        args, scrapValues = getopt.getopt(argList, optS, optL)
        for cArg, cVal in args:
            if cArg in ("-k", "--APIKey"):
                APIKey = cVal
            else:
                Exception(f"Invalid Argument provided '{argList}'")
    except:
        Exception(
            f"Error proccesing arguments. Please create bug report if this continues."
        )
    return APIKey, scrapValues


def main():
    startUp()


if __name__ == "__main__":
    main()
