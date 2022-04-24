#   iOS whatsapp table list
#   -   Z_PRIMARYKEY
#   -   Z_MODELCACHE
#   -   Z_METADATA
#   -   ZWAZ1PAYMENTTRANSACTION
#   -   ZWAVCARDMENTION
#   -   ZWAPROFILEPUSHNAME
#   -   ZWAPROFILEPICTUREITEM
#   -   ZWAMESSAGEINFO
#   -   ZWAMESSAGEDATAITEM
#   -   ZWAMESSAGE
#   -   ZWAMEDIAITEM
#   -   ZWAGROUPMEMBERSCHANGE
#   -   ZWAGROUPMEMBER
#   -   ZWAGROUPINFO
#   -   ZWACHATSESSION
#   -   ZWACHATPUSHCONFIG
#   -   ZWACHATPROPERTIES
#   -   ZWABLACKLISTITEM

import sqlite3
import argparse
import os


def get_col_names(cursor):
    return list(map(lambda x: x[0], cursor.description))


def row_to_dict(row, col_names):
    data = {}
    for i, col_name in enumerate(col_names):
        data[col_name] = row[i]
    return data


def get_last_pk(cursor, tablename):
    chat_session_pk = 0
    data = list(cursor.execute(
        "SELECT Z_PK FROM {} ORDER BY Z_PK DESC LIMIT 1".format(tablename)))
    if len(data) > 0:
        chat_session_pk = data[0][0]
    return chat_session_pk


A_MEDIA_TYPE_TEXT = '0'
A_MEDIA_TYPE_IMAGE = '1'
A_MEDIA_TYPE_AUDIO = '2'
A_MEDIA_TYPE_VIDEO = '3'
A_MEDIA_TYPE_VCARD = '4'
A_MEDIA_TYPE_LOCATION = '5'
A_MEDIA_TYPE_APPLICATION = '9'
A_MEDIA_TYPE_CALL_LOG = '10'
A_MEDIA_TYPE_MSG_DELETED = '11'
A_MEDIA_TYPE_GIF = '13'
A_MEDIA_TYPE_MAYBE_CONTACT = '14'
A_MEDIA_TYPE_MSG_DELETED2 = '15'
A_MEDIA_TYPE_LIVE_LOCATION = '16'
A_MEDIA_TYPE_STICKER = '20'
A_MEDIA_TYPE_APPLICATION2 = '26'

A_EVENT_TYPE_NONE = 0  # text msg
A_EVENT_TYPE_GRP_NAME_CHANGE = 1
A_EVENT_TYPE_GRP_LEFT = 5
A_EVENT_TYPE_GRP_ICON_CHANGE = 6
A_EVENT_TYPE_GRP_NEW_GROUP_NAME = 11

I_MEDIA_TYPE_TEXT = 0
I_MEDIA_TYPE_IMAGE = 1
I_MEDIA_TYPE_VIDEO = 2
I_MEDIA_TYPE_AUDIO = 3
I_MEDIA_TYPE_VCARD = 4
I_MEDIA_TYPE_LOCATION = 5
I_MEDIA_TYPE_GROUP = 6
I_MEDIA_TYPE_LINK = 7
I_MEDIA_TYPE_APPLICATION = 8
I_MEDIA_TYPE_SECURITY = 10
I_MEDIA_TYPE_GIF = 11
I_MEDIA_TYPE_STATUS = 12
I_MEDIA_TYPE_MSG_DELETED = 14
I_MEDIA_TYPE_STICKER = 15
I_MEDIA_TYPE_ONE_TIME_IMAGE = 38
I_MEDIA_TYPE_ONE_TIME_VIDEO = 39
I_MEDIA_TYPE_UPI_INVITE = 40
I_MEDIA_TYPE_BLACKBOX = -1
I_MEDIA_TYPE_MWATOI = -2

I_EVENT_TYPE_MSG_NOT_FROM_ME = 2
I_EVENT_TYPE_MSG_FROM_ME = 0
I_EVENT_TYPE_NUMBER_CHANGE = 9
I_EVENT_TYPE_GRP_LEFT = 3
I_EVENT_TYPE_GRP_ADD = 2
I_EVENT_TYPE_NEW_GROUP_NAME = 12
I_EVENT_TYPE_UPI_ACTIVATED = 39  # "You can now send and receive money on whatsapp"
I_EVENT_TYPE_SECURITY_CODE_CHANGED = 36
# "This chat is with business account"
I_EVENT_TYPE_BUSINESS_ACCOUNT_NOTIFY = 26
I_EVENT_TYPE_BLACKBOX = -1


def atoi_media_and_group_event_type(message):
    media_type, group_event_type = I_MEDIA_TYPE_BLACKBOX, I_EVENT_TYPE_BLACKBOX
    if message["media_wa_type"] == A_MEDIA_TYPE_TEXT:
        if message["media_size"] == A_EVENT_TYPE_NONE:
            if message["media_url"] != None:
                media_type = I_MEDIA_TYPE_LINK
            else:
                media_type = I_MEDIA_TYPE_TEXT
    elif message["media_wa_type"] == A_MEDIA_TYPE_IMAGE:
        media_type = I_MEDIA_TYPE_IMAGE
    elif message["media_wa_type"] == A_MEDIA_TYPE_VIDEO:
        media_type = I_MEDIA_TYPE_VIDEO
    elif message["media_wa_type"] == A_MEDIA_TYPE_AUDIO:
        media_type = I_MEDIA_TYPE_AUDIO
    elif message["media_wa_type"] == A_MEDIA_TYPE_VCARD:
        media_type = I_MEDIA_TYPE_VCARD
    elif message["media_wa_type"] == A_MEDIA_TYPE_LOCATION or message["media_wa_type"] == A_MEDIA_TYPE_LIVE_LOCATION:
        media_type = I_MEDIA_TYPE_LOCATION
    elif message["media_wa_type"] == A_MEDIA_TYPE_APPLICATION or message["media_wa_type"] == A_MEDIA_TYPE_APPLICATION2:
        media_type = I_MEDIA_TYPE_APPLICATION
    elif message["media_wa_type"] == A_MEDIA_TYPE_GIF:
        media_type = I_MEDIA_TYPE_GIF
    elif message["media_wa_type"] == A_MEDIA_TYPE_MSG_DELETED or message["media_wa_type"] == A_MEDIA_TYPE_MSG_DELETED2:
        media_type = I_MEDIA_TYPE_MSG_DELETED
    elif message["media_wa_type"] == A_MEDIA_TYPE_STICKER:
        media_type = I_MEDIA_TYPE_STICKER
    elif message["media_wa_type"] == A_MEDIA_TYPE_MAYBE_CONTACT:
        media_type = I_MEDIA_TYPE_MWATOI
    group_event_type = I_EVENT_TYPE_MSG_FROM_ME if message[
        "key_from_me"] == 1 else I_EVENT_TYPE_MSG_NOT_FROM_ME
    return media_type, group_event_type


def atoi_timestamp(timestamp):
    if timestamp == None:
        return None
    return timestamp/1000 - 978307200


def get_group_member(asrc, out, chat_session, message, group_member_cache):
    if message["key_from_me"] == 1 or chat_session["ZGROUPINFO"] == None:
        return None
    if message["remote_resource"] in group_member_cache:
        return group_member_cache[message["remote_resource"]]
    group_member = list(out.execute("SELECT Z_PK FROM ZWAGROUPMEMBER WHERE ZCHATSESSION=? AND ZMEMBERJID=?", [
                        chat_session["Z_PK"], message["remote_resource"]]))
    if len(group_member) == 1:
        group_member_cache[message["remote_resource"]] = group_member[0][0]
        return group_member[0][0]
    print("Group member key not found: message-{}, chat_session-{}".format(
        message["_id"], chat_session["Z_PK"]))
    print("Looking for new number of {}".format(message["remote_resource"]))
    timestamp = message['timestamp']
    remote_resource = message["remote_resource"]
    remote_resource_trace = [remote_resource]
    print("Tracking number changes in android db")
    while True:
        row = list(asrc.execute("SELECT thumb_image,timestamp FROM legacy_available_messages_view WHERE media_wa_type=0 AND media_size=10 AND key_remote_jid=? AND remote_resource=? AND timestamp>? ORDER BY timestamp", [
                   message["key_remote_jid"], remote_resource, timestamp]))
        if(len(row) == 0):
            break
        print("{} -> ".format(remote_resource), end='')
        remote_resource = row[0][0][7:].decode()
        print(remote_resource)
        remote_resource_trace.append(remote_resource)
        timestamp = row[0][1]
    group_member = list(out.execute("SELECT Z_PK FROM ZWAGROUPMEMBER WHERE ZCHATSESSION=? AND ZMEMBERJID=?", [
                        chat_session["Z_PK"], remote_resource]))
    group_member = group_member[0][0] if len(group_member) == 1 else None
    for remote_resource in remote_resource_trace:
        group_member_cache[remote_resource] = group_member
    if group_member == None:
        print("Member missing.")
    return group_member


def text_factory(b):
    try:
        return b.decode()
    except:
        print("Error decoding message: {}".format(b))
    return b.decode(errors='replace')


def add_media_info(_):
    # Not transferring media/message sent, received or read data. Not worth the effort.
    return None


def add_media_item(media_type, out, chat_session_pk, message_pk, message):
    add_media_item_flag = media_type in [I_MEDIA_TYPE_IMAGE, I_MEDIA_TYPE_VIDEO, I_MEDIA_TYPE_AUDIO, I_MEDIA_TYPE_VCARD,
                                         I_MEDIA_TYPE_LOCATION, I_MEDIA_TYPE_APPLICATION, I_MEDIA_TYPE_GIF, I_MEDIA_TYPE_MSG_DELETED, I_MEDIA_TYPE_STICKER, I_MEDIA_TYPE_LINK]
    media_item_pk = get_last_pk(out, 'ZWAMEDIAITEM')+1
    file_size = message["media_size"]
    media_origin = message["origin"]
    movie_duration = message["media_duration"]
    latitude = message["latitude"]
    longitude = message["longitude"]
    media_url = message["media_url"]
    title = message["media_caption"]
    author_name = None
    meta_data = None
    if media_type == I_MEDIA_TYPE_APPLICATION:
        author_name = message["media_name"]
    if media_type == I_MEDIA_TYPE_VCARD:
        add_vcard_mention(out, media_item_pk, message)
        vcard_name = message["media_name"]
        vcard_string = message["data"]
    elif media_type == I_MEDIA_TYPE_MSG_DELETED:
        title = message["media_name"]
        vcard_name = message["key_remote_jid"]
        vcard_string = message["remote_resource"]
    elif media_type == I_MEDIA_TYPE_LOCATION:
        file_size = 0
        movie_duration = 0
        author_name = message["media_size"]
        vcard_name = None
        if message["media_name"] != None:
            a_media_name = message["media_name"].split(',')
            a_media_name = a_media_name[1:3]+[str(message['media_duration'])]
            vcard_string = ';'.join(a_media_name)
        else:
            vcard_string = None
    else:
        vcard_name = message["media_enc_hash"]
        vcard_string = message["media_mime_type"]
    if message['mentioned_jids'] != None:
        meta_data = b''.join(
            map(lambda x: b'B\x1b'+x.encode(), message['mentioned_jids'].split(',')))
        add_media_item_flag = True
    if not add_media_item_flag:
        return None
    if media_type == I_MEDIA_TYPE_LINK:
        add_message_data_item(out, chat_session_pk, message_pk, message)
    out.execute("INSERT INTO ZWAMEDIAITEM (Z_PK, Z_ENT, Z_OPT, ZCLOUDSTATUS, ZFILESIZE, ZMEDIAORIGIN, ZMOVIEDURATION, ZMESSAGE, ZASPECTRATIO, ZHACCURACY, ZLATITUDE, ZLONGITUDE, ZMEDIAURLDATE, ZAUTHORNAME, ZCOLLECTIONNAME, ZMEDIALOCALPATH, ZMEDIAURL, ZTHUMBNAILLOCALPATH, ZTITLE, ZVCARDNAME, ZVCARDSTRING, ZXMPPTHUMBPATH, ZMEDIAKEY, ZMETADATA) VALUES (:Z_PK, :Z_ENT, :Z_OPT, :ZCLOUDSTATUS, :ZFILESIZE, :ZMEDIAORIGIN, :ZMOVIEDURATION, :ZMESSAGE, :ZASPECTRATIO, :ZHACCURACY, :ZLATITUDE, :ZLONGITUDE, :ZMEDIAURLDATE, :ZAUTHORNAME, :ZCOLLECTIONNAME, :ZMEDIALOCALPATH, :ZMEDIAURL, :ZTHUMBNAILLOCALPATH, :ZTITLE, :ZVCARDNAME, :ZVCARDSTRING, :ZXMPPTHUMBPATH, :ZMEDIAKEY, :ZMETADATA);",
                {"Z_PK": media_item_pk, "Z_ENT": 8, "Z_OPT": 1, "ZCLOUDSTATUS": None, "ZFILESIZE": file_size, "ZMEDIAORIGIN": media_origin, "ZMOVIEDURATION": movie_duration, "ZMESSAGE": message_pk, "ZASPECTRATIO": 0, "ZHACCURACY": 0, "ZLATITUDE": latitude, "ZLONGITUDE": longitude, "ZMEDIAURLDATE": None, "ZAUTHORNAME": author_name, "ZCOLLECTIONNAME": None, "ZMEDIALOCALPATH": None, "ZMEDIAURL": media_url, "ZTHUMBNAILLOCALPATH": None, "ZTITLE": title, "ZVCARDNAME": vcard_name, "ZVCARDSTRING": vcard_string, "ZXMPPTHUMBPATH": None, "ZMEDIAKEY": None, "ZMETADATA": meta_data})
    return media_item_pk


def get_sort_key(cursor, chat_session, userid):
    sort = 1
    row = list(cursor.execute("SELECT ZSORT FROM ZWAMESSAGE WHERE ZCHATSESSION=? AND ZTEXT IS NULL AND ZMESSAGETYPE=6 AND ZGROUPMEMBER IS NULL AND ( ZGROUPEVENTTYPE=2 OR (ZGROUPEVENTTYPE=12 AND ZFROMJID LIKE '{}%')) ORDER BY ZSORT DESC".format(
        userid), [chat_session["Z_PK"]]))
    if(len(row) != 0):
        sort = row[0][0]
    return sort+1


def add_message_data_item(out, chat_session_pk, message_pk, message):
    # It stores link related data.
    print("Adding link data.")
    message_data_item_pk = get_last_pk(out, 'ZWAMESSAGEDATAITEM')+1
    out.execute("INSERT INTO ZWAMESSAGEDATAITEM (Z_PK, Z_ENT, Z_OPT, ZINDEX, ZOWNSTHUMBNAIL, ZTYPE, ZMESSAGE, ZDATE, ZCHATJID, ZCONTENT1, ZCONTENT2, ZMATCHEDTEXT, ZSECTIONID, ZSENDERJID, ZSUMMARY, ZTHUMBNAILPATH, ZTITLE) VALUES (:Z_PK, :Z_ENT, :Z_OPT, :ZINDEX, :ZOWNSTHUMBNAIL, :ZTYPE, :ZMESSAGE, :ZDATE, :ZCHATJID, :ZCONTENT1, :ZCONTENT2, :ZMATCHEDTEXT, :ZSECTIONID, :ZSENDERJID, :ZSUMMARY, :ZTHUMBNAILPATH, :ZTITLE);",
                {"Z_PK": message_data_item_pk, "Z_ENT": 10, "Z_OPT": 1, "ZINDEX": 0, "ZOWNSTHUMBNAIL": None, "ZTYPE": 0, "ZMESSAGE": message_pk, "ZDATE": atoi_timestamp(message["timestamp"]), "ZCHATJID": 'p{}'.format(chat_session_pk), "ZCONTENT1": message["media_url"], "ZCONTENT2": message["media_url"], "ZMATCHEDTEXT": message["media_url"], "ZSECTIONID": None, "ZSENDERJID": None, "ZSUMMARY": message["media_name"], "ZTHUMBNAILPATH": None, "ZTITLE": message["media_caption"]})


def add_vcard_mention(out, media_item_pk, message):
    # It stores vcard related data.
    print("Adding vcard data.")
    vcard_mention_pk = get_last_pk(out, 'ZWAVCARDMENTION')+1
    out.execute("INSERT INTO ZWAVCARDMENTION (Z_PK, Z_ENT, Z_OPT, ZISFROMME, ZTRUSTEDWHENINDEXED, ZMEDIAITEM, ZDATE, ZSENDERJID, ZWHATSAPPID) VALUES (:Z_PK, :Z_ENT, :Z_OPT, :ZISFROMME, :ZTRUSTEDWHENINDEXED, :ZMEDIAITEM, :ZDATE, :ZSENDERJID, :ZWHATSAPPID);",
                {"Z_PK": vcard_mention_pk, "Z_ENT": 14, "Z_OPT": 1, "ZISFROMME": message["key_from_me"], "ZTRUSTEDWHENINDEXED": 1, "ZMEDIAITEM": media_item_pk, "ZDATE": atoi_timestamp(message["timestamp"]), "ZSENDERJID": None if message["key_from_me"] == 1 else message["key_remote_jid"], "ZWHATSAPPID": None})


def add_payment_transaction(out, asrc, message, is_group):
    # It stores payment transaction related data.
    print("Adding payment transaction.")
    payment = asrc.execute(
        "SELECT * FROM pay_transactions WHERE id=?", [message["payment_transaction_id"]])
    payment_cols = get_col_names(payment)
    payment = list(payment)
    group_jid = None if not is_group else message["key_remote_jid"]
    if (len(payment)) == 1:
        payment = row_to_dict(payment[0], payment_cols)
        payment_transaction_pk = get_last_pk(out, 'ZWAZ1PAYMENTTRANSACTION')+1
        if payment['metadata'] == None:
            payment['metadata'] = ''
        out.execute("INSERT INTO ZWAZ1PAYMENTTRANSACTION (Z_PK, Z_ENT, Z_OPT, ZAMOUNT_1000, ZSTATUS, ZTYPE, ZTIMESTAMP, ZBANKTRANSACTIONID, ZCREDENTIALID, ZCURRENCY, ZERRORCODE, ZGROUPJID, ZMESSAGESTANZAID, ZRECEIVERJID, ZSENDERJID, ZTRANSACTIONID, ZMETADATA) VALUES (:Z_PK, :Z_ENT, :Z_OPT, :ZAMOUNT_1000, :ZSTATUS, :ZTYPE, :ZTIMESTAMP, :ZBANKTRANSACTIONID, :ZCREDENTIALID, :ZCURRENCY, :ZERRORCODE, :ZGROUPJID, :ZMESSAGESTANZAID, :ZRECEIVERJID, :ZSENDERJID, :ZTRANSACTIONID, :ZMETADATA);",
                    {"Z_PK": payment_transaction_pk, "Z_ENT": 15, "Z_OPT": 2, "ZAMOUNT_1000": payment["amount_1000"], "ZSTATUS": payment["status"], "ZTYPE": payment["type"], "ZTIMESTAMP": atoi_timestamp(payment["timestamp"]), "ZBANKTRANSACTIONID": payment["bank_transaction_id"], "ZCREDENTIALID": payment["credential_id"], "ZCURRENCY": payment["currency"], "ZERRORCODE": payment["error_code"], "ZGROUPJID": group_jid, "ZMESSAGESTANZAID": payment["key_id"], "ZRECEIVERJID": payment["receiver"], "ZSENDERJID": payment["sender"], "ZTRANSACTIONID": payment["id"], "ZMETADATA": payment["metadata"].encode()})

# Execution begins here.
OUTPUT_FILE = "out\\out.db"
parser = argparse.ArgumentParser(description="Script to convert android db into iOS db.")
parser.add_argument("-adb","--android_db",help="Android DB file.",type=str)
parser.add_argument("-idb","--ios_db",help="iOS DB file.",type=str)
parser.add_argument("-u","--user_id",help="User Id. Eg: 9185XXXXXXXX",type=str)

if os.path.exists(OUTPUT_FILE):
    print("Output file already exists. {}".format(OUTPUT_FILE))
    if input("Do you wish to overwrite it? [y/n]:").upper()=="Y":
        os.remove(OUTPUT_FILE)
    else:
        exit(1)

args = parser.parse_args()
asrc = sqlite3.connect(args.android_db)
asrc.text_factory = text_factory
isrc = sqlite3.connect(args.ios_db)
out = sqlite3.connect(OUTPUT_FILE)
userid = args.user_id

user_jid = userid+"@s.whatsapp.net"

print("Duplicating ios whatsapp db.")
query = "".join(line for line in isrc.iterdump())
out.executescript(query)

print("Initiating android whatsapp db migration.")
print("Reading chat sessions")

total_chat_count = list(asrc.execute("SELECT COUNT(*) FROM chat"))[0][0]
print("Total chat sessions found: %d" % (total_chat_count))

chat_sessions = asrc.execute(
    "SELECT c.*,j.user,j.server,j.agent,j.type,j.raw_string,j.device FROM chat c LEFT JOIN jid j ON c.jid_row_id=j._id")
chat_sessions_cols = get_col_names(chat_sessions)

for chat_session in chat_sessions:
    data = row_to_dict(chat_session, chat_sessions_cols)
    print(data["raw_string"], end=' - ')
    # Checking if chat session already exists
    tmp = list(out.execute(
        'SELECT * FROM ZWACHATSESSION WHERE ZCONTACTJID=?', [data["raw_string"]]))
    if(len(tmp) > 0):
        print("already exists, ignoring.")
    else:
        chat_session_pk = get_last_pk(out, 'ZWACHATSESSION')+1
        data["archived"] = data["archived"] if data["archived"] != None else 0
        spotlight_status = 1 if data["server"] == 'g.us' else -5
        if data["server"] == 's.whatsapp.net':
            # Normal chat
            session_type = 0
            contact_id = 1
        elif data["server"] == 'g.us':
            # Group chat
            session_type = 1
            contact_id = None
        elif data["server"] == 'broadcast':
            # Broadcast
            session_type = 2
            contact_id = None
        else:
            # Status
            session_type = 3
            contact_id = 1
        data["subject"] = data["subject"] if data["subject"] != None else ''
        group_info_pk = None
        if session_type == 1:
            # Group data not present.
            print("creating null group.", end=" ")
            group_info_pk = get_last_pk(out, 'ZWAGROUPINFO')+1
            # Creating group info.
            out.execute("INSERT INTO ZWAGROUPINFO (Z_PK, Z_ENT, Z_OPT, ZSTATE, ZCHATSESSION, ZLASTMESSAGEOWNER, ZCREATIONDATE, ZSUBJECTTIMESTAMP, ZCREATORJID, ZOWNERJID, ZPICTUREID, ZPICTUREPATH, ZSOURCEJID, ZSUBJECTOWNERJID) VALUES (?,5,1,0,?,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);", [
                        group_info_pk, chat_session_pk])
            # Adding group members.
            group_members = asrc.execute(
                "SELECT * FROM group_participants WHERE gjid=?", [data["raw_string"]])
            group_members_cols = get_col_names(group_members)
            for group_member in group_members:
                group_member = row_to_dict(group_member, group_members_cols)
                group_member_pk = get_last_pk(out, 'ZWAGROUPMEMBER')+1
                admin = 0 if group_member["admin"] == 0 else 1
                out.execute("INSERT INTO ZWAGROUPMEMBER (Z_PK, Z_ENT, Z_OPT, ZCONTACTABID, ZISACTIVE, ZISADMIN, ZSENDERKEYSENT, ZCHATSESSION, ZRECENTGROUPCHAT, ZCONTACTIDENTIFIER, ZCONTACTNAME, ZFIRSTNAME, ZMEMBERJID) VALUES (?,6,1,0,1,?,NULL,?,NULL,NULL,'',NULL,?);", [
                            group_member_pk, admin, chat_session_pk, group_member["jid"]])

        out.execute("INSERT INTO ZWACHATSESSION (Z_PK, Z_ENT, Z_OPT, ZARCHIVED, ZCONTACTABID, ZFLAGS, ZHIDDEN, ZIDENTITYVERIFICATIONEPOCH, ZIDENTITYVERIFICATIONSTATE, ZMESSAGECOUNTER, ZREMOVED, ZSESSIONTYPE, ZSPOTLIGHTSTATUS, ZUNREADCOUNT, ZGROUPINFO, ZLASTMESSAGE, ZPROPERTIES, ZLASTMESSAGEDATE, ZLOCATIONSHARINGENDDATE, ZCONTACTIDENTIFIER, ZCONTACTJID, ZETAG, ZLASTMESSAGETEXT, ZPARTNERNAME, ZSAVEDINPUT) VALUES (?,4,2,?,0,256,?,0,0,0,0,?,?,?,?,NULL,NULL,NULL,NULL,?,?,NULL,NULL,?,NULL);",
                    (chat_session_pk, data["archived"], data["hidden"], session_type, spotlight_status, data["unseen_message_count"], group_info_pk, contact_id, data["raw_string"], data["subject"]))
        print("inserted.")

print("Chat sessions migrated.")
print("Reading messages from chat session.")
chat_sessions = out.execute(
    "SELECT * FROM ZWACHATSESSION")
chat_sessions_cols = get_col_names(chat_sessions)

# Creating legacy_available_messages_view if doesn't exist.
with open('query\\create_legacy_available_messages_view.sql','r') as create_query:
    asrc.execute(create_query.read())

# Creating pay_transactions view if doesn't exist.
with open('query\\create_pay_transactions.sql','r') as create_query:
    asrc.execute(create_query.read())

for chat_session in chat_sessions:
    chat_session = row_to_dict(chat_session, chat_sessions_cols)
    messages_count = list(asrc.execute(
        "SELECT COUNT(*) FROM legacy_available_messages_view WHERE key_remote_jid=? ORDER BY timestamp", [chat_session["ZCONTACTJID"]]))[0][0]
    print("{} messages found: {}".format(
        chat_session["ZCONTACTJID"], messages_count))
    messages = asrc.execute(
        "SELECT * FROM legacy_available_messages_view WHERE key_remote_jid=? ORDER BY timestamp", [chat_session["ZCONTACTJID"]])
    messages_cols = get_col_names(messages)
    init_sort = sort = get_sort_key(out, chat_session, userid)
    group_member_cache = {}
    for message in messages:
        message = row_to_dict(message, messages_cols)
        message_pk = get_last_pk(out, 'ZWAMESSAGE')+1

        media_type, group_event_type = atoi_media_and_group_event_type(message)
        if media_type == I_MEDIA_TYPE_BLACKBOX or group_event_type == I_EVENT_TYPE_BLACKBOX:
            continue

        spotlight_status = 2 if message["key_remote_jid"] == 'status@broadcast' else -32768
        message_date = atoi_timestamp(message['timestamp'])
        from_jid = None if message["key_from_me"] == 1 else message["key_remote_jid"]
        to_jid = message["key_remote_jid"] if message["key_from_me"] == 1 else None
        group_member = get_group_member(
            asrc, out, chat_session, message, group_member_cache)
        media_info = add_media_info(message)
        media_item = add_media_item(
            media_type, out, chat_session["Z_PK"], message_pk, message)
        # Handling extra msg after media item add.
        if media_type == I_MEDIA_TYPE_MWATOI:
            media_type = I_MEDIA_TYPE_TEXT
            message["data"] = "<mwatoi> {}".format(message["media_name"])
        if media_type == I_MEDIA_TYPE_TEXT and message["payment_transaction_id"] != None and message["payment_transaction_id"] != 'UNSET':
            #Skipping payment transactions. It's causing crashes because of metadata column.
            message["data"] = "<mwatoi, payment> {}".format(message["data"])
            #add_payment_transaction(out, asrc, message, chat_session["ZGROUPINFO"] != None)

        out.execute("INSERT INTO ZWAMESSAGE (Z_PK, Z_ENT, Z_OPT, ZCHILDMESSAGESDELIVEREDCOUNT, ZCHILDMESSAGESPLAYEDCOUNT, ZCHILDMESSAGESREADCOUNT, ZDATAITEMVERSION, ZDOCID, ZENCRETRYCOUNT, ZFILTEREDRECIPIENTCOUNT, ZFLAGS, ZGROUPEVENTTYPE, ZISFROMME, ZMESSAGEERRORSTATUS, ZMESSAGESTATUS, ZMESSAGETYPE, ZSORT, ZSPOTLIGHTSTATUS, ZSTARRED, ZCHATSESSION, ZGROUPMEMBER, ZLASTSESSION, ZMEDIAITEM, ZMESSAGEINFO, ZPARENTMESSAGE, ZMESSAGEDATE, ZSENTDATE, ZFROMJID, ZMEDIASECTIONID, ZPHASH, ZPUSHNAME, ZSTANZAID, ZTEXT, ZTOJID) VALUES (:Z_PK, :Z_ENT, :Z_OPT, :ZCHILDMESSAGESDELIVEREDCOUNT, :ZCHILDMESSAGESPLAYEDCOUNT, :ZCHILDMESSAGESREADCOUNT, :ZDATAITEMVERSION, :ZDOCID, :ZENCRETRYCOUNT, :ZFILTEREDRECIPIENTCOUNT, :ZFLAGS, :ZGROUPEVENTTYPE, :ZISFROMME, :ZMESSAGEERRORSTATUS, :ZMESSAGESTATUS, :ZMESSAGETYPE, :ZSORT, :ZSPOTLIGHTSTATUS, :ZSTARRED, :ZCHATSESSION, :ZGROUPMEMBER, :ZLASTSESSION, :ZMEDIAITEM, :ZMESSAGEINFO, :ZPARENTMESSAGE, :ZMESSAGEDATE, :ZSENTDATE, :ZFROMJID, :ZMEDIASECTIONID, :ZPHASH, :ZPUSHNAME, :ZSTANZAID, :ZTEXT, :ZTOJID);", {
            "Z_PK": message_pk, "Z_ENT": 9, "Z_OPT": 2, "ZCHILDMESSAGESDELIVEREDCOUNT": 0, "ZCHILDMESSAGESPLAYEDCOUNT": 0, "ZCHILDMESSAGESREADCOUNT": 0, "ZDATAITEMVERSION": 3, "ZDOCID": 0, "ZENCRETRYCOUNT": 0, "ZFILTEREDRECIPIENTCOUNT": message["recipient_count"], "ZFLAGS": 0, "ZGROUPEVENTTYPE": group_event_type, "ZISFROMME": message["key_from_me"], "ZMESSAGEERRORSTATUS": 0, "ZMESSAGESTATUS": message["status"], "ZMESSAGETYPE": media_type, "ZSORT": sort, "ZSPOTLIGHTSTATUS": spotlight_status, "ZSTARRED": message["starred"], "ZCHATSESSION": chat_session["Z_PK"], "ZGROUPMEMBER": group_member, "ZLASTSESSION": chat_session["Z_PK"], "ZMEDIAITEM": media_item, "ZMESSAGEINFO": media_info, "ZPARENTMESSAGE": None, "ZMESSAGEDATE": message_date, "ZSENTDATE": message_date, "ZFROMJID": from_jid, "ZMEDIASECTIONID": None, "ZPHASH": None, "ZPUSHNAME": None, "ZSTANZAID": message["key_id"], "ZTEXT": message["data"], "ZTOJID": to_jid})
        sort += 1
    print("Fixing ios and android messages order.")
    ios_message_last_pk = get_last_pk(isrc, 'ZWAMESSAGE')
    out.execute("UPDATE ZWAMESSAGE SET ZSORT=?+ZSORT WHERE ZCHATSESSION=? AND ZSORT>=? AND Z_PK<=?",
                [sort-init_sort, chat_session["Z_PK"], init_sort, ios_message_last_pk])
    #updating total msgs, last message and last message date.
    message_counter = list(out.execute(
        "SELECT COUNT(*) FROM ZWAMESSAGE WHERE ZCHATSESSION=?", [chat_session["Z_PK"]]))[0][0]
    last_message = None
    last_message_date = None
    row = list(out.execute(
        "SELECT Z_PK,ZMESSAGEDATE FROM ZWAMESSAGE WHERE ZCHATSESSION=? ORDER BY ZSORT DESC LIMIT 1", [chat_session["Z_PK"]]))
    if len(row) == 1:
        last_message, last_message_date = row[0]
    out.execute("UPDATE ZWACHATSESSION SET ZMESSAGECOUNTER=?,ZLASTMESSAGE=?,ZLASTMESSAGEDATE=? WHERE Z_PK=?",
                [message_counter, last_message, last_message_date, chat_session["Z_PK"]])

print("Updating Z_PRIMARYKEY table.")
for row in out.execute('SELECT Z_ENT,Z_NAME FROM Z_PRIMARYKEY'):
    last_pk = get_last_pk(out, 'Z'+row[1])
    out.execute('UPDATE Z_PRIMARYKEY SET Z_MAX=? WHERE Z_ENT=?',
                [last_pk, row[0]])

out.commit()

out.close()
isrc.close()
asrc.close()
