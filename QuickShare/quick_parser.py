from datetime import datetime
import os
from utils.db_library import *


""" 아티팩트 경로 입력 """
# com.samsung.sharelive
MobQuick_path = "share_live.db"
# com.android.providers.media.module
external_db = "external.db"
# PC Quick Share
PcQuick_path = "PCQuickShareV4.db"
PCQuick_log_path = "Logs"


class QuickShare():
    def __init__(self):
        self.version = 1.0
        self.quick_list = []

    def _convert_unixtimestamp(self, timestamp):
        time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        return time

    def sharelive_contact(self, path):
        with sqlite3.connect(path) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute("select * from devices")

        mob_list = []
        for index in data.fetchall():
            device = 'Tablet' if index[3]  == 1 else 'Desktop' if index[3]  > 1 else 'Phone'

            mob_dic = {'platform': "Mobile", 'time': self._convert_unixtimestamp(index[26] / 1000.0), 'name': index[2], 'type': device,
                     'mac': index[0]}
            mob_list.append(mob_dic)
        return mob_list


    def downloaded(self):
        with sqlite3.connect(external_db) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute("select date_modified, _display_name, mime_type, _data, _size, title from downloads")


            for index in data.fetchall():
                if 'Quick Share' in index[3]:
                    download_data = {
                        'event': 'Received',
                        'share_id': None,
                        'filename': index[3].split('/')[-1],
                        'time': self._convert_unixtimestamp(index[0] / 1000), 'filesize': index[4],
                        'mimetype': index[2],
                        'device_id': None, 'device_name': None,
                        'status': 'Success'
                    }

                    self.quick_list.append(download_data)

            return self.quick_list


    def sharelive_send(self):
        with sqlite3.connect(MobQuick_path) as db_connection:
            cur = db_connection.cursor()
            data1 = cur.execute("select device_id, share_id, device_name, file_sent_count, file_cancelled_count, file_failed_count from devices")
            data1 = data1.fetchall()

            data2 = cur.execute("select share_id, uri from files")
            data2 = data2.fetchall()

            data3 = cur.execute("select id, create_time from shares")
            data3 = data3.fetchall()

            for index in data1:
                send_status = ''
                if index[3] > 0:
                    send_status = 'Success'
                elif index[3] > 0:
                    send_status = 'Cancel'
                elif index[5] > 0:
                    send_status = 'Failed'

                if send_status != '':
                    for index3 in data3:
                        for index2 in data2:
                            if index2[0] == index3[0] == index[1]:
                                share_id = index3[0]
                                share_time = index3[1]
                                share_file = index2[1]

                                send_data = {'event': 'Send' , 'share_id': share_id, 'time': self._convert_unixtimestamp(share_time / 1000), 'filename': share_file.split('/')[-1],
                                             'device_id': index[0], 'device_name': index[2],
                                             'status': send_status,
                                             'mimetype': None, 'filesize': None}
                                self.quick_list.append(send_data)


    def PCQuickShareV4(self, path):
        with sqlite3.connect(path) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute("select deviceModel, deviceType, deviceName,  CreatedTime from DeviceInfoLists")

        pc_list = []
        for index in data.fetchall():
            device = 'Tablet' if index[1] == 'tablet' else 'Desktop' if index[1] == 'pc' else 'Phone'

            pc_dict = {'platform': "Desktop", 'time': self._convert_unixtimestamp(index[3] / 1000.0), 'name': index[2], 'type': device,
                       'mac': None}
            pc_list.append(pc_dict)
        return pc_list


    def PCQuick_Logs(self, path):
        file_list = os.listdir(path)
        pcquick_log_list = []

        for index in file_list:
            with open(path + os.sep + index, 'rb') as f:
                text = f.readlines()

                for index2 in text:
                    struct = str(index2)[2:-1].split(' ')
                    try:
                        timestamp = struct[0] + 'T' + struct[1] + '000Z'

                        # Scan Result
                        if struct[8] + ' ' + struct[9] == 'OnResponseReceived 272':
                            device_flag = str(index2)[2:-1].split('=')[3][1]
                            device = 'Tablet' if device_flag == '2' else 'Desktop' if device_flag == '3' else 'Phone'

                            pcquick_dict = {'platform': "Desktop", 'time': timestamp, 'name': str(index2)[2:-1].split('=')[2].split(',')[0][1:], 'type': device,
                                          'mac': str(index2)[2:-1].split('=')[1].split(',')[0][1:]}
                            

                            if pcquick_dict['time'] not in pcquick_log_list:
                                pcquick_log_list.append(pcquick_dict)
                    except:
                        pass

        return pcquick_log_list


def quick_contact_list():
    qs = QuickShare()
    MobQS = qs.sharelive_contact(MobQuick_path)
    PCQS = qs.PCQuickShareV4(PcQuick_path)
    PCQS_log = qs.PCQuick_Logs(PCQuick_log_path)

    return MobQS + PCQS + PCQS_log


def run(out_path):
    qs = QuickShare()
    qs.sharelive_send()
    qs.downloaded()

    for total_index2 in qs.quick_list:
        total_index2['service'] = 'Quick Share'
        insert_total_sharing(total_index2, out_path)

    return qs.quick_list
