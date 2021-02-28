
var html = {

   soundCardInfo(cardid, cardConf) {
      /* - - */
      let zid = `zid_${cardid}`,
         rid = `vid_${cardid}`,
         inc = `inc_${cardid}`,
         lbl = cardConf.userLbl,
         vol = cardConf.volume,
         chc = (cardConf.useInOrderCall == 1) ? "checked" : "",
         phold = "";
      /* - - */
      if (lbl == "Enter zone name") {
         phold = `${lbl} (max 16 chars)`;
         lbl = "";
      }
      /* - - */
      let htmlTxt = `<input type="text" id="${zid}" class="css-zid" value="${lbl}"` + 
            ` placeholder="${phold}" maxlength="16" />`,
         htmlRng = `<input type="range" id="${rid}" class="css-rid"step="2" min="40"` + 
            ` max="110" value="${vol}" />`,
         htmlCtrls = `<ctrl>Select Music Folder:&nbsp;<select id="selMusicDirs"></select>&nbsp;` + 
            `<input type="button" id="btnPlayFolder" scid="${cardid}" value="Play Folder" /></ctrl>` + 
            `<ctrl>Inc. In Order Callout:&nbsp;<input type="checkbox" id="${inc}" ${chc} /></ctrl>` +  
            `<ctrl><input type="button" id="btnPlayTest" scid="${cardid}" value="Play Test" /></ctrl>` + 
            `<ctrl><input type="button" id="btnSaveInfo" scid="${cardid}" value="Update" /></ctrl>` + 
            `<img id="btnCloseDetails" src="/static/imgs/btn-close.png" />`;
      /* - - */
      return `<div class="sound-card-details">` + 
         `<div>User Zone Name:&nbsp;${htmlTxt}</div>` + 
         `<div>Sound Volume:&nbsp;(40)&nbsp;${htmlRng}&nbsp;(110)</div>` + 
         `<div class="sc-controls">${htmlCtrls}</div>` + 
         `<div id="sndCardState" class="snd-card-state"></div></div>`;
      /* - - */ 
   },

   loadMusicFolders() {
      /* - - */
      let oneach = function(_, f) {
            $("#selMusicDirs").append(`<option value="${f}">${f}</option>`);
         };
      /* - - */
      $("#selMusicDirs").html(`<option value="NoFolder">NoFolder</option>`);
      $(app.musicFolders).each(oneach)
   }

};
