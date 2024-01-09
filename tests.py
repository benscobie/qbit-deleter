from unittest.mock import MagicMock, Mock, patch, call
import unittest
from script import check_torrents
from script import torrent_applicable_for_deletion

class TestQbitDeleter(unittest.TestCase):

    @patch("script.shutil.disk_usage")
    @patch('script.torrent_applicable_for_deletion')
    def test_disk_limit_reached_deletes_appropriate_torrents(self, mock_torrent_applicable_for_deletion, mock_shutil_disk_usage):
        mock_torrent_applicable_for_deletion.return_value = True
        mock_shutil_disk_usage.return_value.free = 500

        torrent1 = MagicMock(name='Torrent 1', total_size=1000, hash='hash1')
        torrent2 = MagicMock(name='Torrent 2', total_size=1000, hash='hash2')
        torrent3 = MagicMock(name='Torrent 3', total_size=400, hash='hash3')

        qbt_client_mock = MagicMock()
        qbt_client_mock.torrents_info = MagicMock(return_value=[torrent1, torrent2, torrent3])
        args = Mock()
        args.freespace = 2000
        args.freespacepath = '/'
        args.dryrun = False
        args.deletefiles = True
        args.deleteunregistered = False

        check_torrents(qbt_client_mock, args)

        self.assertEqual(qbt_client_mock.torrents_delete.call_count, 2)
        qbt_client_mock.torrents_delete.assert_has_calls([call(delete_files=True, torrent_hashes='hash1'), call(delete_files=True, torrent_hashes='hash2')])

    def test_enough_ratio_is_applicable_for_deletion(self):
        torrent = MagicMock(name='Torrent', total_size=1000, ratio=1, hash='hash')
        qbt_client_mock = MagicMock()

        args = Mock()
        args.ratio = 1

        result = torrent_applicable_for_deletion(torrent, qbt_client_mock, args)

        self.assertEqual(result, True)

    def test_enough_seed_time_is_applicable_for_deletion(self):
        torrent = MagicMock(name='Torrent', ratio=0.5, hash='hash', seeding_time=9999)
        qbt_client_mock = MagicMock()
        args = Mock()
        args.ratio = 1
        args.seedduration = 1000

        result = torrent_applicable_for_deletion(torrent, qbt_client_mock, args)

        self.assertEqual(result, True)

    def test_single_file_enough_seed_time_is_applicable_for_deletion(self):
        torrent = MagicMock(name='Torrent', ratio=0.5, hash='hash', seeding_time=9999)
        qbt_client_mock = MagicMock()

        args = Mock()
        args.ratio = 1
        args.seedduration = 0
        args.singleseedduration = 1000

        qbt_client_mock.torrents_files = Mock(return_value=[1])

        result = torrent_applicable_for_deletion(torrent, qbt_client_mock, args)

        self.assertEqual(result, True)

    def test_multi_file_enough_seed_time_is_applicable_for_deletion(self):
        torrent = MagicMock(name='Torrent', ratio=0.5, hash='hash', seeding_time=9999)
        qbt_client_mock = MagicMock()

        args = Mock()
        args.ratio = 1
        args.seedduration = 0
        args.collectionseedduration = 1000

        qbt_client_mock.torrents_files = Mock(return_value=[1,2])

        result = torrent_applicable_for_deletion(torrent, qbt_client_mock, args)

        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()