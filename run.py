#!/usr/bin/env python3

import os
import flask, json
import setproctitle
import multiprocessing as mp
import core.sb6server as sb6s
import core.sb6monitor as sb6m
import core.defs as defs


app = flask.Flask(__name__)
setproctitle.setproctitle(defs.PRC_NAME_SB6_SERVER)


@app.route("/")
def idx():
   try:
      return flask.render_template("index.html")
   except Exception as ex:
      # pass to 500 page
      pass


@app.route("/api/<card_id>/play/num/<num>")
def play_number(card_id, num):
   sb6obj = sb6s.SB6Server()
   if card_id == "all":
      sb6obj.play_num_on_all_cards(num)
   else:
      pass
   return "OK"


@app.route("/api/<card_id>/play/folder/<fld>")
def play_folder(card_id, fld):
   sb6obj = sb6s.SB6Server()
   return sb6obj.start_folder_player(card_id, fld)


@app.route("/api/<card_id>/stop/folder")
def stop_folder(card_id):
   return sb6s.SB6Server.kill_folder_play(card_id)


# reads & checks state file in data folder
@app.route("/api/<card_id>/get-state")
def get_snd_crd_state(card_id):
   res_buff = sb6s.SB6Server.get_snd_crd_state(card_id)
   return flask.Response(response=res_buff, content_type="text/plain")


@app.route("/api/<card_id>/play/test")
def run_card_test(card_id):
   try:
      test_proc = mp.Process(target=sb6s.SB6Server.run_card_test, args=(card_id,))
      test_proc.start()
      return f"PID:{test_proc.pid}"
   except Exception as ex:
      print(ex)


@app.route("/api/<card_id>/stop/test")
def stop_card_test(card_id):
   try:
      sb6s.SB6Server.stop_card_test(card_id)
      return "OK"
   except Exception as ex:
      print(ex)


@app.route("/api/<card_id>/volume/<level>")
def set_card_volume(card_id, level):
   sb6obj = sb6s.SB6Server()
   return sb6obj.set_card_volume(card_id, level)


@app.route("/api/read/aplay-l")
def read_aplay_l():
   sb6obj = sb6s.SB6Server()
   buff = sb6obj.sys_cmd_aplay_l()
   return buff


@app.route("/api/update/cards-conf", methods=["POST"])
def update_cards_conf():
   jsonBuff: str = flask.request.form["jsonBuff"]
   sb6obj = sb6s.SB6Server()
   buff = sb6obj.update_cards_config(jsonBuff)
   return buff


@app.route("/api/get/music-folders")
def get_music_folders():
   folders = os.listdir("mp3s/music")
   return json.dumps(folders)


def start_app_server():
   try:
      # start monitor
      print("\n - - - starting app monitor - - -\n")
      args = (defs.PRC_NAME_SB6_SERVER,)
      p = mp.Process(target=sb6m.sb6monitor.start, args=args)
      p.start()
      print(f"\tmonitor pid: {p.pid}")
      # start app server
      print("\n - - - starting app server - - -\n")
      app.run(host='0.0.0.0', port=8000, debug=False)
      # - - -
   except Exception as ex:
      print(f"\n{ex}\n")


# - - - - - - entry point - - - - - -
if __name__ == "__main__":
   start_app_server()
