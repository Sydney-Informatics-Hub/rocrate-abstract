# from pathlib import Path

import json
from pathlib import Path
from fuzz import random_text, random_property
from pytest_httpserver import HTTPServer

from rocrate_abstract.rocrate_abstract import Crate, minimal_crate


# https://pytest-httpserver.readthedocs.io/en/latest/ for testing fetch


def test_crate(tmp_path):
    """Build and save and reload a crate"""
    jcrate = minimal_crate()
    for i in range(1000):
        props = {"name": random_text(4), "description": random_text(11)}
        for j in range(30):
            prop, val = random_property()
            props[prop] = val
        jcrate.add("Dataset", f"#ds{i:05d}", props)
    jsonf = Path(tmp_path) / "ro-crate-metadata.json"
    jcrate.write_json(Path(tmp_path))
    with open(jsonf, "r") as jfh:
        jsonld = json.load(jfh)
        jcrate2 = TinyCrate(jsonld=jsonld)
        for i in range(1000):
            eid = f"#ds{i:05d}"
            ea = jcrate.get(eid)
            eb = jcrate2.get(eid)
            assert ea.props == eb.props


def test_load_file(crates):
    cratedir = crates["textfiles"]
    with open(Path(cratedir) / "ro-crate-metadata.json", "r") as jfh:
        jsonld = json.load(jfh)
        crate = TinyCrate(jsonld=jsonld, directory=cratedir)
        tfile = crate.get("doc001/textfile.txt")
        contents = tfile.fetch()
        with open(Path(cratedir) / "doc001" / "textfile.txt", "r") as tfh:
            contents2 = tfh.read()
            assert contents == contents2


def test_load_url(crates, httpserver: HTTPServer):
    # test http endpoint with some content
    contents = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
    httpserver.expect_request("/textfileonurl.txt").respond_with_data(
        contents, content_type="text/plain"
    )

    cratedir = crates["textfiles"]
    with open(Path(cratedir) / "ro-crate-metadata.json", "r") as jfh:
        jsonld = json.load(jfh)
        crate = TinyCrate(jsonld=jsonld, directory=cratedir)
        # add an entity to the crate with the endpoint URL as the id
        urlid = httpserver.url_for("/textfileonurl.txt")
        crate.add("File", urlid, {"name": "textfileonurl.txt"})
        # get the entity and try to fetch
        efile = crate.get(urlid)
        contents2 = efile.fetch()
        assert contents == contents2
