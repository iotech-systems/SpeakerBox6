

const sndCardState = {

   jsonBuff: null,

   update(res) {
      try {
         /* - - */
         jsBuff = utils.getJsonObj(res);
         if (jsBuff == consts.NOT_JSON_STR) {
            return;
         }
         /* - - */
         sndCardState.jsonBuff = jsBuff;
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
      } catch(e) {
         console.log([e, jsBuff]);
      }
      /* - - */
   },

   onFolderPlayer() {
      /* - - */
      console.log(sndCardState.jsonBuff);
      let sel = `#${sndCardState.jsonBuff.soundCard} .snd-crd-status`;
      $(sel).text(`playing: ${sndCardState.jsonBuff.playingFolder}`);
      /* - - */
      if (sndCardState.jsonBuff.sb6s_is_running) {
         $("#selMusicDirs").attr("disabled", "1");
         $("#selMusicDirs").val(sndCardState.jsonBuff.playingFolder);
         $("#btnPlayFolder").val(consts.FLD_STOP);
         $("#btnPlayFolder").removeClass("un-busy").addClass("busy");   
      } else {
         $("#selMusicDirs").removeAttr("disabled");
         $("#selMusicDirs").val(sndCardState.jsonBuff.playingFolder);
         $("#btnPlayFolder").val(consts.FLD_PLAY);
         $("#btnPlayFolder").removeClass("busy").addClass("un-busy");
      }
      /* - - */
   }

};
