"""
This example shows how to get the names of the 2020 presidential candidates.
"""

from opynfec import OpynFEC


def main():
    # Replace with your personal API key for higher rate limits
    api = OpynFEC(api_key="DEMO_KEY")

    # Here is the call to get all 2020 presidential candidates
    pres_candidates_2020 = api.candidates(  # Use the `candidates` method
        search=True,  # You are searching for candidates (not providing name, id, etc.)
        election_year=2020,  # election year
        office="P",  # P = president, can also use H or S for House/Senate
        election_full=True,  # Get data for full election cycle, otherwise only gets for 1 yr
        has_raised_funds=True,  # To narrow down the list, only get serious candidates
    )

    # Lots of info returned in the result, but we just want to see the names
    names = list(map(lambda c: c.get("name", None), pres_candidates_2020))
    print(names)


if __name__ == "__main__":
    main()
