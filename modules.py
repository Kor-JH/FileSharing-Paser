import NearbyShare.nearby_parser as nb
import QuickShare.quick_parser as qs
import PrivateShare.private_parser as pv
from utils.db_library import *


def get_sharing_info():
    out_path = "results.db"

    make_total_sharing(out_path)
    make_contact_table(out_path)
    make_ps_sharing(out_path)
    make_nbu_sharing(out_path)
    make_qs_sharing(out_path)

    nbu_info = nb.run(out_path)
    quickshare_data = qs.run(out_path)
    contact_list = qs.quick_contact_list()
    pv_info = pv.run(out_path)

    contact_list = contact_list + pv_info[1]
    for index in contact_list:
        insert_contacted_data(index, out_path)

    for index2 in pv_info[2] + pv_info[3]:
        insert_ps_sharing(index2, out_path)

    for index3 in nbu_info:
        insert_nbu_sharing(index3, out_path)

    for index4 in quickshare_data:
        insert_qs_sharing(index4, out_path)


    with sqlite3.connect(out_path) as db_connection:
        cur = db_connection.cursor()

        data = cur.execute(
            "select EventTime, Event, Device_name, FileName from quick_sharing")

        data2 = cur.execute(
            "select EventTime, Event, FileName from ps_sharing")

        data = data.fetchall()
        data2 = data2.fetchall()


        for total_index in data:
            total_index['service'] = 'Quick Share'
            insert_total_sharing(total_index, out_path)

        for total_index2 in data2:
            total_index2['service'] = 'Private Share'
            total_index2['device_name'] = None
            insert_total_sharing(total_index2, out_path)
