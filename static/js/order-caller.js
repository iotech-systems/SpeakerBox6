
const orderCaller = {

   selNumBoxID: null,
   sellCallHistID: null,
   callBuffArr: [],

   /* orderCaller.init("txtCallNumber", "callHistBox"); */
   init(nbox, chist) {
      orderCaller.selNumBoxID = `#${nbox}`;
      orderCaller.sellCallHistID = `#${chist}`;
      /* - - */
      $(orderCaller.selNumBoxID).on("keypress", orderCaller.onKeyPress);
   },

   onKeyPress(e) {
      if (e.key.toUpperCase() == "ENTER")
         orderCaller.callOrderNumber();
   },

   onEnterPress() {
   },

   sendToSpeakerBox() {

   },

   /* http://192.168.1.160:5000/api/all/play/num/55 */
   callOrderNumber() {
      orderCaller.disableInput();
      let num = $(orderCaller.selNumBoxID).val(),
         callNumUrl = `/api/all/play/num/${num}`;
      /* - - */
      fetch(callNumUrl).then(res => {
            /* - - */
            let num = $(orderCaller.selNumBoxID).val(),
               /* greb first time string */
               time = new Date().toTimeString().split(" ")[0],
               numFrame = html.callNumFrame(num, time);
            if (orderCaller.callBuffArr.length > 13)
               orderCaller.callBuffArr.shift();
            orderCaller.callBuffArr.push(numFrame);
            /* - - */
            tbuff = $("#callHistBox").html(orderCaller.callBuffArr);
            //$("#callHistBox").html(tbuff.trim());
            $(orderCaller.selNumBoxID).val("");
            /* delay to keep crazy posting from happening */
            setTimeout(() => {
                  orderCaller.enableInput();
               }, 560);
            /* - - */
         });
      /* - - */
   },

   disableInput() {
      $(orderCaller.selNumBoxID).attr("disabled", "1");
      $("#btnCallNumber").attr("disabled", "1");
   },

   enableInput() {
      $(orderCaller.selNumBoxID).removeAttr("disabled");
      $("#btnCallNumber").removeAttr("disabled");
   }

};
