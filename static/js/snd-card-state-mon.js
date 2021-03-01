
const sndCardMonitor = {

   sndCardID: null,
   targetDivID: null,

   init(cardid, targetDivID) {
      sndCardMonitor.sndCardID = cardid;
      sndCardMonitor.targetDivID = targetDivID;
   },

   run() {
      sndCardMonitor.__run__();
      setInterval(sndCardMonitor.__run__, 1200);
   },

   __run__() {
      if (sndCardMonitor.sndCardID == null)
         return;
      let callurl= `/api/${sndCardMonitor.sndCardID}/get-state`;
      /* - - */
      $.get(callurl, (res) => {
            try {
               $(`#${sndCardMonitor.targetDivID}`).html(res);
               sndCardState.update(res);
            } catch(e) {
               console.log([e, res]);
            }
         });
   }

};
