
const utils = {

   timeNowStr() {
      return new Date().toTimeString().split(" ")[0];
   },

   getJsonObj(buff) {
      try {
         return JSON.parse(buff);
      } catch(e) {
         return consts.NOT_JSON_STR;
      }
   }

};
