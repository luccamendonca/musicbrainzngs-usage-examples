# Musicbrainz API script collection (?)

For now there's only one script that's responsible for fetching the earliest release year for a given `artist,album` list (provided as a CSV).
Use the `example_input.csv` as an, er... example?

## Running the script

> Python3 is mandatory (of course).

```
$ python3 -m pip install -r requirements.txt
```

```
$ python3 ./get-earliest-release.py -i my-input-file.csv -o my-output-file.csv -v
```

