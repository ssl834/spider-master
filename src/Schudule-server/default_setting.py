# coding: utf8
"""
How ScrapydWeb works:
BROWSER_HOST <<<>>> SCRAPYDWEB_BIND:SCRAPYDWEB_PORT <<<>>> your SCRAPYD_SERVERS

GitHub: https://github.com/my8100/scrapydweb
"""

import os

settings={
    # -------一般设置--------
    'debug': True,
    'port': 5000,
    'autoreload': True,
    'ui_modules': {},
    # 设置默认的处理函数类，如：404页面等
    'default_handler_class': None,
    'serve_traceback': False,

    # -------模板设置-------
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'compiled_template_cache': True,
    'autoescape': None,

    # -------认证安全设置-------
    # cookie标识位，用来给cookie签名。
    'cookie_secret': '',
    'login_url': '',
    # 如果true, 跨站请求伪造(防护) 将被开启.
    'xsrf_cookies': True,
    'xsrf_cookie_version': None,

    # -------静态文件设置-------
    'static_hash_cache': False,
    'static_path': os.path.join(os.path.dirname(__file__), 'static/v100/css '),
    'static_url_prefix': '/static/',
    # 额外添加
    'SCRAPYDWEB_BIND':'0.0.0.0',
    'SCRAPYDWEB_PORT' : 5000,
    'ENABLE_AUTH':False,
    'USERNAME':'',
    'PASSWORD':'',
    'SCRAPY_PROJECTS_DIR':'',
    'SCRAPYD_SERVERS':[
    '127.0.0.1:6800',
    # 'username:password@localhost:6801#group',
    ('', '', '', '', ''),
],
    'SCRAPYD_LOGS_DIR':'',
    'SCRAPYD_LOG_EXTENSIONS':['.log', '.log.gz', '.txt'],
    'SHOW_SCRAPYD_ITEMS':True,
    'SHOW_DASHBOARD_JOB_COLUMN':False,
    'DASHBOARD_RELOAD_INTERVAL':300,
    'DAEMONSTATUS_REFRESH_INTERVAL':10,
    'ENABLE_CACHE':True,
    'CACHE_ROUND_INTERVAL':300,
    'CACHE_REQUEST_INTERVAL':10,
    'DELETE_CACHE':False,
    'ENABLE_EMAIL':False,
    'SMTP_SERVER':'',
    'SMTP_PORT':0,
    'SMTP_OVER_SSL':False,
    'SMTP_CONNECTION_TIMEOUT':10,
    'FROM_ADDR':'',
    'EMAIL_PASSWORD':'',
    'TO_ADDRS':[],
    'EMAIL_WORKING_DAYS':[],
    'EMAIL_WORKING_HOURS':[],
    'ON_JOB_RUNNING_INTERVAL':0,
    'ON_JOB_FINISHED':False,
    'DEBUG':False,
    'VERBOSE':False


}





















# Config for https://mail.google.com using SSL
# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 465
# SMTP_OVER_SSL = True

# Config for https://mail.google.com
# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 587
# SMTP_OVER_SSL = False

# Config for https://mail.qq.com/ using SSL
# SMTP_SERVER = 'smtp.qq.com'
# SMTP_PORT = 465
# SMTP_OVER_SSL = True

# Config for http://mail.10086.cn/
# SMTP_SERVER = 'smtp.139.com'
# SMTP_PORT = 25
# SMTP_OVER_SSL = False




# As for different email service provider, you might have to get an APP password (like Gmail)
# or an authorization code (like QQ mail) and set it as the EMAIL_PASSWORD.
# Check out below links to get more help:
# https://stackoverflow.com/a/27515833/10517783 How to send an email with Gmail as the provider using Python?
# https://stackoverflow.com/a/26053352/10517783 Python smtplib proxy support

# e.g., ['username@gmail.com', ]


######### email working time ##########
#Monday is 1 and Sunday is 7.
# [1, 2, 3, 4, 5, 6, 7]






########## advanced triggers ##########
# - LOG_XXX_THRESHOLD:
#   - Trigger email notice the first time reaching the threshold for a specific kind of log.
#   - The default is 0, set it to a positive integer to enable this trigger.
# - LOG_XXX_TRIGGER_STOP (optional):
#   - The default is False, set it to True to stop current job automatically when reaching the LOG_XXX_THRESHOLD.
#   - The SIGTERM signal would be sent only one time to shut down the crawler gracefully.
#   - In order to avoid an UNCLEAN shutdown, the 'STOP' action would be executed one time at most
#   - if none of the 'FORCESTOP' triggers is enabled, no matter how many 'STOP' triggers are enabled.
# - LOG_XXX_TRIGGER_FORCESTOP (optional):
#   - The default is False, set it to True to FORCESTOP current job automatically when reaching the LOG_XXX_THRESHOLD.
#   - The SIGTERM signal would be sent twice resulting in an UNCLEAN shutdown, without the Scrapy stats dumped!
#   - The 'FORCESTOP' action would be executed if both of the 'STOP' and 'FORCESTOP' triggers are enabled.

# Note that the 'STOP' action and the 'FORCESTOP' action would STILL be executed even when the current time
# is NOT within the EMAIL_WORKING_DAYS and the EMAIL_WORKING_HOURS, though NO email would be sent.

LOG_CRITICAL_THRESHOLD = 0
LOG_CRITICAL_TRIGGER_STOP = False
LOG_CRITICAL_TRIGGER_FORCESTOP = False

LOG_ERROR_THRESHOLD = 0
LOG_ERROR_TRIGGER_STOP = False
LOG_ERROR_TRIGGER_FORCESTOP = False

LOG_WARNING_THRESHOLD = 0
LOG_WARNING_TRIGGER_STOP = False
LOG_WARNING_TRIGGER_FORCESTOP = False

LOG_REDIRECT_THRESHOLD = 0
LOG_REDIRECT_TRIGGER_STOP = False
LOG_REDIRECT_TRIGGER_FORCESTOP = False

LOG_RETRY_THRESHOLD = 0
LOG_RETRY_TRIGGER_STOP = False
LOG_RETRY_TRIGGER_FORCESTOP = False

LOG_IGNORE_THRESHOLD = 0
LOG_IGNORE_TRIGGER_STOP = False
LOG_IGNORE_TRIGGER_FORCESTOP = False


############################## System #########################################
# The default is False, set it to True to enable debug mode and the interactive debugger
# would be shown in the browser instead of the "500 Internal Server Error" page.
# Actually, it's not recommended to turn on debug mode, also no need,
# since its side effects includes creating two caching subprocess in the background.
DEBUG = False

# The default is False, set it to True to set the logging level to DEBUG for getting more
# information about how ScrapydWeb works, especially while debugging.
VERBOSE = False
