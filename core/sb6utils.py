
import os, io
import datetime as dt
import psutil, json
import core.defs as defs


class sb6Utils(object):

   def __init__(self):
      pass

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def __utc_now():
      return dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

   def utc_now(self):
      return sb6Utils.__utc_now()

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def kill_pid(self, pid: int):
      print(f"kill_pid: {pid}")
      if not pid in psutil.pids():
         return f"PID_NOT_FOUND: {pid}"
      os.system(f"kill -9 {pid}")

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def get_state_file(self, card_id: str) -> str:
      state_file = self.state_file_name(card_id)
      if not os.path.exists(state_file):
         return f"NO_STATE_FILE: {state_file}"
      with open(state_file, "r") as f:
         buff = f.read()
      return buff

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def new_state_file(self, card_id: str, state: dict):
      state_file = self.state_file_name(card_id)
      self.rm_state_file(state_file)
      with open(state_file, "w") as f:
         f.write(json.dumps(state))

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def new_error_file(self, card_id: str, error_msg: str):
      error_file = self.error_file_name(card_id)
      self.rm_file(error_file)
      with open(error_file, "w") as f:
         f.write(error_msg)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def rm_state_file(self, card_id: str) -> bool:
      state_file = self.state_file_name(card_id)
      if not os.path.exists(state_file):
         return True
      os.remove(state_file)
      if not os.path.exists(state_file):
         return True

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def rm_file(self, path: str) -> bool:
      try:
         if not os.path.exists(path):
            return True
         os.remove(path)
         if not os.path.exists(path):
            return True
      except:
         return False

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def state_file_name(self, card_id) -> str:
      return f"{defs.RUNTIME_FLD}/{card_id}_state.json"

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def error_file_name(self, card_id) -> str:
      return f"{defs.RUNTIME_FLD}/{card_id}_error.json"

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def get_state_object(self, card_id):
      buff = self.get_state_file(card_id)
      return json.loads(buff)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def new_state_object(self, tag, card_id, pidPrefix=None, pid=None):
      tmp = {"stateTag": f"{tag}", "soundCard": f"{card_id}",
         "createUtcDts": f"{self.utc_now()}"}
      if pidPrefix is not None and pid is not None:
         tmp[f"{pidPrefix}PID"] = int(pid)
      # - - - -
      return tmp

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def update_state_pid_info(self, state, pidPrefix):
      pidName = f"{pidPrefix}PID"
      pid = state[pidName]
      state[f"{pidPrefix}_is_running"] = False
      state[f"{pidPrefix}PID_found"] = False
      if psutil.pid_exists(pid):
         proc = psutil.Process(pid)
         state[f"{pidPrefix}_is_running"] = proc.is_running()
         state[f"{pidName}_found"] = True
