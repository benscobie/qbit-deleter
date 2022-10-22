import argparse
import os
from envdefault import EnvDefault


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ho", "--host", action=EnvDefault, required=True, envvar='QBIT_HOST',
        help="Specify the qBittorrent host (can also be specified using QBIT_HOST environment variable)")
    parser.add_argument(
        "-po", "--port", action=EnvDefault, type=int, default=8080, envvar='QBIT_PORT',
        help="Specify the qBittorrent port (can also be specified using QBIT_PORT environment variable)")
    parser.add_argument(
        "-u", "--username", action=EnvDefault, envvar='QBIT_USERNAME',
        help="Specify the qBittorrent username (can also be specified using QBIT_USERNAME environment variable)")
    parser.add_argument(
        "-p", "--password", action=EnvDefault, envvar='QBIT_PASSWORD',
        help="Specify the qBittorrent password (can also be specified using QBIT_PASSWORD environment variable)")
    parser.add_argument(
        "-d", "--dryrun", action='store_true', default=None,
        help="Specify to not delete torrents (can also be specified using QBIT_DRY_RUN environment variable)")
    parser.add_argument(
        "-dl", "--disklimit", action=EnvDefault, type=int, required=False, default=0, envvar='QBIT_DISK_LIMIT_BYTES',
        help="Specify a disk limit in bytes as a delete condition (can also be specified using QBIT_DISK_LIMIT_BYTES environment variable)")
    parser.add_argument(
        "-s", "--sleep", action=EnvDefault, type=int, default=30, envvar='QBIT_SLEEP_DURATION',
        help="Specify how long to sleep between runs, only relevant if --runonce is FALSE (can also be specified using QBIT_SLEEP_DURATION environment variable)")
    parser.add_argument(
        "-ro", "--runonce", action='store_true', default=None,
        help="Specify to run once instead of forever (can also be specified using QBIT_RUN_ONCE environment variable)")
    parser.add_argument(
        "-seed", "--seedduration", action=EnvDefault, type=int, required=False, default=0, envvar='QBIT_SEED_DURATION',
        help="Specify how long a torrent should be seeded for in seconds before deletion (can also be specified using QBIT_SEED_DURATION environment variable)")
    parser.add_argument(
        "-r", "--ratio", action=EnvDefault, type=float, required=False, default=0, envvar='QBIT_SEED_RATIO',
        help="Specify a ratio a torrent should reach before deletion (can also be specified using QBIT_SEED_RATIO environment variable)")
    parser.add_argument(
        "-sseed", "--singleseedduration", action=EnvDefault, type=int, required=False, default=0,
        envvar='QBIT_SINGLE_SEED_DURATION',
        help="Specify how long a single file torrent should be seeded for in seconds before deletion (can also be specified using QBIT_SINGLE_SEED_DURATION environment variable)")
    parser.add_argument(
        "-cseed", "--collectionseedduration", action=EnvDefault, type=int, required=False, default=0,
        envvar='QBIT_COLLECTION_SEED_DURATION',
        help="Specify how long a multi file torrent should be seeded for in seconds before deletion (can also be specified using QBIT_COLLECTION_SEED_DURATION environment variable)")
    parser.add_argument(
        "-df", "--deletefiles", action='store_true', default=None,
        help="Specify to delete files on disk as well as the torrent (can also be specified using QBIT_DELETE_FILES environment variable)")
    parser.add_argument(
        "-du", "--deleteunregistered", action='store_true', default=None,
        help="Specify to delete unregistered torrents (all trackers need to report unregistered) (can also be specified using QBIT_DELETE_UNREGISTERED environment variable)")
    args = parser.parse_args()

    if args.runonce is None:
        if 'QBIT_RUN_ONCE' in os.environ:
            args.runonce = True
        else:
            args.runonce = False

    if args.dryrun is None:
        if 'QBIT_DRY_RUN' in os.environ:
            args.dryrun = True
        else:
            args.dryrun = False

    if args.deletefiles is None:
        if 'QBIT_DELETE_FILES' in os.environ:
            args.deletefiles = True
        else:
            args.deletefiles = False

    if args.deleteunregistered is None:
        if 'QBIT_DELETE_UNREGISTERED' in os.environ:
            args.deleteunregistered = True
        else:
            args.deleteunregistered = False

    return args
