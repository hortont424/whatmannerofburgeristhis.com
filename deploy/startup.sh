git --git-dir /var/www/whatmannerofburgeristhis.com/.git --work-tree /var/www/whatmannerofburgeristhis.com pull
cd /var/www/whatmannerofburgeristhis.com
NOPREFIX=1 make
chown -R www-data /var/www
/usr/bin/supervisord -n