import shutil
import qbittorrentapi
import time
from args import parse
from util import is_tag_in_torrent

unregistered_torrent_messages = ["Unregistered torrent"]


def main():
    args = parse()

    qbt_client = qbittorrentapi.Client(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        VERIFY_WEBUI_CERTIFICATE=False,
        REQUESTS_ARGS={"timeout": (45, 60)},
    )

    try:
        qbt_client.auth_log_in()
        print("Login successful")
    except qbittorrentapi.LoginFailed as e:
        print("Failed to login. Invalid username/password.")
        exit(1)
    except Exception as e:
        print(e)
        exit(2)

    if args.runonce:
        check_torrents(qbt_client, args)
        exit(0)
    else:
        while True:
            check_torrents(qbt_client, args)
            print(f"Sleeping for {args.sleep} seconds")
            time.sleep(args.sleep)


def check_torrents(qbt_client, args):
    free_disk_space = shutil.disk_usage(args.freespacepath).free

    if args.freespace == 0 or free_disk_space < args.freespace:
        for torrent in qbt_client.torrents_info(
            sort="num_complete", reverse=True, tag=args.tag
        ):
            if torrent_applicable_for_deletion(torrent, qbt_client, args):
                print(f"Deleting torrent: {torrent.name}")
                if not args.dryrun:
                    qbt_client.torrents_delete(
                        delete_files=args.deletefiles, torrent_hashes=torrent.hash
                    )
                free_disk_space += torrent.total_size

                if args.freespace > 0 and free_disk_space >= args.freespace:
                    break

    if args.deleteunregistered:
        for torrent in qbt_client.torrents_info():
            trackers = [i for i in torrent.trackers if i.url.startswith("http")]

            if len(trackers) == 0:
                continue

            can_be_deleted = True
            for tracker in trackers:
                if (
                    tracker.status != qbittorrentapi.TrackerStatus.NOT_WORKING
                    or not any(
                        ele in tracker.msg for ele in unregistered_torrent_messages
                    )
                ):
                    can_be_deleted = False
                    break

            if can_be_deleted:
                print(f"Deleting torrent as unregistered: {torrent.name}")
                if not args.dryrun:
                    qbt_client.torrents_delete(
                        delete_files=args.deletefiles, torrent_hashes=torrent.hash
                    )


def torrent_applicable_for_deletion(torrent, qbt_client, args):
    if args.excludetag and is_tag_in_torrent(args.excludetag, torrent.tags):
        return False

    if args.restrict_to_working:
        trackers = [i for i in torrent.trackers if i.url.startswith("http")]

        tracker_working = False
        for tracker in trackers:
            if tracker.status == qbittorrentapi.TrackerStatus.WORKING or (
                tracker.status == qbittorrentapi.TrackerStatus.NOT_WORKING
                and any(ele in tracker.msg for ele in unregistered_torrent_messages)
            ):
                tracker_working = True
                break

        if len(trackers) > 0 and not tracker_working:
            return False

    if args.ratio and torrent.ratio >= args.ratio:
        print(f"Enough ratio to delete: {torrent.name}")
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
        print(f"Enough seeding time to delete: {torrent.name}")
        return True

    return False


if __name__ == "__main__":
    main()
