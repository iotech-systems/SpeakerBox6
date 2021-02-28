

const sndCardState = {

   jsonBuff: null,

   update(jsBuff) {
      /* - - */
      jsBuff = JSON.parse(jsBuff);
      if (jsBuff.stateTag == undefined) {
         console.log(jsBuff);
         return;
      }
      sndCardState.jsonBuff = jsBuff;
      /* - - */
      switch(sndCardState.jsonBuff.stateTag) {
         case "FolderPlayer":
            sndCardState.onFolderPlayer();
            break;
         case "":
            break;
         default:
         break;
      }
      /* - - */
   },

   onFolderPlayer() {
      if (sndCardState.jsonBuff.sb6s_is_running) {
         $("#selMusicDirs").attr("disabled", "1");
         $("#selMusicDirs").val(sndCardState.jsonBuff.playingFolder);
         $("#btnPlayFolder").val(consts.FLD_STOP);
      } else {
         $("#selMusicDirs").removeAttr("disabled");
         $("#selMusicDirs").val(sndCardState.jsonBuff.playingFolder);
         $("#btnPlayFolder").val(consts.FLD_PLAY);
      }
   }

};
