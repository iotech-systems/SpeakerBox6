
/*
   author: owsiak, erik
   date: 25/02/2021   
*/

/* const FLD_PLAY = "Play Folder";
const FLD_STOP = "Stop Play"; */

const consts = {
   FLD_PLAY: "Play Folder",
   FLD_STOP: "Stop Play",
   NOT_JSON_STR: "NOT_JSON_STR"
};


const app = {

   musicFolders: null,
   cardsConfig: null,
   cardsStateFiles: [],
   cardsConfigUrl: "/static/data/cards-config.json",
   postCardsConfUrl: "/api/update/cards-conf",

   init() {
      /* - - */
      $(".sc-tab").on("click", app.onSoundCardTabClick);
      $("#btnCallNumber").on("click", orderCaller.callOrderNumber);
      /* - - */
      app.loadCardsConf();
      app.loadMusicFolders();
      orderCaller.init("txtCallNumber", "callHistBox");
      /* - - */
      sndCardMonitor.run();
      setInterval(() => {
            app.updateTabStatus();
         }, 2000);
   },

   updateZoneTabs() {
      /* - - */
      let oneach = function(_, tab) {
            try {
               let tabid = $(tab).attr("id"),
                  obj = app.cardsConfig[tabid];
               $(tab).find(".usr-lbl").text(obj.userLbl);
            } catch(e) {
               console.log(e);
            }
         };
      /* - - */
      $(".sc-tab").each(oneach);
   },

   onSoundCardTabClick() {
      /* check if sound card test is running */
      if (app.isCardTestRunning())
         return;
      /* - - */
      app.clearTabs();
      /* - - */
      $(this).addClass("tab-bg-color");
      app.loadSoundCardDetails(this);
   },

   loadSoundCardDetails(tab) {
      /* - - */
      let cardid = $(tab).attr("id"),
         cardConf = app.cardsConfig[cardid],
         buff = html.soundCardInfo(cardid, cardConf);
      /* - - */
      $("#soundCardInfo").html(buff);
      /* update music select */
      html.loadMusicFolders();
      /* add events */
      $("#btnPlayTest").off().on("click", app.onPlayStopCardTest);
      $("#btnSaveInfo").off().on("click", app.saveSoundCardInfo);
      $("#btnCloseDetails").off().on("click", app.closeSoundCardDetails);
      $("#btnPlayFolder").off().on("click", app.onPlayStopMusicFolderClick);
      /* - - */
      app.loadSoundCardStateFile(cardid);
      sndCardMonitor.init(cardid, "sndCardState");
      /* - - */
   },

   onPlayStopCardTest() {
      /* - - */
      let __btn__ = this,
         val = $(__btn__).val(),
         scid = $(__btn__).attr("scid");
      /* - - */
      switch(val) {
         case "Play Test":
            $(__btn__).val("Stop Test");
            app.playSoundCardTest(__btn__, scid);
            break;
         case "Stop Test":
            $(__btn__).val("Play Test");
            app.stopSoundCardTest(__btn__, scid);
            break;
         default:
            break;
      }
      /* - - */
   },

   playSoundCardTest(__btn__, card_id) {
      /* - - */
      let testUrl = `/api/${card_id}/play/test`;
      let ondone = function(res) {
            let pid = res.replace("PID:", "");
            $(__btn__).attr("testpid", pid);
         };
      /* start test */
      $.get(testUrl, ondone)
   },

   stopSoundCardTest(__btn__, card_id) {
      /* - - */
      let callUrl = `/api/${card_id}/stop/test`;
      let ondone = function(res) {
            if (res == "OK")
               $(__btn__).attr("testpid", "");
         };
      /* kill test */
      $.get(callUrl, ondone)
   },

   /* { "volume": "50%",
      "userLbl": "Enter zone name" } */
   saveSoundCardInfo() {
      /* - - */
      let scid = $(this).attr("scid"),
         useInOrderCall = ($(`#inc_${scid}`).is(":checked")) ? 1 : 0,
         userLbl = $(`#zid_${scid}`).val(),
         volume = $(`#vid_${scid}`).val();
      /* - - */
      app.cardsConfig[scid] = {useInOrderCall, volume, userLbl};
      app.postCardsConf();
      /* - - */
   },

   postCardsConf() {
      /* - - */
      let ondone = function(res) {
            if (res == "OK")
               app.loadCardsConf();
            /* - - */
            app.updateZoneTabs();
         };
      /* - - */
      let jsonBuff = JSON.stringify(app.cardsConfig);
      $.post(app.postCardsConfUrl, {jsonBuff}, ondone);
      /* - - */
   },

   loadCardsConf() {
      $.get(app.cardsConfigUrl, (res) => {
            app.cardsConfig = res;
            app.updateZoneTabs();
         });
   },

   closeSoundCardDetails() {
      /* - - */
      if (app.isCardTestRunning())
         return;
      /* - - */
      app.clearTabs();
      $("#soundCardInfo").html("");
      /* - - */
      sndCardMonitor.sndCardID = null;
   },

   clearTabs() {
      $(".sc-tab").each((_, t) => {
         $(t).removeClass("tab-bg-color");
      });
   },

   isCardTestRunning() {
      let pid = $("#btnPlayTest").attr("testpid");
      if ((pid != undefined) && (pid != "")) {
         alert("Please End Sound Card Test!");
         return true;
      } else {
         return false;
      }
   },

   loadMusicFolders() {
      let dirsUrl = "/api/get/music-folders"
      $.get(dirsUrl, (res) => {
            app.musicFolders = JSON.parse(res);
            console.log(app.musicFolders);
         });
   },

   onPlayStopMusicFolderClick() {
      /* - - */
      let __btn__ = this,
         card_id = $(this).attr("scid"),
         fld = $("#selMusicDirs").val();
      /* - - */
      if ($(this).val() == consts.FLD_PLAY) {
         let callurl = `/api/${card_id}/play/folder/${fld}`;
         $.get(callurl, (res) => {
               if (res.startsWith("PID:")) {
                  /* proc started */
                  $(__btn__).val(consts.FLD_STOP);
                  $(__btn__).removeClass("un-busy").addClass("busy");   
                  $(__btn__).attr("pid", res.replace("PID:", ""));
                  $("#selMusicDirs").attr("disabled", "1");
                  sndCardMonitor.sndCardID = card_id; 
               } else if (res.startsWith("ERROR.")){
                  alert(res.replace("ERROR.", ""));
               }
            });
      } else if ($(this).val() == consts.FLD_STOP) {
         $(__btn__).val(consts.FLD_PLAY);
         $(__btn__).removeClass("busy").addClass("un-busy");
         let callurl = `/api/${card_id}/stop/folder`;
         $.get(callurl, (res) => {
               if (res == "OK")
                  $("#selMusicDirs").removeAttr("disabled");
                  sndCardMonitor.sndCardID = null;
            });
      } else {
         console.log($(this).val());
      }
   },

   loadSoundCardStateFile(card_id) {
      let callurl = `/static/data/${card_id}_state.json`;
      $.get(callurl, (jobj) => {
            if (jobj.playingFolder) {
               $("#selMusicDirs").val(jobj.playingFolder);
               $("#selMusicDirs").attr("disabled", "1");
               $("#btnPlayFolder").val(FLD_STOP);   
            }
         });
   },

   /* this will need more work as the logic to inluced playing 
      folders or song lists */
   updateTabStatus() {
      /* - - */
      for (let card_id in app.cardsConfig) {
         let obj = app.cardsConfig[card_id],
            sel = `#${card_id} .snd-crd-status`;
         if (obj.useInOrderCall == 0) 
            continue;
         let msg = `OrderCalling; vol: ${obj.volume}%;`;
         $(sel).html(msg);
      }
   }

};


/* = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = */ 
/* on doc loaded */
window.addEventListener("DOMContentLoaded", (e) => {
   app.init();
});
