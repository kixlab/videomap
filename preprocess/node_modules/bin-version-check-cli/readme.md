# bin-version-check-cli [![Build Status](https://travis-ci.org/sindresorhus/bin-version-check-cli.svg?branch=master)](https://travis-ci.org/sindresorhus/bin-version-check-cli)

> Check whether a binary version satisfies a [semver range](https://github.com/npm/node-semver#ranges)

Useful when you have a thing that only works with specific versions of a binary.


## Install

```
$ npm install --global bin-version-check-cli
```


## Usage

```
$ bin-version-check --help

  Usage
    $ bin-version-check <binary> <semver-range>

  Options
    --args  CLI args to get binary version (Can be set multiple times) [Default: --version]

  Example
    $ curl --version
    curl 7.30.0 (x86_64-apple-darwin13.0)
    $ bin-version-check curl '>=8'
    curl 7.30.0 doesn't satisfy the version requirement of >=8

  Exits with code 0 if the semver range is satisfied and 1 if not
```


## Related

- [bin-version-check](https://github.com/sindresorhus/bin-version-check) - API for this module


## License

MIT © [Sindre Sorhus](https://sindresorhus.com)
