"""
Tools for accessing the Dota 2 match history web API
"""

import urllib
import logging

API_KEY = None
BASE_URL = "https://api.steampowered.com/IDOTA2Match_570/"

logger = logging.getLogger("dota2py")


def set_api_key(key):
    """
    Set your API key for all further API queries
    """

    global API_KEY
    API_KEY = key


def url_map(base, params):
    """
    Return a URL with get parameters based on the params passed in
    This is more forgiving than urllib.urlencode and will attempt to coerce
    non-string objects into strings and automatically UTF-8 encode strings.

    @param params: HTTP GET parameters
    """

    url = base

    if '?' not in url and len(params):
        url += "?"
    elif '?' in url:
        if not url.endswith("&") and not url.endswith("?"):
            url += "&"

    for key, value in params.iteritems():
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)

            url += "%s=%s&" % (urllib.quote_plus(key.encode("utf-8")),
                               urllib.quote_plus(value.encode("utf-8")))

    if url.endswith("&") or url.endswith("?"):
        url = url[:-1]

    return str(url)


def get_page(url):
    """
    Fetch a page
    """

    import requests
    logger.debug('GET %s' % (url, ))
    return requests.get(url)


def make_request(name, params=None, version="V001", key=None,
                 fetcher=get_page, base=None):
    """
    Make an API request
    """

    params = params or {}
    params["key"] = key or API_KEY

    if not params["key"]:
        raise ValueError("API key not set")

    url = url_map("%s%s/%s/" % (base or BASE_URL, name, version), params)
    return fetcher(url)


def get_match_history(start_at_match_id=None, player_name=None, hero_id=None,
                      skill=0, date_min=None, date_max=None, account_id=None,
                      league_id=None, matches_requested=None,
                      **kwargs):
    """
    List of most recent 25 matches before start_at_match_id
    """

    params = {
        "start_at_match_id": start_at_match_id,
        "player_name": player_name,
        "hero_id": hero_id,
        "skill": skill,
        "date_min": date_min,
        "date_max": date_max,
        "account_id": account_id,
        "league_id": league_id,
        "matches_requested": matches_requested,
    }

    return make_request("GetMatchHistory", params, **kwargs)


def get_match_history_by_sequence_num(start_at_match_seq_num,
                                      matches_requested=None, **kwargs):
    """
    Most recent matches ordered by sequence number
    """
    params = {
        "start_at_match_seq_num": start_at_match_seq_num,
        "matches_requested": matches_requested
    }

    return make_request("GetMatchHistoryBySequenceNum", params,
        **kwargs)


def get_match_details(match_id, **kwargs):
    """
    Detailed information about a match
    """

    return make_request("GetMatchDetails", {"match_id": match_id}, **kwargs)


def get_steamid(vanityurl, **kwargs):
    """
    Get a players steamid from their steam name/vanity url
    """

    params = {"vanityurl": vanityurl}
    return make_request("ResolveVanityURL", params, version="v0001",
        base="http://api.steampowered.com/ISteamUser/")
