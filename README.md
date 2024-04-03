# `bridge`

Have you ever needed to clone a repo to a server, but `scp` and `git clone` were not an option?

Unlikely, I know. But I have. And `bridge` is now my best friend.

## Usage

1. Change `main.py`. Add your `exclusions` and your `origin_path`
```python
if __name__ == "__main__":
    exclusions: list[str] = [
        r'.*\.git.*',
        r'.*\.md',
    ]                       # Add pattens to exclude files from copy
    origin_path = Path("")
    clone(origin_path, exclusions)
```

2. Copy the contents of `bridge.py` to the server

3. Make it executable and run!
```commandline
chmod +x bridge.py
./bridge.py
```
