
import boto3
from datetime import datetime
import os
import logging

LOGLEVEL = os.getenv('LOG_LEVEL').strip()
TIMESTAMP_FORMAT = '%Y-%m-%d-%H-%M'
RDS = boto3.client('rds')
DB_IDENTIFIER = 'database-1'

logger = logging.getLogger()
logger.setLevel(LOGLEVEL.upper())


def lambda_handler(event, context):

    now = datetime.now()
    now_timestamp = now.strftime(TIMESTAMP_FORMAT)

    snapshot_identifier = ('{}{}'.format(DB_IDENTIFIER, now_timestamp))

    try:
        response = RDS.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=DB_IDENTIFIER,
            )

    except Exception as e:
        logger.info('Could not create snapshot %s (%s)' % (snapshot_identifier, e))


if __name__ == '__main__':
    lambda_handler(None, None)

