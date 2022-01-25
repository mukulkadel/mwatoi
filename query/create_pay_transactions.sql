CREATE VIEW IF NOT EXISTS pay_transactions AS
SELECT 
pay_transaction.amount_1000,
pay_transaction.status,
pay_transaction.type,
pay_transaction.timestamp,
pay_transaction.bank_transaction_id,
pay_transaction.credential_id,
pay_transaction.currency_code AS currency,
pay_transaction.error_code,
pay_transaction.key_id,
receiver_jid.raw_string AS receiver,
sender_jid.raw_string AS sender,
pay_transaction.id,
pay_transaction.metadata
FROM pay_transaction
LEFT JOIN jid AS sender_jid ON pay_transaction.sender_jid_row_id=sender_jid._id
LEFT JOIN jid AS receiver_jid ON pay_transaction.receiver_jid_row_id=receiver_jid._id