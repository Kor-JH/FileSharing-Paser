from datetime import datetime
from utils.db_library import *


""" 아티팩트 경로 입력 """
# com.samsung.privateshare
ts_path = "transaction_database.db"
log_path = "ps.log"


class PrivateShare():
    def __init__(self):
        self.version = 1.0
        self.ps_share_list = []

    def _convert_unixtimestamp(self, timestamp):
        time = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        return time

    def transfer_data(self, path):
        with sqlite3.connect(path) as db_connection:
            cur = db_connection.cursor()
            data = cur.execute("select * from 'Transaction'")
        return data.fetchall()

    def ps_log(self, path):
        with open(path, 'rb') as f:
            text = f.readlines()

            owner_name = None
            member_list = []
            send_list = []
            receive_list = []
            temp_list = []

            cnt = 0
            for index in text:
                struct = str(index)[2:-1].split(' ')

                if len(struct) > 4:
                    if (struct[4][:-1] == 'getInvitationFromDB()') \
                            and owner_name == None:
                        owner_name = struct[5]

                    # 멤버 추가
                    #TODO 한글 인코딩이 하나 있음, 해결필요
                    if (struct[4] == 'addSource(invitations)') and struct[6] != '[]':
                        member_dict = {'platform': "Mobile", 'name': str(index).split(',')[1].split('=')[1], 'time': self._convert_unixtimestamp(int(str(index).split(',')[4].split('=')[1])),
                                       'type': None, 'mac': None}
                        member_list.append(member_dict)

                    # 보낸 파일 정보
                    if struct[4][:-1] == 'fileDisplayName':
                        flag = 1
                        while True:
                            temp = str(text[cnt + flag]).split(' ')
                            if temp[5] == 'SUCCESS':
                                break
                            flag +=1

                        send_dict = {'event': 'Send', 'filename': str(index).split(',')[0].split(' ')[5], 'time': '2022-' + str(text[cnt+flag]).split(' ')[0][2:] + 'T' +
                                                                                                              str(text[cnt+flag]).split(' ')[1] + '000Z', 'filekey': None}
                        send_list.append(send_dict)

                    # 받은 파일 정보
                    if (struct[4] == 'addSource(fileLogCards)') and struct[6] != '[]':
                        receive_dict = {'event': 'Received', 'filename': struct[10].split('=')[1][:-1], 'time': self._convert_unixtimestamp(int(struct[11].split('=')[1][:-1])),
                                        'filekey': struct[13].split('=')[1][:-1], 'thumbnailkey': struct[14].split('=')[1][:-1]}

                        # 중복제거
                        if not receive_dict['time'] in temp_list:
                            receive_list.append(receive_dict)
                            temp_list.append(receive_dict['time'])

                cnt += 1
        return owner_name, member_list, send_list ,receive_list


def run(out_path):
    pv = PrivateShare()
    owner_name, log_member, log_send, log_receive = pv.ps_log(log_path)

    for total_index3 in pv.ps_share_list :
        total_index3['service'] = 'Private Share'
        total_index3['device_name'] = None
        insert_total_sharing(total_index3, out_path)

    return owner_name, log_member, log_send, log_receive