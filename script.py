import qbittorrentapi
import time
import argparse
from envdefault import EnvDefault

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
    "-d", "--dryrun", action=EnvDefault, required=False, default=False, envvar='QBIT_DRY_RUN',
    help="Specify whether to actually delete torrents or not (can also be specified using QBIT_DRY_RUN environment variable)")
parser.add_argument(
    "-dl", "--disklimit", action=EnvDefault, type=int, required=False, default=0, envvar='QBIT_DISK_LIMIT_BYTES',
    help="Specify a disk limit in bytes as a delete condition (can also be specified using QBIT_DISK_LIMIT_BYTES environment variable)")
parser.add_argument(
    "-s", "--sleep", action=EnvDefault, type=int, default=30, envvar='QBIT_SLEEP_DURATION',
    help="Specify how long to sleep between runs, only relevant if --runonce is FALSE (can also be specified using QBIT_SLEEP_DURATION environment variable)")
parser.add_argument(
    "-ro", "--runonce", action=EnvDefault, type=bool, required=False, default=False, envvar='QBIT_RUN_ONCE',
    help="Specify whether to run once or forever (can also be specified using QBIT_RUN_ONCE environment variable)")
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
    "-df", "--deletefiles", action=EnvDefault, type=bool, required=True, default=False, envvar='QBIT_DELETE_FILES',
    help="Specify whether to delete files or just the torrent on deletion (can also be specified using QBIT_DELETE_FILES environment variable)")
args = parser.parse_args()

qbt_client = qbittorrentapi.Client(
    host=args.host,
    port=args.port,
    username=args.username,
    password=args.password
)


def main():
    try:
        qbt_client.auth_log_in()
        print("Login successful")
    except qbittorrentapi.LoginFailed as e:
        print(e)

    if args.runonce:
        check_torrents()
        exit(0)
    else:
        while True:
            check_torrents()
            print(f'Sleeping for {args.sleep} seconds')
            time.sleep(args.sleep)


def check_torrents():
    torrents = []
    torrent_disk_space = 0

    for torrent in qbt_client.torrents_info(sort='added_on'):
        torrents.append(torrent);
        torrent_disk_space += torrent.total_size

    if args.disklimit:
        print(f'Disk space used: {torrent_disk_space / 1000000000} GB / {args.disklimit / 1000000000} GB')

    if args.disklimit == 0 or torrent_disk_space > args.disklimit:
        for torrent in torrents:
            if torrent_applicable_for_deletion(torrent):
                print(f'Deleting torrent: {torrent.name}')
                if not args.dryrun:
                    qbt_client.torrents_delete(delete_files=args.deletefiles, torrent_hashes=torrent.hash)
                torrent_disk_space -= torrent.total_size

                if args.disklimit > 0 and torrent_disk_space <= args.disklimit:
                    break


def torrent_applicable_for_deletion(torrent):
    if args.ratio and torrent.ratio >= args.ratio:
        print(f'Enough ratio to delete: {torrent.name}')
        return True

    if args.seedduration:
        min_seed_time = args.seedduration
    else:
        files = qbt_client.torrents_files(torrent.hash)

        if len(files) > 1:
            min_seed_time = args.singleseedduration
        else:
            min_seed_time = args.collectionseedduration

    if min_seed_time and torrent.seeding_time > min_seed_time:
        print(f'Enough seeding time to delete: {torrent.name}')
        return True

    return False


if __name__ == "__main__":
    main()
