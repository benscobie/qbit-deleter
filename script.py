import qbittorrentapi
import time
from args import parse

unregistered_torrent_messages = ['Unregistered torrent']


def main():
    args = parse()

    qbt_client = qbittorrentapi.Client(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )

    try:
        qbt_client.auth_log_in()
        print('Login successful')
    except qbittorrentapi.LoginFailed as e:
        print(e)
        exit(1)

    if args.runonce:
        check_torrents(qbt_client, args)
        exit(0)
    else:
        while True:
            check_torrents(qbt_client, args)
            print(f'Sleeping for {args.sleep} seconds')
            time.sleep(args.sleep)


def check_torrents(qbt_client, args):
    torrent_disk_space = 0

    for torrent in qbt_client.torrents_info(sort='added_on'):
        torrent_disk_space += torrent.total_size

    if args.disklimit:
        print(f'Disk space used: {torrent_disk_space / 1000000000} GB / {args.disklimit / 1000000000} GB')

    if args.disklimit == 0 or torrent_disk_space > args.disklimit:
        for torrent in qbt_client.torrents_info(sort='added_on', tag=args.tag):
            if torrent_applicable_for_deletion(torrent, qbt_client, args):
                print(f'Deleting torrent: {torrent.name}')
                if not args.dryrun:
                    qbt_client.torrents_delete(delete_files=args.deletefiles, torrent_hashes=torrent.hash)
                torrent_disk_space -= torrent.total_size

                if args.disklimit > 0 and torrent_disk_space <= args.disklimit:
                    break

    if args.deleteunregistered:
        for torrent in qbt_client.torrents_info():
            trackers = [i for i in torrent.trackers if i.url.startswith('http')]

            if len(trackers) == 0:
                continue

            can_be_deleted = True
            for tracker in trackers:
                if tracker.status != 4 or not any(ele in tracker.msg for ele in unregistered_torrent_messages):
                    can_be_deleted = False
                    break

            if can_be_deleted:
                print(f'Deleting torrent as unregistered: {torrent.name}')
                if not args.dryrun:
                    qbt_client.torrents_delete(delete_files=args.deletefiles, torrent_hashes=torrent.hash)


def torrent_applicable_for_deletion(torrent, qbt_client, args):
    if args.ratio and torrent.ratio >= args.ratio:
        print(f'Enough ratio to delete: {torrent.name}')
        return True

    if args.seedduration:
        min_seed_time = args.seedduration
    else:
        files = qbt_client.torrents_files(torrent.hash)

        if len(files) > 1:
            min_seed_time = args.collectionseedduration
        else:
            min_seed_time = args.singleseedduration

    if min_seed_time and torrent.seeding_time > min_seed_time:
        print(f'Enough seeding time to delete: {torrent.name}')
        return True

    return False


if __name__ == "__main__":
    main()
