from utils.db_library import *
from datetime import datetime

""" 아티팩트 경로 입력 """
db_path = "CuratorAppData.DefaultAccount"
# com.android.providers.downloads
download_db = "downloads.db"
# com.android.providers.media.module
external_db = "external.db"

class NearbyShare():
    def __init__(self):
        self.version = 1.0
        self.nbu_list = []

    def _convert_unixtimestamp(self, timestamp):
        time = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        return time

    def transfer_data(self, path):
        with sqlite3.connect(path) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute("select * from 'Transaction'")
        return data.fetchall()

    def CuratorAppData(self, path):
        with sqlite3.connect(path) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute("select conversation_session_proto, person_id, session_id, first_created from conversation_table")
            data = data.fetchall()

            proto = str(data[0][0]).split('&')

            file =  '/storage' + proto[2].split('storage')[1].split('\\')[0]
            target_name =  proto[4].split('x12')[1][4:].split('\\')[0]
            time = self._convert_unixtimestamp(data[0][3])

            nearby_send = {
                'event': 'Send',
                'filepath': file, 'filename': file.split('/')[-1],
                'device_name': target_name,
                'description': None, 'time': time, 'filesize': None,
                'mimetype': None
            }

            self.nbu_list.append(nearby_send)


    def downloaded(self):
        with sqlite3.connect(download_db) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute(
                "select uri, _data, title, description, lastmod, total_bytes, mimetype from downloads")
            data = data.fetchall()

            file_list = []
            for index in data:
                if index[0] == 'non-dwnldmngr-download-dont-retry2download':

                    download_data = {
                        'event': 'Received',
                        'filepath': index[1], 'filename': index[2],
                        'device_name': None,
                        'description': index[3], 'time': self._convert_unixtimestamp(index[4]), 'filesize': index[5],
                        'mimetype': index[6]
                    }

                    self.nbu_list.append(download_data)
                    file_list.append(index[2])

       # return download_list
        # with sqlite3.connect(external_db) as db_connection:
        #     cur = db_connection.cursor()
        #     data2 = cur.execute(
        #         "select download_uri, date_modified, _display_name, mime_type, _data, _size, title  from downloads")
        #     data2 = data2.fetchall()
        #
        #     for index2 in data2:
        #         if index[2] not in file_list:
        #             if index2[0] == 'non-dwnldmngr-download-dont-retry2download':
        #
        #                 # download_data2 = {
        #                 #     'filepath': index[4], 'filename': index[2],
        #                 #     'description': index[3], 'time': self._convert_unixtimestamp(index[4]), 'filesize': index[5]
        #                 # }
        #
        #                 print('ws')


        # with sqlite3.connect(external_db) as db_connection:
        #     cur = db_connection.cursor()
        #     data = cur.execute(
        #         "select conversation_session_proto, person_id, session_id, first_created from downloads")
        #     data = data.fetchall()


def run(out_path):
    nbu = NearbyShare()
    conversation_data = nbu.CuratorAppData(db_path)
    download_data = nbu.downloaded()

    for total_index in nbu.nbu_list:
        total_index['service'] = 'Nearby Share'
        insert_total_sharing(total_index, out_path)

    return nbu.nbu_list