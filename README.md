# teeheesmart

Python library for controlling a [TESmart][tesmart] media switch over a TCP
connection using their un-named [Hex protocol][hex].

It's primarily intended for use as a device driver for a [Home Assistant][ha]
integration.

## USAGE

```py
from teeheesmart import get_media_switch

device_url = '10.0.0.1'
media_switch = get_media_switch(device_url)

media_switch.select_source(3) # Change to input 3
media_switch.update() # Refreshes device state
```

See `src/teeheesmart/media_switch.py` for full `MediaSwitch` capabilities.

### Device URL format

The URL takes the form of `<scheme>://<host>:<port>#<protocol>` with all
but `host` being optional.

Default scheme is `tcp`, with a default port of `5000`.

Default protocol is Hex (identifier: `hex`.)

Examples:

+ `10.0.0.1` ->
  Scheme: `tcp`, Host: `10.0.0.1`, Port: `5000`, Protocol: `hex`
+ `localhost:1337` ->
  Scheme: `tcp`, Host: `localhost`, Port: `1337`, Protocol: `hex`
+ `localhost:1337#hex` ->
  Scheme: `tcp`, Host: `localhost`, Port: `1337`, Protocol: `hex`
+ `tcp://10.0.0.1` ->
  Scheme: `tcp`, Host: `10.0.0.1`, Port: `5000`, Protocol: `hex`
+ `tcp://switch.local:8080` ->
  Scheme: `tcp`, Host: `switch.local`, Port: `8080`, Protocol: `hex`

## Limitations

The library was tested and developed using a TESmart [HSW-1601][hsw1601], but
_should_ work for any TESmart switch using their [Hex protocol][hex].

It does _not_ currently support:

+ _Matrix_ switch operations, since I don't have a device to test with
+ Serial communication, since TCP is the more likely control mechanism for home
automation purposes

The library has extension points for adding the support above should an
opportunity or need to do so arise.

## Development workflow

### Python environment

Workflow scripts assume a working Python environment, including `pip`.

Remember to be kind to yourself and use a virtual environment.

```sh
python3 -m venv env
env/bin/activate
```

### Setup

Install development and runtime dependencies. This also installs the library as an
editable path, so that it can be loaded in the REPL and `pytest`.

```sh
script/setup
```

### Tests

Run unit tests:

```sh
script/test
```

Tests can also be continuously run while developing with:

```sh
ptw .
```

### Build

To build distributables:

```sh
script/build
```

Build artifacts will be placed in the `dist` directory.

### Publishing

Build the distribution.

```sh
script/build
```

Publish the library to TestPyPI.

```sh
script/publish_test
```

Publish the library to PyPI.

```sh
script/publish
```

[ha]: https://www.home-assistant.io/
[tesmart]: https://www.tesmart.com/
[hex]: https://support.tesmart.com/hc/en-us/article_attachments/10269851662361
[hsw1601]: https://www.tesmart.com/collections/hdmi-switch/products/hsw1601-e23
