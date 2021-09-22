#!/usr/bin/env python

import sys, os, time, subprocess

prefix = 'spend'

machines = ['54.82.140.247', '54.242.100.177', '54.242.130.234', '54.237.125.244', '54.198.95.176', '54.196.78.231']

targets = {
  'hotels' : ['expedia', 'hotels', 'priceline', 'travelocity'],
  'cars' : ['cheaptickets', 'expedia', 'orbitz', 'priceline', 'travelocity']   
}

accounts = {
  # OMITTED FROM PUBLIC DATA RELEASE
}

tests = {
  'spender': [('control', 'firefox'),
              ('control2', 'firefox'),
              ('buy_low', 'firefox'),
              ('buy_high', 'firefox'),
              ('click_low', 'firefox'),
              ('click_high', 'firefox')]
}

def open_tunnel(machine, port):
  print ('Starting tunnel from 127.0.0.1:%i to %s' % (port, machine))
  p = subprocess.Popen(['ssh','-f','-N','-D','127.0.0.1:' + str(port),'-o','StrictHostKeyChecking=no',
                        '-i', '../ancsaaa-keypair.pem', 'ubuntu@' + machine]);
  time.sleep(10);

def get_next_free_port(port):
  out = sys_execute(['lsof','-i','-P']);
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
  ports = {}

  # open tunnels
  for machine in machines:
    port = get_next_free_port(port)
    open_tunnel(machine, port)
    ports[machine] = port
    port += 1

  print( 'Opened', len(ports), 'ssh tunnels')

  for target, stores in targets.iteritems():
    if not os.path.exists(os.path.join(prefix, target)):
      os.makedirs(os.path.join(prefix, target))
        
    for store in stores:

      if not os.path.exists(os.path.join(prefix, target, store)):
        os.makedirs(os.path.join(prefix, target, store))

      procs = []
      for test, subjects in tests.iteritems():

        print('Running %s - %s - %s' % (target, store, test))

        # make directories for results
        resultdir = time.strftime(os.path.join(prefix, target, store, test, 'results_%Y_%m_%d_%H'))
        if not os.path.exists(resultdir):
          os.makedirs(resultdir)
        for subject in subjects:
          subjectdir = os.path.join(resultdir, subject[0])
          if not os.path.exists(subjectdir):
            os.makedirs(subjectdir)
        
        # execute phantomjs
        for subject in subjects:
          name, useragent = subject
          user, pw, ip = accounts[target][name]

          cmd = ['phantomjs',
                 '--web-security=false',
                 '--proxy=127.0.0.1:%i' % (ports[ip]),
                 '--proxy-type=socks5',
                 'store.js',
                 '--service=%s' % (target),
                 '--store=%s' % (store),
                 '--output=%s' % (os.path.join(resultdir, name)),
                 '--user-agent=%s' % (useragent),
                 '--login=true',
                 '--username=%s' % (user),
                 '--password=%s' % (pw),
                 '--persist-cookies=%s/cookies/%s_%s_%s_%s.cookie' % (prefix, target, store, test, name)
                 ]

          #print cmd
          procs.append(subprocess.Popen(cmd))

      start_time = time.time()
      while len(procs) > 0 and time.time() - start_time <= 2520: # 42 minutes
        time.sleep(60)
        x = 0
        while x < len(procs):
          if procs[x].poll() != None:
            procs.pop(x)
          else:
            x += 1

      if len(procs) > 0:
        print('Let the reaping begin')
        for proc in procs:
          if proc.poll() == None:
            print('Phantom is hung. Time to murder it')
            try: proc.kill()
            except:
              print('Problem killing', proc.pid)
          else: print('Phantom exited normally')

os.system('killall -9 ssh')

