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


def find_app_from_id(app_id):
    headers = {
        "authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNSRjVITkJHUFEifQ.eyJpc3MiOiI4Q1UyNk1LTFM0IiwiaWF0IjoxNjAwMzkxOTgyLCJleHAiOjE2MDM0MTU5ODJ9.L7n44RSJSFL60iVnOn6PkrCbpZG8kKTvQ_buZ7plIcSZQwTHYZdJSTiRzN8F9vEINC61aD1ahAs8dKzZtbwD9A",
    }

    params = dict(
        [
            ("platform", "web"),
            ("additionalPlatforms", "appletv,ipad,iphone,mac"),
            (
                "extend",
                "description,developerInfo,editorialVideo,eula,fileSizeByDevice,messagesScreenshots,privacyPolicyUrl,privacyPolicyText,promotionalText,screenshotsByType,supportURLForLanguage,versionHistory,videoPreviewsByType,websiteUrl",
            ),
            (
                "include",
                "genres,developer,reviews,merchandised-in-apps,customers-also-bought-apps,developer-other-apps,app-bundles,top-in-apps,eula",
            ),
            ("l", "en-gb"),
        ]
    )

    response = web.get(
        "https://amp-api.apps.apple.com/v1/catalog/SA/apps/" + str(app_id),
        headers=headers,
        params=params,
    )

    if response.status_code == 200:
        data = response.json()["data"][0]["attributes"]
        return {
            "app_name": data["name"],
            "developer_name": data["artistName"],
            "app_id": app_id,
            "bundle_id": data["platformAttributes"]["ios"]["bundleId"],
        }
    else:
        return None


def find_apps_from_token(token, storefront="us"):
    response = web.get(
        "http://itunes.apple.com/search?",
        params={"term": token, "entity": "software", "country": storefront, "limit": 9},
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
        return None


def add_item_app(wf, app, info="app_id"):
    wf.add_item(app["app_name"], app["developer_name"], valid=True, arg=app[info])


def main(wf):
    query = wf.args[0]
    args = query.split(" ")

    if len(args) > 1 and args[0] in ["id", "bundle"]:
        info = {"id": "app_id", "bundle": "bundle_id"}[args[0]]
        args = args[1:]
    else:
        info = "app_id"

    is_app_id = False
    if len(args) == 1 and len(args[0]) in (9, 10):
        try:
            int(args[0])
            is_app_id = True
        except:
            pass

    if is_app_id:
        app = find_app_from_id(args[0])

        if app is None:
            wf.add_item("No results", "No app found for ID " + query)
        else:
            add_item_app(wf, app, info=info)
    else:
        if len(args) > 1 and args[-1].lower() in storefront_list:
            storefront = args[-1]
            token = " ".join(args[:-1])
        else:
            storefront = "us"
            token = " ".join(args)

        apps_list = find_apps_from_token(token, storefront)
        if apps_list is None:
            wf.add_item("No results", "No app found for token " + token)
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
