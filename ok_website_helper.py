# this will need to be udpated since we will eventually be extracting files from 2009 onward
import requests

base_url = 'http://webserver1.lsb.state.ok.us/cf/'




def get_vote_docs_from(session_year):
    result = requests.get(base_url + session_year)
    result.raise_for_status()

    return result.content.decode('utf-8')