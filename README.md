# opynfec
Python wrapper for OpenFEC API

***This product uses the openFEC API but is not endorsed or certified by the Federal Election Commission (FEC).***

## Setup

### Download

Download the package via pip with the command

```python
>>> pip install opynfec
```

### Get API Key

For small-scale testing, you can use `"DEMO_KEY"` as your API key, but for higher rate limits, create your own personalized key with the FEC at: https://api.open.fec.gov/developers/.

## Basic Example

First, create you API connection object:

```python
>>> from opynfec import OpynFEC
>>> api = OpynFEC("DEMO_KEY")  # Replace with you own key if you have it
```

Now you can use any of the implemented endpoints. For example, you can search for basic info about President Biden from all of the candidates that have registered with the FEC:

```python
>>> api.search("biden", category="candidates")
[{'name': 'OBAMA, BARACK / JOSEPH R. BIDEN', 'id': 'P80003338', 'office_sought': 'P'}, {'name': 'BIDEN, JOSEPH R JR', 'id': 'P80000722', 'office_sought': 'P'}, ...]
```

See below for an overview of all of the endpoints that have been implemented.

## What has been implemented?

Below we go through each category (in the same way [the openFEC does in their documentation](https://api.open.fec.gov/developers/)) and describe the status of each.

* candidate: use the `candidate()` and `candidates()` methods

* committee: use the `committee()` and `committees()` methods

* dates: *not implemented*

* financial: use the `financial()` method

* search: use the `search()` method

* filings: *not implemented*

* receipts: use the `receipts()` method

* disbursements: use the `disbursements()` method

* loans: *not implemented*

* debts: *not implemented*

* independent expenditures: *not implemented*

* party-coordinated expenditures: *not implemented*

* communication cost: *not implemented*

* electioneering: *not implemented*

* presidential: *not implemented*

* filer resources: *not implemented*

* efiling: *not implemented*

* audit: *not implemented*

* legal: *not implemented*

More work will continue to be done, and contributions are always welcome!