# `bridge`

Have you ever needed to clone a repo to a server, but `scp` and `git clone` were not an option?

Unlikely, I know. But I have. And `bridge` is now my best friend.

## Usage

1. [OPTIONAL] Change `main.py`. Add your `exclusions`
```python
if __name__ == "__main__":
    exclusions: list[str] = [
        r'.*\.git.*',
        r'.*\.md',
    ]                       # Add pattens to exclude files from copy
    clone(origin_path, exclusions)
```

2. Run script, specifying the path with `-p [PATH]`
```bash
python3 ./main.py -p path/to/copy/from
```

3. Copy the contents of `bridge.py` to the server

4. Make it executable and run!
```bash
chmod +x bridge.py
./bridge.py
```
