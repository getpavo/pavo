from ftplib import FTP
import logging
import io

from jackman.helpers import get_config_value

log = logging.getLogger(__name__)

ftp_settings = get_config_value('deployment.ftp')
if not ftp_settings:
    raise ValueError('Missing ftp details in Jackman configuration file')


def safe():
    with FTP(ftp_settings['host']) as ftp:
        ftp.login(user=ftp_settings['username'], passwd=ftp_settings['password'])
        ftp.cwd(ftp_settings['path'])

        file_map = {}
        for file in ftp.nlst():
            r = io.BytesIO()
            ftp.retrbinary(f'RETR {file}', r.write)
            file_map[file] = r
            r.close()
    try:
        unsafe()
    except Exception as e:
        log.exception('Something went wrong trying to deploy. Replacing with backup.')


def unsafe():
    pass
