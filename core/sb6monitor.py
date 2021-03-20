
import time
import psutil
import setproctitle
import core.defs as defs


class sb6monitor(object):

   proc_name: str

   @staticmethod
   def start(proc_name):
      sb6monitor.proc_name = proc_name
      sb6monitor.__main__()

   @staticmethod
   def __main__():
      # set proc name
      setproctitle.setproctitle(defs.PRC_NAME_SB6_MONITOR)
      while True:
         try:
            time.sleep(16.0)
            print("\tsb6monitor: __main__")
         except Exception as ex:
            pass
      # end main

   @staticmethod
   def __is_proc_running(self, proc_name):
      for proc in psutil.process_iter():
         pass
