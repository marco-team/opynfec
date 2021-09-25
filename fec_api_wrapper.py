from typing import List, Dict, Union, Optional
import urllib.parse
import requests


class FECAPIWrapper:
    BASE_URL = "https://api.open.fec.gov/v1/"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get_request(self, endpoint: str, **kwargs) -> dict:
        """General method for making a GET request to the API.

        Parameters
        ----------
        endpoint : str
            Additional url path endpoint to be tacked on to the end of the BASE_URL, but
            before the query parameters.
        **kwargs : dict
            Any query parameters, besides your API key.

        Returns
        -------
        response : dict
            The API response.
        """
        kwargs.update({"api_key": self.api_key})
        query = urllib.parse.urlencode(kwargs, doseq=True, quote_via=urllib.parse.quote)
        url = f"{self.BASE_URL}{endpoint.strip('/')}/?{query}"
        response = requests.get(url)
        return response.json()

    def candidate(self, candidate_id: str, **kwargs) -> dict:
        """Find detailed information about a particular candidate.

        Use the candidate_id to find the most recent information about that candidate.
        See https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__
        for detailed query parameter info.

        Parameters
        ----------
        candidate_id : str
            A unique identifier assigned to each candidate registered with the FEC. If a
            person runs for several offices, that person will have separate candidate
            IDs for each office.
        **kwargs : dict
            Additional query parameters. See API docs for more info.

        Returns
        -------
        result: dict
            Dict of fields representing a single candidate.
        """
        response = self._get_request(f"candidate/{candidate_id}", **kwargs)
        return response["results"][0]

    def candidate_history(
        self, candidate_id: str, cycle: Optional[int] = None, **kwargs
    ) -> List[dict]:
        """Find out a candidate's characteristics over time.

        This is particularly useful if the candidate runs for the same office in
        different districts or you want to know more about a candidate's previous races.

        This information is organized by candidate_id, so it won't help you find a
        candidate who ran for different offices over time; candidates get a new ID for
        each office.

        See https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__history_
        for info about using without `cycle` parameter.

        See https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__history__cycle__
        for info about using with `cycle` parameter.


        Parameters
        ----------
        candidate_id : str
            A unique identifier assigned to each candidate registered with the FEC. If a
            person runs for several offices, that person will have separate candidate
            IDs for each office.
        cycle : Optional[int], optional
            Two-year election cycle in which a candidate runs for office. Calculated
            from Form 2. The cycle begins with an odd year and is named for its ending,
            even year. This cycle follows the traditional house election cycle and
            subdivides the presidential and Senate elections into comparable two-year
            blocks. To retrieve data for the entire four years of a presidential term or
            six years of a senatorial term, you will need the election_full flag. By
            default None

        Returns
        -------
        results : List[dict]
            Candidate history.
        """
        endpoint = f"candidate/{candidate_id}/history"
        if cycle is not None:
            endpoint = f"{endpoint}/{cycle}"
        return self._get_request(endpoint, **kwargs)["results"]

    def search(self, q: Union[str, List[str]], category: str) -> List[Dict[str, str]]:
        """Search for candidates or committees by name.

        If you're looking for information on a particular person or group, using a name
        to find the candidate_id or committee_id on this endpoint can be a helpful first
        step. See https://api.open.fec.gov/developers/#/search for API documentation.

        Parameters
        ----------
        q : Union[str, List[str]]
            Name(s) (candidate or committee) to search for.
        category : {'candidates', 'committees'}
            Whather to search for candidates or committees.

        Returns
        -------
        results : List[Dict[str, str]]
            The search results

        Raises
        ------
        ValueError
            If `category` is not one of {'candidates', 'committees'}.
        """
        if category not in {"candidates", "committees"}:
            raise ValueError(
                "`category` should be one of {'candidates', 'committees'}, but got "
                f"{category!r}"
            )
        return self._get_request(f"names/{category}", q=q)["results"]
