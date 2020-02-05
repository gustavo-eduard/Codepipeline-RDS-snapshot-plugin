
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
    codepipeline = boto3.client('codepipeline')
    job_id = event['CodePipeline.job']['id']

    try:
        now = datetime.now()
        now_timestamp = now.strftime(TIMESTAMP_FORMAT)

        snapshot_identifier = ('{}-{}'.format(DB_IDENTIFIER, now_timestamp))
        snapshot = RDS.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=DB_IDENTIFIER,
            ) 
        logger.debug(snapshot)
        response = codepipeline.put_job_success_result(jobId=job_id)

    except Exception as error:
        logger.info('Could not create snapshot %s (%s)' % (snapshot_identifier, error))
        response = codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={'type': 'JobFailed', 'message': error}
            )
    logger.debug(response)

if __name__ == '__main__':
    lambda_handler(None, None)

