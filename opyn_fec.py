from typing import List, Dict, Union, Optional
import math
import urllib.parse
import requests


class OpynFEC:
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
        response.raise_for_status()
        return response.json()

    def _get_unpaginated_request(self, endpoint: str, **kwargs) -> dict:
        # Use max per_page unless specified otherwise
        use_kwargs = {"per_page": 100}
        use_kwargs.update(kwargs)

        all_results = []
        n_pages = math.inf
        page = 1
        while page <= n_pages:
            use_kwargs["page"] = page
            response = self._get_request(endpoint=endpoint, **use_kwargs)
            all_results.extend(response["results"])
            n_pages = response["pagination"]["pages"]
            page += 1

        return all_results

    def candidate(
        self, candidate_id: str, history: bool = False, totals: bool = False, **kwargs
    ) -> List[dict]:
        """Find detailed information about a particular candidate.

        If `history` & `totals` are both False, see the following for query parameters:
        https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__.
        If `history` is True and `cycle` is passed, see:
        https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__history__cycle__.
        If `history` is True and `cycle` is not passed, see:
        https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__history_.
        If `totals` is True, see:
        https://api.open.fec.gov/developers/#/candidate/get_candidate__candidate_id__totals_.

        Parameters
        ----------
        candidate_id : str
            A unique identifier assigned to each candidate registered with the FEC. If
            a person runs for several offices, that person will have separate candidate
            IDs for each office.
        history : bool, optional
            Find out a candidate's characteristics over time. This is particularly
            useful if the candidate runs for the same office in different districts or
            you want to know more about a candidate's previous races. This information
            is organized by candidate_id, so it won't help you find a candidate who ran
            for different offices over time; candidates get a new ID for each office.
            Pass the optional kwarg `cycle` to get info about a particular cycle. By
            default False.
        totals : bool, optional
            This endpoint provides information about a committee's Form 3, Form 3X, or
            Form 3P financial reports, which are aggregated by two-year period. We refer
            to two-year periods as a cycle. The cycle is named after the even-numbered
            year and includes the year before it. To obtain totals from 2013 and 2014,
            you would use 2014. In odd-numbered years, the current cycle is the next
            year — for example, in 2015, the current cycle is 2016. For presidential and
            Senate candidates, multiple two-year cycles exist between elections. By
            default False.
        **kwargs : dict
            Query parameters.

        Returns
        -------
        results : List[dict]
            Results about a particular candidate.

        Raises
        ------
        ValueError
            If user passes both `history` & `totals` as True.
        """
        endpoint = f"candidate/{candidate_id}"

        if history and totals:
            raise ValueError("`history` and `totals` cannot both be True.")
        elif history:
            endpoint = f"{endpoint}/history"
            cycle = kwargs.pop("cycle", False)
            if cycle:
                endpoint = f"{endpoint}/{cycle}"
        elif totals:
            endpoint = f"{endpoint}/totals"

        return self._get_unpaginated_request(endpoint, **kwargs)

    def candidates(
        self,
        search: bool = False,
        totals: bool = False,
        by_office: bool = False,
        by_party: bool = False,
        **kwargs,
    ) -> List[dict]:
        """Fetch basic information about candidates, and use parameters to filter
        results to the candidates you're looking for.

        Each result reflects a unique FEC candidate ID. That ID is particular to the
        candidate for a particular office sought. If a candidate runs for the same
        office multiple times, the ID stays the same. If the same person runs for
        another office — for example, a House candidate runs for a Senate office — that
        candidate will get a unique ID for each office.

        See the following for documentation on available query parameters:
            - If `search`, `totals`, `by_office`, `by_party` are all False:
                https://api.open.fec.gov/developers/#/candidate/get_candidates_
            - If `search` is True:
                https://api.open.fec.gov/developers/#/candidate/get_candidates_search_
            - If `totals` is True, byt `by_office` and `by_party` are False:
                https://api.open.fec.gov/developers/#/candidate/get_candidates_totals_
            - If `totals` and `by_office` is True, but `by_party` is False:
                https://api.open.fec.gov/developers/#/candidate/get_candidates_totals_by_office_
            - If `totals`, `by_office`, and `by_party` are all True:
                https://api.open.fec.gov/developers/#/candidate/get_candidates_totals_by_office_by_party_

        Parameters
        ----------
        search : bool, optional
            Fetch basic information about candidates and their principal committees, by
            default False.
        totals : bool, optional
            Aggregated candidate receipts and disbursements grouped by cycle, by default
            False.
        by_office : bool, optional
            Aggregated candidate receipts and disbursements grouped by office by cycle.
            Only used if `totals` is True, by default False.
        by_party : bool, optional
            Aggregated candidate receipts and disbursements grouped by office by party
            by cycle. Only used if both `totals` and `by_office` is True, by default
            False.
        **kwargs : dict
            Query parameters.

        Returns
        -------
        results : List[dict]
            Candidates results.

        Raises
        ------
        ValueError
            If `search` and `totals` are both True. Or if `search` is True and any of
            {`totals`, `by_office`, `by_party`} are True.
        """
        endpoint = "candidates"
        if search and totals:
            raise ValueError("`search` and `totals` cannot both be True.")
        elif search:
            if totals or by_office or by_party:
                raise ValueError(
                    "If `search` is True, all of {`totals`, `by_office`, `by_party`} "
                    "must be False"
                )
            endpoint = f"{endpoint}/search"
        elif totals:
            endpoint = f"{endpoint}/totals"
            if by_office:
                endpoint = f"{endpoint}/by_office"
                if by_party:
                    endpoint = f"{endpoint}/by_party"

        return self._get_unpaginated_request(endpoint, **kwargs)

    def committee(
        self, committee_id: str, history: bool = False, **kwargs
    ) -> List[dict]:
        endpoint = f"committee/{committee_id}"
        if history:
            endpoint = f"{endpoint}/history"
            cycle = kwargs.pop("cycle", False)
            if cycle:
                endpoint = f"{endpoint}/{cycle}"
        return self._get_unpaginated_request(endpoint, **kwargs)

    def committees(
        self, candidate_id: Optional[str] = None, history: bool = False, **kwargs
    ) -> List[dict]:
        if candidate_id is None:
            endpoint = "committees"
        else:
            endpoint = f"candidate/{candidate_id}"
            if history:
                endpoint = f"{endpoint}/history"
                cycle = kwargs.pop("cycle", False)
                if cycle:
                    endpoint = f"{endpoint}/{cycle}"
        return self._get_unpaginated_request(endpoint, **kwargs)

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
