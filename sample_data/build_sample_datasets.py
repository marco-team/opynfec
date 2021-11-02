import json
from opynfec import OpynFEC


def main():
    api = OpynFEC("YpWoDU7JpXhTYpcdzLQtxhyRNevLuuQqxNYR7TR3")

    # Data to store to save to files at the end
    committees = []
    committee_to_committee = []
    individual_to_committee = []

    # Get presidential candidates
    pres_candidates_2020 = api.candidates(
        search=True,
        election_year=2020,
        office="P",
        election_full=True,
        name=["biden", "trump"],
    )

    for candidate in pres_candidates_2020:
        print(f"{candidate['name']} ({candidate['candidate_id']})")

        # Get each candidate's principal committees
        principal_committees = candidate["principal_committees"]

        # Get top 20 largest disbursements made to candidate committees
        direct_disbursements = api.disbursements(
            by_recipient_id=True,
            cycle=2020,
            sort="-total",
            recipient_id=list(map(lambda c: c["committee_id"], principal_committees)),
            result_limit=20,
        )

        for disbursement in direct_disbursements:
            print("\t", disbursement["committee_name"])

        # Get the largest donations made by other committees to these committees
        secondary_disbursements = api.disbursements(
            by_recipient_id=True,
            cycle=2020,
            sort="-total",
            recipient_id=list(map(lambda d: d["committee_id"], direct_disbursements)),
            result_limit=20,
        )

        for disbursement in secondary_disbursements:
            print("\t\t", disbursement["committee_name"])

        all_disbursements = direct_disbursements + secondary_disbursements
        committee_to_committee.extend(all_disbursements)

        # Get top largest individual donors to all of those committees
        # Can only specify max of 10 IDs per call
        all_committee_ids = list(
            map(lambda d: d["committee_id"], principal_committees + all_disbursements)
        )
        indv_donors = []
        for i in range(0, len(all_committee_ids), 10):
            committee_ids_subset = all_committee_ids[i : i + 10]
            indv_donors_subset = api.receipts(
                committee_id=committee_ids_subset,
                is_individual=True,
                two_year_transaction_period=2020,
                sort="-contribution_receipt_amount",
                result_limit=20,
            )
            indv_donors.extend(indv_donors_subset)

        for indv_donor in indv_donors:
            print(
                "\t\t\t",
                indv_donor["contributor_name"],
                indv_donor["contribution_receipt_amount"],
            )

        individual_to_committee.extend(indv_donors)

        # Save all committees
        committees.extend(api.committees(committee_id=all_committee_ids, cycle=2020))

    # Save all the data
    with open("candidates.json", "a") as f:
        json.dump(pres_candidates_2020, f, indent=4)

    with open("committee_to_committee.json", "a") as f:
        json.dump(committee_to_committee, f, indent=4)

    with open("individual_to_committee.json", "a") as f:
        json.dump(individual_to_committee, f, indent=4)

    with open("committees.json", "a") as f:
        json.dump(committees, f, indent=4)


if __name__ == "__main__":
    main()
