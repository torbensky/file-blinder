# blind.py

A general-purpose, simple utility for blinding files. Intended to help researchers who need to analyse files without introducing bias from knowing which particular dataset they are processing.

# Running

## Blind files sharing the same "grouping prefix"

For any file type (same as `--fileType "*"`)

`python blind.py ./sample-data/prefix-group group-by-prefix`

For a specific file type (only `.tif` files)

`python blind.py ./sample-data/prefix-group group-by-prefix --fileType tif`

## Blind all files in the specified directory

For any file type (same as `--fileType "*"`)

`python blind.py ./sample-data/all-files all-files-in-dir`

For a specific file type (only `.nd2` files)

`python blind.py ./sample-data/all-files all-files-in-dir --fileType nd2`
