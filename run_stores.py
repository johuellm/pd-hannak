#!/usr/bin/env python

import sys, os, time, subprocess

machines = ['actraiser',  'aero-fighters',  'asterix',  
            'asteroids',  'aztarac',  'babypacman',  'batsugun',  
            'blandia',  'burgertime',  'burninrubber',  
            'captaincommando',  'cruisn-world',  'dangerousdungeons',  
            'darktower',  'deathrace',  'defender',  
            'dogyuun',  'donkeykong',  'doubledribble',  
            'exvania', 'finalfight',  'fireshark',  
            'funkyjet',  'galmedes',  'goldentee',  'gorf',  
            'gunbuster',  'hangon',  'holosseum',  
            'hook',  'jumpbug',  'junglehunt',  'kageki',  
            'kingofdragons',  'knuckleheads',  'kungfu',  'lastresort',  
            'legionnaire',  'lethalenforcers',  'mortalkombat',  
            'motofrenzy',  'mutantfighter',  'mysticriders',  
            'outrunners',  'pong',  
            'prosoccer',  'rastan',  'repulse',  
            'rezon',  'shogunwarriors',   'spacelords',  
            'tailgunner',  'tempest',  'trackandfield',  'turtles',  
            'ultratank', 
] # 'stargate',
machines.reverse()

# WORKING: staples, travelocity, newegg, macys, homedepot, cdw, orbitz, cheaptickets, expedia

usernames = {
  ## OMITED FROM PUBLIC DATA RELEASE
}

targets = {
  #'hotels': ['kayak', 'hotels', 'venere', 'booking', 'orbitz', 'priceline', 'expedia', 'cheaptickets', 'travelocity',],
  #'cars' : ['priceline', 'orbitz', 'expedia', 'cheaptickets', 'travelocity',],
  'ecommerce': ['local'] #['local', 'walmart', 'homedepot'], # ['sears', 'jcpenney', 'officedepot', 'bestbuy', 'walmart', 'cdw', 'staples', 'newegg', 'macys', 'homedepot',],
}

tests = {
  'browser': [('control', 'chrome', False, False),
              ('chrome', 'chrome', False, False),
              ('ie8', 'ie8', False, False),
              ('firefox', 'firefox', False, False),
              ('safari', 'safari', False, False),
              ('safari_osx', 'safari_osx', False, False),
              ('android', 'android', False, False)],
  'OS': [('control', 'win7', False, False),
         ('win7', 'win7', False, False),
         ('xp', 'xp', False, False),
         ('linux', 'linux', False, False),
         ('osx', 'osx', False, False)],
  'logged_out' : [('in', 'default', True, False),
                  ('control', 'default', False, False),
                  ('out', 'default', False, False),
                  ('clear', 'default', False, True)],
#  'referer': [('control', 'default', 'http://www.pricegrabber.com/'),
#              ('no-ref', 'default', None),
#              ('pricegrabber', 'default', 'http://www.pricegrabber.com/'),
#              ('retailmenot', 'default', 'http://www.retailmenot.com/'),
#              ('dealnews', 'default', 'http://dealnews.com/'),
#              ('coupons', 'default', 'http://www.coupons.com/coupon-codes/'),
#              ('twitter', 'default', 'http://twitter.com/'),
#              ('google', 'default', 'http://www.google.com/shopping/'),
#              ('facebook', 'default', 'http://facebook.com/')],
}

def open_tunnel(machine, port):
  print('Starting tunnel from 127.0.0.1:%i to %s' % (port, machine))
  p = subprocess.Popen(['ssh','-f','-N','-D','127.0.0.1:' + str(port),'-o','StrictHostKeyChecking=no',machine]);
  time.sleep(10);

def get_next_free_port(port):
  out = sys_execute(['lsof', '-i', '-P']);
  while port < 65536:
    if out.find(':' + str(port)) == -1: return port
    port += 1
  return 0

def sys_execute(command_array):
  try:
    out = subprocess.check_output(command_array, stderr=subprocess.STDOUT);
    return out
  except subprocess.CalledProcessError:
    return '';

if __name__ == '__main__':

  m = 0
  port = 8000
  ports = [8000]


  """# open tunnels
  for test, subjects in tests.items():
    for subject in subjects:
      port = get_next_free_port(port)
      open_tunnel(machines[m], port)
      ports.append(port);
      port += 1
      m += 1

  print('Opened', m, 'ssh tunnels')
  """


  for target, stores in targets.items():
    if not os.path.exists(target):
      os.makedirs(target)
        
    for store in stores:

      if not os.path.exists(target + '/' + store):
        os.makedirs(target + '/' + store)

      procs = []
      p = 0
      for test, subjects in tests.items():

        print('Running %s - %s - %s' % (target, store, test))

        # make directories for results
        resultdir = time.strftime(target + '/' + store + '/' + test + '//results_%Y_%m_%d_%H')
        if not os.path.exists(resultdir):
          os.makedirs(resultdir)
        for subject in subjects:
          subjectdir = resultdir + '/' + subject[0]
          if not os.path.exists(subjectdir):
            os.makedirs(subjectdir)
        
        # execute phantomjs
        for subject in subjects:
          name, useragent, login, clear = subject

          cmd = ['phantomjs',
                 '--web-security=false',
                 '--proxy=127.0.0.1:%8000',
                 '--proxy-type=socks5',
                 'store.js',
                 '--service=%s' % (target),
                 '--store=%s' % (store),
                 '--output=%s' % (resultdir + '/' + name),
                 '--user-agent=%s' % (useragent)]

          """
          if login:
            print(f"login: {store}")
            user, pw = usernames[store]
            cmd.append('--login=true')
            cmd.append('--username=%s' % (user))
            cmd.append('--password=%s' % (pw))
          
          
          if clear:
            cmd.append('--clear-cookies')
          else:
            cmd.append('--persist-cookies=cookies//%s_%s_%s_%s.cookie' % (target, store, test, name))
          """
          print(cmd)
          procs.append(subprocess.Popen(cmd, shell=True))
          p += 1
      
      start_time = time.time()
      while len(procs) > 0 and time.time() - start_time <= 520: # 42 minutes
        time.sleep(60)
        x = 0
        while x < len(procs):
          if procs[x].poll() is not None:
            procs.pop(x)
          else:
            x += 1

      if len(procs) > 0:
        print('Let the reaping begin')
        for proc in procs:
          if proc.poll() is None:
            print('Phantom is hung. Time to murder it')
            try: proc.kill()
            except:
              print('Problem killing', proc.pid)
          else: print('Phantom exited normally')

os.system('killall -9 ssh')

