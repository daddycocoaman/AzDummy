# `azdummy`

**Usage**:

```console
$ azdummy [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --verbose`: [default: False]
* `--timer`: Print execution time after output  [default: False]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `config`: Show or edit configuration data
* `gen`: Generate fake data for specified type
---
## `azdummy config`

Show or edit configuration data

**Usage**:

```console
$ azdummy config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `launch`: Opens the configuration file in default...
* `reset`: Reset the configuration to default.
* `set`: Set a configuration key/value pair.
* `show`: Show the configuration.

### `azdummy config launch`

Opens the configuration file in default editor

**Usage**:

```console
$ azdummy config launch [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `azdummy config reset`

Reset the configuration to default.

**Usage**:

```console
$ azdummy config reset [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `azdummy config set`

Set a configuration key/value pair.

**Usage**:

```console
$ azdummy config set [OPTIONS] KEY VALUE
```

**Arguments**:

* `KEY`: Key to set. Must exist in config.  [required]
* `VALUE`: Value to set for key.  [required]

**Options**:

* `--help`: Show this message and exit.

### `azdummy config show`

Show the configuration.

By default, does not show secrets. If using --verbose, secrets will be shown in plaintext.

**Usage**:

```console
$ azdummy config show [OPTIONS]
```

**Options**:

* `--types`: Show expected field types for configuration  [default: False]
* `--help`: Show this message and exit.

---
## `azdummy gen`

Generate fake data for specified type

**Usage**:

```console
$ azdummy gen [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `users`: Generate fake user data.

### `azdummy gen users`

Generate fake user data.

The output format determines which fields are generated. By default, this will
generate output to the console with the fields that can be uploaded directly
to Azure Portal.

CSV format will output two CSVs: one for bulk create and one for bulk delete.

JSON format will output to console fields that can used to create objects
directly via Microsoft Graph REST API.

**Usage**:

```console
$ azdummy gen users [OPTIONS]
```

**Options**:

* `--tenant TEXT`: Tenant name  [default: azdummy.onmicrosoft.com]
* `--count INTEGER RANGE`: Number of users to generate. Max 50000.  [default: 500]
* `--format [console|csv|json]`: Format for output.  [default: console]
* `-b, --block-login`: Prevent generated users from logging in  [default: False]
* `--output-file FILENAME`: File to output. Extension not required.  [default: output]
* `--help`: Show this message and exit.

