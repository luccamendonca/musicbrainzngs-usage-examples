import csv
import argparse
import multiprocessing
from re import search

import musicbrainzngs

musicbrainzngs.set_useragent("python", "3.X")

PARSER = argparse.ArgumentParser(
    description="gets the earliest release date from each album on a CSV file and generates a new CSV file containing the release year"
)
PARSER.add_argument(
    "-i", dest="input_file", type=str, default="albums.csv", help="The input file path"
)
PARSER.add_argument(
    "-m",
    dest="multiprocessing_enabled",
    action="store_true",
    default=False,
    help="Enable multiprocessing",
)
PARSER.add_argument(
    "-o",
    dest="output_file",
    type=str,
    default="albums_with_release_dates.csv",
    help="The output file path",
)
PARSER.add_argument("-v", action="store_true", dest="verbose", help="Show verbose logs")
ARGS = PARSER.parse_args()


def release_get_year(search_params={}):
    artist = search_params.get("artist", "")
    album = search_params.get("album", "")
    if ARGS.verbose:
        print(f"\nStarting request to musicbrainz")
    release = musicbrainzngs.search_releases(
        artist=artist,
        release=album,
        limit=1,
    )
    release_count = release.get("release-count", 0)
    release_list = release.get("release-list", [])
    if ARGS.verbose:
        print(f"Search for '{artist} - {album}' returned {release_count} results.")

    earliest_release_year = str(
        min([int(r.get("date", "0000-00-00")[:4]) for r in release_list])
    )

    return {
        "artist": artist,
        "album": album,
        "earliest_release": earliest_release_year,
    }


def generate_output_csv(release_list=[]):
    keys = release_list.pop().keys()
    with open(ARGS.output_file, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(release_list)


if __name__ == "__main__":
    print(
        f"""
    RELEASE DATE FINDER

    This script searches releases for a given a `artist,album` CSV
    and outputs another CSV to the path specified in the following format:
    `artist,album,earliest_release`

    Input file: {ARGS.input_file}
    Output file: {ARGS.output_file}
    Verbose output: {ARGS.verbose}
    """
    )

    csv_reader = csv.DictReader(open(ARGS.input_file, mode="r", encoding="utf-8-sig"))
    album_list = [row for row in csv_reader]
    releases_with_years = []

    if ARGS.verbose:
        print(f"Found {len(album_list)} albums on the input CSV.")

    if ARGS.multiprocessing_enabled:
        cpu_count = multiprocessing.cpu_count()
        with multiprocessing.Pool(cpu_count) as pool:
            if ARGS.verbose:
                print(f"Starting process pool with {cpu_count} CPUs")
            releases_with_years = pool.map(release_get_year, album_list)
    else:
        releases_with_years = [release_get_year(row) for row in album_list]

    generate_output_csv(releases_with_years)
