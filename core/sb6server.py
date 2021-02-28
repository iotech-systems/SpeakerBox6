
import time
import os, sys, io, re
import json, random, psutil
import datetime as dt
import subprocess as sp
import multiprocessing as mp
import setproctitle
import core.sb6utils as sb6utils
import core.defs as defs


class SB6Server(object):

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def __init__(self):
      self.sc_table = {}
      self.sc_confs = {}
      self.load_sound_card_table()

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def get_cmd_arr(cmd):
      if cmd == "aplay-l":
         return ["aplay", "-l | grep USB"]

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def play_mp3_proc(card_id, mp3path):
      if not os.path.exists(mp3path):
         return f"fnf: {mp3path}"
      # -- do ---
      os.putenv("AUDIODEV", f"hw:{card_id}")
      os.system(f"play -q {mp3path}")

   @staticmethod
   def play_fld_proc(card_id: str, fld: str):
      try:
         setproctitle.setproctitle(f"{card_id}_ply_fld")
         utils = sb6utils.sb6Utils()
         path = f"{defs.MUSIC_ROOT}/{fld}"
         # -- do ---
         # mp3s in the folder
         mp3s = os.listdir(path)
         # set sound card for play cmd process
         os.putenv("AUDIODEV", f"hw:{card_id}")
         # - - - -
         sb6sPID = os.getpid()
         state = utils.new_state_object("FolderPlayer",
            card_id, "sb6s", sb6sPID)
         state["playingFolder"] = fld
         # - - - -
         while True:
            rid = random.randrange(0, len(mp3s), 1)
            track = f"{path}/{mp3s[rid]}"
            # update state json file
            state["playingTrack"] = track
            state["updateUtcDts"] = utils.utc_now()
            play = sp.Popen(["play", "-q", track])
            state["playPID"] = play.pid
            utils.new_state_file(card_id, state)
            ref_play = psutil.Process(play.pid)
            # wait on play
            while ref_play.status() != "zombie":
               time.sleep(0.66)
            play.kill()
            time.sleep(1.0)
      except Exception as ex:
         print(ex)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def get_snd_crd_state(card_id):
      try:
         state_file = f"{defs.RUNTIME_FLD}/{card_id}_state.json"
         if not os.path.exists(state_file):
            return f"STATE_FILE_NOT_FOUND: {state_file}"
         utils = sb6utils.sb6Utils()
         state = utils.get_state_object(card_id)
         # - - - -
         if "playPID" in state:
            utils.update_state_pid_info(state, "play")
         # - - - -
         if "sb6sPID" in state:
            utils.update_state_pid_info(state, "sb6s")
         # - - - -
         if "testPID" in state:
            utils.update_state_pid_info(state, "test")
         # - - - -
         return json.dumps(state)
      except Exception as e:
         return f"ERROR: {str(e)}"

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def sys_cmd_aplay_l(self):
      sys.stdout = iobuff = io.StringIO()
      os.system("aplay -l | grep USB")
      sys.stdout = sys.__stdout__
      return iobuff.getvalue()

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def play_num_on_all_cards(self, num):
      try:
         mp3_path = f"mp3s/nums/num{num}.mp3"
         procs = self.start_order_call_procs(mp3_path)
         # wait on mp3 procs
         for proc in procs:
            if not proc.is_alive():
               procs.remove(proc)
            time.sleep(0.1)
            if len(procs) == 0:
               break
         return "mp3 procs done!"
      except Exception as ex:
         print(ex)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def start_order_call_procs(self, fpath):
      arr = []
      with open(defs.SC_CONFS, "r") as f:
         buff = f.read()
      jobj = json.loads(buff)
      # - - - -
      for card_id in self.sc_table.keys():
         if int(jobj[card_id]["useInOrderCall"]) == 0:
            continue
         mp3proc = mp.Process(target=SB6Server.play_mp3_proc, args=(card_id, fpath))
         arr.append(mp3proc)
         mp3proc.start()
      return arr

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def start_folder_player(self, card_id, fld):
      # check if folder exists
      path = f"{defs.MUSIC_ROOT}/{fld}"
      if not os.path.exists(path):
         return f"ERROR.FolderNotFound: [{path}]"
      # check if folder has tracks
      files = os.listdir(path)
      if len(files) == 0:
         return f"ERROR.NoFiles: [{path}]"
      # - - - -
      mp3fldproc = mp.Process(target=SB6Server.play_fld_proc, args=(card_id, fld))
      mp3fldproc.start()
      return f"PID:{mp3fldproc.pid}"

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def set_card_volume(self, card_name, level: str):
      cmd = f"amixer -c {card_name} sset Speaker {level}%"
      buff = sp.check_output(cmd, shell=True)
      return buff

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   # card 0: SB6_P3 [USB Audio Device], device 0: USB Audio [USB Audio]
   def load_sound_card_table(self):
      patt = r"card.*([0-9]{1,2}):.*(SB6_P[0-9]{1,2})"
      resp = sp.Popen(["aplay", "-l"], stdout=sp.PIPE)
      lns = resp.stdout.readlines()
      for ln in lns:
         buff = ln.decode("utf-8").strip()
         if "USB Audio" not in buff:
            continue
         match = re.search(patt, buff)
         grps = match.groups()
         if len(grps) != 2:
            continue
         card_id = grps[0].strip()
         card_name = grps[1].strip()
         self.sc_table[card_name] = card_id
      # --- end for ---
      # print(self.sc_table)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def update_cards_config(self, jsonBuff):
      try:
         # - - - -
         utils = sb6utils.sb6Utils()
         utils.save_snd_cards_conf(jsonBuff)
         self.update_cards_volume(jsonBuff)
         # - - - -
         return "OK"
      except Exception as ex:
         print(ex)
         return "ERR"

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def update_cards_volume(self, jsonBuff):
      obj = json.loads(jsonBuff)
      for card_name in obj:
         vol = obj[card_name]["volume"]
         buff = self.set_card_volume(card_name, vol)
         print(buff)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def run_card_test(card_id):
      try:
         # - - - -
         utils = sb6utils.sb6Utils()
         proc_name = f"{card_id}_test"
         for p in psutil.process_iter():
            if p.name() == proc_name:
               msg = f"Process Exists: {proc_name}"
               utils.new_error_file(card_id, msg)
               print(fr"proc exists; kill it first!: {proc_name}")
               sys.exit(1001)
         # - - - -
         setproctitle.setproctitle(proc_name)
         utils = sb6utils.sb6Utils()
         testPID = os.getpid()
         state = utils.new_state_object("OrderCallerTester",
            card_id, "test", testPID)
         utils.new_state_file(card_id, state)
         # - - - -
         os.putenv("AUDIODEV", f"hw:{card_id}")
         for num in range(1, 100):
            mp3_path = f"mp3s/nums/num{num}.mp3"
            os.system(f"play -q {mp3_path}")
            state["lastOrderCalled"] = mp3_path
            state["lastTestCallUtcDts"] = utils.utc_now()
            utils.new_state_file(card_id, state)
            time.sleep(1.0)
         # - - - -
      except Exception as ex:
         print(ex)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def stop_card_test(pid: int):
      try:
         print(f"stop_card_test ~ pid: {pid}")
         utils = sb6utils.sb6Utils()
         utils.kill_pid(pid)
      except Exception as ex:
         print(ex)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   @staticmethod
   def kill_folder_play(card_id):
      try:
         utils = sb6utils.sb6Utils()
         buff = utils.get_state_file(card_id)
         if buff.startswith("NO_STATE_FILE"):
            return buff
         # - - - -
         jobj = json.loads(buff)
         utils.kill_pid(int(jobj["playPID"]))
         utils.kill_pid(int(jobj["sb6sPID"]))
         utils.rm_state_file(card_id)
         # - - - -
         return "OK"
      except Exception as ex:
         print(ex)
