#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, web

storefront_list = [
    "ae",
    "ao",
    "ar",
    "at",
    "au",
    "az",
    "bb",
    "be",
    "bg",
    "bm",
    "br",
    "by",
    "bo",
    "ca",
    "kh",
    "ch",
    "cl",
    "cn",
    "co",
    "cr",
    "cz",
    "de",
    "dk",
    "do",
    "dz",
    "ec",
    "eg",
    "ee",
    "es",
    "fi",
    "fr",
    "gb",
    "gh",
    "gr",
    "gt",
    "hk",
    "hr",
    "hu",
    "id",
    "ie",
    "il",
    "in",
    "it",
    "jp",
    "ke",
    "kr",
    "kw",
    "kz",
    "lv",
    "lb",
    "lk",
    "lt",
    "lu",
    "mg",
    "mo",
    "mx",
    "my",
    "ni",
    "ng",
    "nl",
    "no",
    "nz",
    "om",
    "pa",
    "py",
    "pe",
    "ph",
    "pk",
    "pl",
    "pt",
    "qa",
    "ro",
    "ru",
    "sa",
    "se",
    "sg",
    "si",
    "sk",
    "sv",
    "th",
    "tn",
    "tr",
    "tw",
    "ua",
    "us",
    "uy",
    "uz",
    "ve",
    "vn",
    "za",
]


def find_apps(query, storefront="us"):
    response = web.get(
        "http://itunes.apple.com/search?",
        params={"term": query, "entity": "software", "country": storefront, "limit": 9},
    )
    if response.status_code == 200:
        return [
            {
                "app_name": item["trackName"],
                "developer_name": item["sellerName"],
                "app_id": item["trackId"],
                "bundle_id": item["bundleId"],
            }
            for item in response.json()["results"]
        ]
    else:
        return []


def add_item_app(wf, app, info="app_id"):
    wf.add_item(app["app_name"], app["developer_name"], valid=True, arg=app[info])


def main(wf):
    query = wf.args[0]
    args = query.split(" ")

    if len(args) > 1 and args[0] in ["id", "bundle"]:
        info = {"id": "app_id", "bundle": "bundle_id"}[args.pop(0)]
    else:
        info = "app_id"

    if len(args) > 1 and args[-1].lower() in storefront_list:
        storefront = args.pop(-1).lower()
    else:
        storefront = "us"
    query = " ".join(args)

    apps_list = find_apps(query, storefront)
    if not apps_list:
        wf.add_item("No results", "No apps found for " + query)
    else:
        for app in apps_list:
            add_item_app(wf, app, info=info)

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(
        update_settings={
            'github_slug': 'pinuz95/alfred-app-store-finder',
            'frequency': 1
        }
    )

    if wf.update_available:
        wf.add_item(
            'New version available',
            'Click here to install the update',
            autocomplete='workflow:update',
        )

    sys.exit(wf.run(main))
