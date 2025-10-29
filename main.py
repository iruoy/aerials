import json
import os
import urllib.request
from typing import TypedDict, NotRequired, cast


class Source(TypedDict):
    name: str
    description: str
    license: str
    scenes: list[str]
    manifestUrl: str
    local: bool
    cacheable: bool


class Manifest(TypedDict):
    sources: list[Source]


# Can't be handled the same way as Source, Manifest and Entries
# because it contains keys with hyphens
Asset = TypedDict(
    "Asset",
    {
        "scene": str,
        "url-1080-H264": str,
        "accessibilityLabel": str,
        "id": str,
        "title": str,
        "url-4K-SDR": str,
        "timeOfDay": str,
        "url-1080-SDR": str,
        "pointsOfInterest": NotRequired[dict[str, str]],
    },
)


class Entries(TypedDict):
    assets: list[Asset]


def get_manifest() -> Manifest:
    with open("manifest.json", "r") as file:
        return cast(Manifest, json.load(file))


def get_entries(path: str, source: Source) -> Entries:
    file_path = os.path.join(path, "entries.json")
    if not os.path.exists(file_path):
        os.makedirs(path, exist_ok=True)
        _ = urllib.request.urlretrieve(source["manifestUrl"], file_path)

    with open(file_path, "r") as file:
        return cast(Entries, json.load(file))


def main():
    path = "clips"
    manifest = get_manifest()

    for source in manifest["sources"]:
        source_path = os.path.join(path, source["name"])
        entries = get_entries(source_path, source)

        for asset in entries["assets"]:
            asset_path = os.path.join(source_path, asset["id"] + ".4k-sdr.mov")
            print(f"Downloading {asset['url-4K-SDR']} to {asset_path}")
            _ = urllib.request.urlretrieve(asset["url-4K-SDR"], asset_path)


if __name__ == "__main__":
    main()
