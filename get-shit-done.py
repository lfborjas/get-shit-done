import sys, os, subprocess

def abort(e):
    print e
    sys.exit(0)

if len(sys.argv<=1):
    abort('Usage: %s [work | play]'%sys.argv[0])

if not os.geteuid() == 0:
    abort('Run this as root or GTFO')

site_list = [
	'reddit.com', 'forums.somethingawful.com', 'somethingawful.com',
	'digg.com', 'break.com', 'news.ycombinator.com',
	'infoq.com', 'bebo.com', 'twitter.com',
	'facebook.com', 'blip.com', 'youtube.com',
	'vimeo.com', 'delicious.com', 'flickr.com',
	'friendster.com', 'hi5.com', 'linkedin.com',
	'livejournal.com', 'meetup.com', 'myspace.com',
	'plurk.com', 'stickam.com', 'stumbleupon.com',
	'yelp.com', 'slashdot.com'
]

restart_daemon = 'service networking restart'
hosts = '/etc/hosts'
start,end = map(lambda s: "##%s-GET-SHIT-DONE"%s, ['START', 'END'])

action = sys.argv[1]

if action == 'work':
    with open(hosts, 'r+') as f:
        contents = f.read()
        if start in contents and end in contents:
            abort('Work mode already set')
        contents += """
            %(start)s
            %(banned)s
            %(end)s
        """%{
             'start': start, 
             'end': end,
             'banned': '\n'.join(['127.0.0.1\t%s\n127.0.0.1\twww.%s\n'%(s,s) for s in site_list])
             }
        f.write(contents)
        subprocess.call(restart_daemon, shell=True)

    
elif action == 'play':
    with open(hosts, 'r+') as f:
        c = f.read()
        if start in c and end in c:
            c = c.replace(c[c.find(start):c.find(end)], '')
            f.write(c)
            subprocess.call(restart_daemon, shell=True)
