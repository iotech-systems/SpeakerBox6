#!/usr/bin/env python3

import os
import flask, json
import multiprocessing as mp
import core.sb6server as sb6


app = flask.Flask(__name__)


@app.route("/")
def idx():
   return flask.render_template("index.html")


@app.route("/api/<card_id>/play/num/<num>")
def play_number(card_id, num):
   sb6s = sb6.SB6Server()
   if card_id == "all":
      sb6s.play_num_on_all_cards(num)
   else:
      pass
   return "OK"


@app.route("/api/<card_id>/play/folder/<fld>")
def play_folder(card_id, fld):
   sb6s = sb6.SB6Server()
   return sb6s.start_folder_player(card_id, fld)


@app.route("/api/<card_id>/stop/folder")
def stop_folder(card_id):
   return sb6.SB6Server.kill_folder_play(card_id)


# reads & checks state file in data folder
@app.route("/api/<card_id>/get-state")
def get_snd_crd_state(card_id):
   return sb6.SB6Server.get_snd_crd_state(card_id)


@app.route("/api/<card_id>/play/test")
def run_card_test(card_id):
   try:
      test_proc = mp.Process(target=sb6.SB6Server.run_card_test, args=(card_id,))
      test_proc.start()
      return f"PID:{test_proc.pid}"
   except Exception as ex:
      print(ex)


@app.route("/api/kill/test/<pid>")
def stop_card_test(pid: int):
   try:
      sb6.SB6Server.stop_card_test(pid)
      return "OK"
   except Exception as ex:
      print(ex)


@app.route("/api/<card_id>/volume/<level>")
def set_card_volume(card_id, level):
   sb6s = sb6.SB6Server()
   return sb6s.set_card_volume(card_id, level)


@app.route("/api/read/aplay-l")
def read_aplay_l():
   sb6s = sb6.SB6Server()
   buff = sb6s.sys_cmd_aplay_l()
   return buff


@app.route("/api/update/cards-conf", methods=["POST"])
def update_cards_conf():
   jsonBuff: str = flask.request.form["jsonBuff"]
   sb6s = sb6.SB6Server()
   buff = sb6s.update_cards_config(jsonBuff)
   return buff


@app.route("/api/get/music-folders")
def get_music_folders():
   folders = os.listdir("mp3s/music")
   return json.dumps(folders)


def start_web_server():
   print("starting web server")


# - - - entry point - - -
if __name__ == "__main__":
   # app.run(host='0.0.0.0', debug=True)
   start_web_server()
