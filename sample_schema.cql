CREATE KEYSPACE user_activity WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

CREATE TABLE user_activity.sessions (
  user_id uuid,
  session_id uuid,
  created_at timestamp,
  last_access timestamp,
  PRIMARY KEY (user_id, session_id)
) WITH default_time_to_live = 86400
  AND comment = 'Session data with 1-day TTL';

CREATE TABLE user_activity.logs (
  log_id uuid,
  log_type text,
  message text,
  created_on timestamp,
  PRIMARY KEY (log_id)
) WITH default_time_to_live = 604800
  AND comment = 'Log table with 7-day TTL';

CREATE TABLE user_activity.audit_events (
  event_id uuid,
  user_id uuid,
  event_type text,
  PRIMARY KEY (event_id)
) WITH comment = 'No TTL applied on this table';