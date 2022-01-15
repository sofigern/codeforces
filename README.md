# codeforces-client

Codeforces Client is a Python library and tooling for working with Codeforces.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install codeforces-client.

```bash
pip install codeforces-client
```
To configure default params like your codeforces handle or favorite programming language you can use:
```bash
cf-cli config
```
You can load all submissions you made to codeforces before with:
```bash
cf-cli load
```
Load could be specified with different params i.e. next command will load all submissions, including unsuccessful `tourist` made for the contest `2` in `delphi`. Please use `--help` for detailed info.
```bash
cf-cli load --handle=tourist --contest-id=2 --verdict=any --language=delphi
```

## Usage

```python
import codeforces_client as cf
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[gpl-3.0](LICENSE)