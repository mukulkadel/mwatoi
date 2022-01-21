CREATE VIEW IF NOT EXISTS legacy_available_messages_view AS
SELECT message._id,
 chat.raw_string AS key_remote_jid,
 message.from_me AS key_from_me,
 message.key_id,
 message.status,
 message.broadcast AS needs_push,
 message.text_data AS data,
 message.timestamp,
 message_media.message_url AS media_url,
 message_media.mime_type AS media_mime_type,
 CAST (CASE WHEN (message.message_type = 7 AND message.status=6) THEN 0 ELSE message.message_type END AS VARCHAR) AS media_wa_type,
 IFNULL(message_media.file_length,0) AS media_size,
 message_media.media_name,
 message_media.file_hash AS media_hash,
 message_media.media_duration,
 message.origin,
 message_location.latitude,
 message_location.longitude,
 NULL AS thumb_image,
 jid.raw_string AS remote_resource,
 message.received_timestamp,
 message.timestamp AS send_timestamp,
 message.receipt_server_timestamp,
 message.receipt_server_timestamp AS receipt_device_timestamp,
 NULL AS raw_data,
 message.recipient_count,
 NULL AS read_device_timestamp,
 NULL AS played_device_timestamp,
 NULL AS media_caption,
 message.participant_hash,
 message.starred,
 NULL AS quoted_row_id,
 NULL AS mentioned_jids,
 NULL AS multicast_id,
 NULL AS edit_version,
 message_media.enc_file_hash AS media_enc_hash,
 pay_transaction.id AS payment_transaction_id,
 NULL AS forwarded,
 NULL AS preview_type,
 NULL AS send_count,
 message.lookup_tables,
 NULL AS future_message_type,
 message.message_add_on_flags,
 message.chat_row_id,
 message_ephemeral.expire_timestamp
FROM message
LEFT JOIN jid ON message.sender_jid_row_id=jid._id
LEFT JOIN (SELECT chat._id,jid.raw_string FROM chat JOIN jid ON chat.jid_row_id=jid._id) AS chat ON message.chat_row_id=chat._id
LEFT JOIN message_media ON message._id=message_media.message_row_id
LEFT JOIN message_location ON message._id=message_location.message_row_id
LEFT JOIN pay_transaction ON message._id=pay_transaction.message_row_id
LEFT JOIN message_ephemeral ON message._id = message_ephemeral.message_row_id
LEFT JOIN deleted_chat_job AS job ON job.chat_row_id = message.chat_row_id 
WHERE IFNULL(NOT((IFNULL(message.starred, 0) = 0 AND message._id <= IFNULL(job.deleted_message_row_id, 1)) OR (IFNULL(message.starred, 0) = 1 AND message._id <= IFNULL(job.deleted_starred_message_row_id, 1)) OR ( (job.deleted_message_categories IS NOT NULL) AND   (job.deleted_message_categories LIKE '%"' || message.message_type || '"%') AND   ( (IFNULL(message.starred, 0) = 0 AND message._id <= IFNULL(job.deleted_categories_message_row_id, 1)) OR (IFNULL(message.starred, 0) = 1 AND message._id <= IFNULL(job.deleted_categories_starred_message_row_id, 1)) ))), 0)