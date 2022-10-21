# qBittorrent Deleter

![License MIT](https://img.shields.io/badge/license-MIT-blue.svg) [![](https://img.shields.io/docker/pulls/benscobie/qbit-deleter.svg)](https://hub.docker.com/r/benscobie/qbit-deleter 'DockerHub')

## Overview

Automatically deletes torrents in qBittorrent based on various conditions such as ratio, seed time and disk usage.

## Features

- Can be configured to delete torrents when:
  - A specified disk limit has been reached.
  - A specified ratio has been reached.
  - A specified seed duration has been reached, separate arguments are available for single file torrents and multi file torrents.
  - All trackers are reporting that the torrent is no longer registered.
- Configure whether to delete files on disk as well as the torrent.
- Can be run once or indefinitely.
- Includes a dry run mode so that you can see what it will do.

## Usage

### Docker Compose

```yml
services:
  qbit-deleter:
    container_name: qbit-deleter
    image: benscobie/qbit-deleter:latest
    environment:
      - QBIT_HOST=example.com
      - QBIT_PORT=54000
      - QBIT_USERNAME=admin
      - QBIT_PASSWORD=mypassword
      - QBIT_SEED_RATIO=1.0
      - QBIT_SINGLE_SEED_DURATION=86400
      - QBIT_COLLECTION_SEED_DURATION=604800
      - QBIT_DISK_LIMIT_BYTES=1000000000000
      - QBIT_SLEEP_DURATION=120
      - QBIT_DELETE_FILES=1
      - QBIT_DELETE_UNREGISTERED=1
```

See the [Arguments section](#arguments) for a full list of available environment variables.

### Command line

Clone the repository and run:
```commandline
pip install -r requirements.txt
./script.py --host example.com --port 54000 --username admin --password password
```

## Arguments

It's important to note that currently when a disk limit is specified, torrents meeting any ratio or seeding duration will only be deleted once the disk limit has been breached, in which case the oldest torrent meeting the condition(s) is deleted first.

| Description                                                                                                                | CLI                             | Environment Variable          | Default      |
|:---------------------------------------------------------------------------------------------------------------------------|:--------------------------------|-------------------------------|:-------------|
| Set the host for qBittorrent.                                                                                              | -ho --host                      | QBIT_HOST                     |              |
| Set the port for qBittorrent.                                                                                              | -po --port                      | QBIT_PORT                     | 8080         |
| Set the username for qBittorrent.                                                                                          | -u --username                   | QBIT_USERNAME                 |              |
| Set the password for qBittorrent.                                                                                          | -p --password                   | QBIT_PASSWORD                 |              |
| Enable dry run mode. Does not delete torrents, just prints what it will do.                                                | -d --dryrun                     | QBIT_DRY_RUN                  | False        | 
| Run once instead of forever.                                                                                               | -ro --runonce                   | QBIT_RUN_ONCE                 | False        |
| How long to sleep between runs, only relevant if not running once.                                                         | -s --sleep                      | QBIT_SLEEP_DURATION           | 30           |
| Disk limit in bytes as a delete condition. Disk usage is calculated by adding up the size of each torrent.                 | -dl --disklimit                 | QBIT_DISK_LIMIT_BYTES         | 0 (no limit) |
| Ratio a torrent should reach before deletion.                                                                              | -r --ratio                      | QBIT_SEED_RATIO               | 0 (no limit) |
| How long a torrent should be seeded for in seconds before deletion. Takes precedence over single and multi file durations. | -seed --seedduration            | QBIT_SEED_DURATION            | 0 (no limit) |
| How long a single file torrent should be seeded for in seconds before deletion.                                            | -sseed --singleseedduration     | QBIT_SINGLE_SEED_DURATION     | 0 (no limit) |
| How long a multi file torrent should be seeded for in seconds before deletion.                                             | -cseed --collectionseedduration | QBIT_COLLECTION_SEED_DURATION | 0 (no limit) |
| Enable deletion of files on disk as well as the torrent.                                                                   | -df --deletefiles               | QBIT_DELETE_FILES             | False        |
| Enable deletion of unregistered torrents, all trackers need to report unregistered.                                        | -du --deleteunregistered        | QBIT_DELETE_UNREGISTERED      | False        |

Running the following will also print the available arguments:

```commandline
./script.py --help
```

## Contributing

Pull requests are welcomed. If you would like to introduce a completely new feature, please open an issue in the first instance so that we can discuss the suitability and any implementation details.

## License

[MIT License](LICENSE)