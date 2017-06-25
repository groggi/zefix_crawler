import requests
import itertools
import string
import pprint
import time
import random
import pickle

ENTRY_STEP = 500


def get_companies(search: str, session: requests.Session):
    results = []
    offset = 0
    has_more = True
    while has_more:
        # be nice
        time.sleep(random.randint(0, 3))
        search_data = {"name": search, "maxEntries": ENTRY_STEP, "offset": offset}
        search_request = session.post(url="https://www.zefix.ch/ZefixREST/api/v1/firm/search.json", json=search_data)
        if search_request.status_code != requests.codes.ok:
            print("Failed:")
            print("""\tsearch: {search}\n\toffset: {offset}\n\tresult: {result}""".format(search=search, offset=offset,
                                                                                          result=search_request.text))
            has_more = False
            continue

        json_result = search_request.json()
        results.extend(json_result['list'])
        has_more = bool(json_result['hasMoreResults'])
        offset += ENTRY_STEP
    return results


# TODO: add digits, punctuations and so on. Needs some checking...
search_strings = [''.join(k) for k in itertools.product(string.ascii_lowercase, repeat=3)]
search_total = len(search_strings)
all_found = []

session = requests.Session()

for step, search in enumerate(search_strings):
    print("Working on {step}/{total}".format(step=step, total=search_total))
    all_found.extend(get_companies(search, session))
    print("Total records: {records_total}".format(records_total=len(all_found)))

with open("result.pickle", "wb") as f:
    pickle.dump(all_found, f)

pprint.pprint(all_found)
print(len(all_found))
