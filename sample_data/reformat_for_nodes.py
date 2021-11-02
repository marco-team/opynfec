import json
import uuid


def main():
    #### Load in the datasets
    with open("sample_data/candidates.json") as f:
        candidates = json.load(f)

    with open("sample_data/committee_to_committee.json") as f:
        committee_to_committee = json.load(f)

    with open("sample_data/individual_to_committee.json") as f:
        individual_to_committee = json.load(f)

    #### Make nodes with the following form
    # {
    #   'type': one of ['candidate', 'committee', 'individual']
    #   'id': ID of committee/individual/candidate
    #   'name': name of committee/individual/candidate
    # }
    #
    #### Make edges with the following form
    # {
    #   'source': ID of committee/individual making contribution
    #   'quantity': dollars of contribution
    #   'date': date of contribution
    #   'target': ID of committee/individual receiving contribution
    # }
    #
    # Indiviudals dont have IDs, so generate them. Just in case check all IDs to make sure

    nodes = []
    edges = []
    for committee_donation in committee_to_committee:
        source_id = (
            str(uuid.uuid4())
            if committee_donation["committee_id"] is None
            else committee_donation["committee_id"]
        )
        target_id = (
            str(uuid.uuid4())
            if committee_donation["recipient_id"] is None
            else committee_donation["recipient_id"]
        )

        nodes.append(
            {
                "type": "committee",
                "id": source_id,
                "name": committee_donation["committee_name"],
            }
        )

        nodes.append(
            {
                "type": "committee",
                "id": target_id,
                "name": committee_donation["recipient_name"],
            }
        )

        edges.append(
            {
                "source": source_id,
                "quantity": committee_donation["total"],
                "date": None,
                "target": target_id,
            }
        )

    for candidate in candidates:
        cndt_id = (
            str(uuid.uuid4())
            if candidate["candidate_id"] is None
            else candidate["candidate_id"]
        )
        nodes.append(
            {
                "type": "candidate",
                "id": cndt_id,
                "name": candidate["name"],
            }
        )

        for principal_committee in candidate["principal_committees"]:
            princ_cmte_id = (
                str(uuid.uuid4())
                if principal_committee["committee_id"] is None
                else principal_committee["committee_id"]
            )
            nodes.append(
                {
                    "type": "committee",
                    "id": princ_cmte_id,
                    "name": principal_committee["name"],
                }
            )
            edges.append(
                {
                    "source": princ_cmte_id,
                    "quantity": None,
                    "date": None,
                    "target": cndt_id,
                }
            )

    for individual_donation in individual_to_committee:
        committee_id = (
            str(uuid.uuid4())
            if individual_donation["committee"]["committee_id"] is None
            else individual_donation["committee"]["committee_id"]
        )

        # FIgure out if contributor is truly an individual or committee
        contributor = individual_donation.get("contributor", None)
        if contributor is not None:
            # This is a committee-to-committee transaction
            contributor_type = "committee"
            contributor_id = contributor["committee_id"]
            contributor_name = contributor["name"]
        else:
            # This is an individual to committee transaction
            contributor_type = "individual"
            contributor_id = (
                str(uuid.uuid4())
                if individual_donation["contributor_id"] is None
                else individual_donation["contributor_id"]
            )
            contributor_name = individual_donation["contributor_name"]

        nodes.append(
            {
                "type": contributor_type,
                "id": contributor_id,
                "name": contributor_name,
            }
        )

        nodes.append(
            {
                "type": "committee",
                "id": committee_id,
                "name": individual_donation["committee"]["name"],
            }
        )

        edges.append(
            {
                "source": contributor_id,
                "quantity": individual_donation["contribution_receipt_amount"],
                "date": individual_donation["load_date"],
                "target": committee_id,
            }
        )

    #### Now write them to 2 new files
    with open("sample_data/nodes.json", "w") as f:
        json.dump(nodes, f)

    with open("sample_data/edges.json", "w") as f:
        json.dump(edges, f)


if __name__ == "__main__":
    main()
