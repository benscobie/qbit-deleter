def get_list(data):
    if data is None:
        return None
    elif isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return [data]
    else:
        return [d.strip() for d in str(data).split(",")]


def is_tag_in_torrent(check_tag, torrent_tags):
    tags = get_list(torrent_tags)
    return check_tag in tags
