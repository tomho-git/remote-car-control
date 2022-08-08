<template>
  <div
    id="app"
    class="noselect allContainer"
    v-loading="isLoading"
    v-if="showControl"
  >
    <div>
      <button
        @mousedown="moveForward()"
        @mouseup="stopMotion()"
        @touchstart="moveForward()"
        @touchend="stopMotion()"
        class="noselect button"
      >
        <img
          style="width: 8vh"
          src="./assets/up-arrow.png"
          class="imageDisableDrag"
        />
      </button>
    </div>
    <div class="rotateButtons">
      <button
        @mousedown="rotateAntiClockwise()"
        @mouseup="stopMotion()"
        @touchstart="rotateAntiClockwise()"
        @touchend="stopMotion()"
        class="noselect button"
      >
        <img
          style="width: 8vh"
          src="./assets/anticlockwise.png"
          class="imageDisableDrag"
        />
      </button>
      <button
        @mousedown="rotateClockwise()"
        @mouseup="stopMotion()"
        @touchstart="rotateClockwise()"
        @touchend="stopMotion()"
        class="noselect button"
      >
        <img
          style="width: 8vh"
          src="./assets/clockwise.png"
          class="imageDisableDrag"
        />
      </button>
    </div>
    <div>
      <button
        @mousedown="moveBackward()"
        @mouseup="stopMotion()"
        @touchstart="moveBackward()"
        @touchend="stopMotion()"
        class="noselect button"
      >
        <img
          style="width: 8vh"
          src="./assets/down-arrow.png"
          class="imageDisableDrag"
        />
      </button>
    </div>
    <div class="Recording">
      <el-button
        @click="startRecording()"
        type="primary"
        round
        v-if="!isRecording"
        style="padding: 1.5vh 3vw"
        >Start Recording</el-button
      >
      <el-button
        @click="stopRecording()"
        type="danger"
        round
        v-if="isRecording"
        style="padding: 1.5vh 3vw"
        >Stop Recording</el-button
      >
      <el-button
        @click="showCurrentLocation()"
        type="info"
        round
        style="padding: 1.5vh 3vw"
        >Show Current Location</el-button
      >
    </div>
    <div class="messageContainer">
      Message Box:
      <div class="messageBox">
        <div class="textBox" v-html="messageList" id="messageTextBox"></div>
      </div>
    </div>
    <el-dialog
      title="Current Location"
      :visible.sync="dialogVisible"
      width="100%"
    >
      <div>Latitude: {{ currentLocation.lat }}</div>
      <div>Longitude: {{ currentLocation.long }}</div>
      <div>Height: (in mm){{ currentLocation.height }}</div>
      <div>Accuracy: (in mm){{ currentLocation.accuracy }}</div>
    </el-dialog>
  </div>
  <div v-else class="allContainer">
    <input type="file" ref="doc" @change="readFile()" />
    <!-- <div v-if="fileLatLong">{{ calculateArea() }}</div> -->
    <div id="mapContainer" class="mapContainer"></div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import * as turf from "@turf/turf";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

export default {
  name: "App",
  components: {},
  data: function () {
    return {
      wheelMotion: null,
      messageList: "",
      lastTimeStamp: "",
      isRecording: false,
      dialogVisible: false,
      currentLocation: {},
      isLoading: false,
      //for map
      showControl: false,
      center: [22.302711, 114.177216], //hong kong lat long
      fileContent: [],
      fileLatLong: [],
      mapObject: {},
      polygon: {},
    };
  },
  methods: {
    setupLeafletMap: function () {
      this.mapObject = L.map("mapContainer").setView(this.center, 13);
      L.tileLayer("http://{s}.google.com/vt?lyrs=s,h&x={x}&y={y}&z={z}", {
        maxZoom: 20,
        subdomains: ["mt0", "mt1", "mt2", "mt3"],
      }).addTo(this.mapObject);
    },
    addPolygon: function () {
      var latlngs = [this.fileLatLong];
      if (Object.keys(this.polygon).length == 0) {
        this.polygon = L.polygon(latlngs, { color: "red" })
          .addTo(this.mapObject)
          .bindPopup(
            "<div class='area'>area: " +
              this.calculateArea().area +
              "(m2)</div> <div class='length'>length: " +
              this.calculateArea().length +
              "(km)</div>"
          );
      } else {
        this.polygon.setLatLngs(latlngs);
      }
      this.mapObject.fitBounds(this.polygon.getBounds());
    },
    splitFileIntoLatLong() {
      this.fileLatLong = [];
      for (let i = 1; i < this.fileContent.length; i++) {
        var details = this.fileContent[i].split(",");
        if (details && details[1] && details[2]) {
          this.fileLatLong.push([details[1], details[2]]);
        }
      }
    },
    readFile() {
      this.file = this.$refs.doc.files[0];
      const reader = new FileReader();
      if (this.file.name.includes(".csv")) {
        reader.onload = (res) => {
          this.fileContent = res.target.result.split(/\r\n|\n/);
          this.splitFileIntoLatLong();
          this.addPolygon();
        };
        reader.onerror = (err) => console.log(err);
        reader.readAsText(this.file);
      } else {
        this.content = "check the console for file output";
        reader.onload = (res) => {
          console.log(res.target.result);
        };
        reader.onerror = (err) => console.log(err);
        reader.readAsText(this.file);
      }
    },
    calculateArea() {
      if (this.fileLatLong.length == 0)
        return {
          area: 0,
          length: 0,
        };
      //calculate area
      var polygon = turf.multiPolygon([[this.fileLatLong]]);
      var area = turf.area(polygon);
      var length = turf.length(polygon, { units: "kilometers" });
      return {
        area: Math.round(area * 1000) / 1000.0, // in m2
        length: Math.round(length * 1000) / 1000.0, // in km
      };
    },
    moveForward() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=forward")
          .then((resp) => {
            this.addMessage("Move backward success");
          })
          .catch((err) => {
            this.addMessage("ERROR: " + err);
          });
      }, 1000);
    },
    moveBackward() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=backward")
          .then((resp) => {
            this.addMessage("Move backward success");
          })
          .catch((err) => {
            this.addMessage("ERROR: " + err);
          });
      }, 1000);
    },
    rotateAntiClockwise() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=anticlockwise")
          .then((resp) => {
            this.addMessage("Rotate anti-clockwise success");
          })
          .catch((err) => {
            this.addMessage("ERROR: " + err);
          });
      }, 300);
    },
    rotateClockwise() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=clockwise")
          .then((resp) => {
            this.addMessage("Rotate clockwise success");
          })
          .catch((err) => {
            this.addMessage("ERROR: " + err);
          });
      }, 300);
    },
    stopMotion() {
      clearInterval(this.wheelMotion);
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?car=stop")
        .then((resp) => {
          this.addMessage("Stop success");
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
        });
    },
    startRecording() {
      this.isLoading = true;
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?gps=start")
        .then((resp) => {
          this.addMessage("Start Recording");
          this.isRecording = true;
          this.isLoading = false;
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
          this.isLoading = false;
        });
    },

    stopRecording() {
      this.isLoading = true;
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?gps=end")
        .then((resp) => {
          this.addMessage("Stop Recording");
          this.isRecording = false;
          this.isLoading = false;
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
          this.isLoading = false;
        });
    },
    addMessage(message) {
      if (this.lastTimeStamp != this.getCurrentTimeStamp()) {
        var messageWithTimeStamp = "";
        if (message.startsWith("ERROR:")) {
          messageWithTimeStamp =
            "<div style='color: red'>" +
            "<" +
            this.getCurrentTimeStamp() +
            "> " +
            message +
            "</div>";
        } else {
          messageWithTimeStamp =
            "<div><" + this.getCurrentTimeStamp() + "> " + message + "</div>";
        }
        if (this.messageList) {
          this.messageList = this.messageList + messageWithTimeStamp;
        } else {
          this.messageList = messageWithTimeStamp;
        }
        this.lastTimeStamp = this.getCurrentTimeStamp();
        setTimeout(() => {
          this.scrolltoBottom();
        }, 50);
      }
    },
    scrolltoBottom() {
      var textBox = document.getElementById("messageTextBox");
      textBox.scrollTop = textBox.scrollHeight;
    },
    getCurrentTimeStamp() {
      return moment(new Date()).format("YYYY-MM-DD HH:mm:ss");
    },
    showCurrentLocation() {
      this.isLoading = true;
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?gps=latest")
        .then((resp) => {
          this.currentLocation = resp.data;
          this.dialogVisible = true;
          this.isLoading = false;
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
          this.isLoading = false;
        });
    },
    checkmobile() {
      let check = false;
      (function (a) {
        if (
          /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(
            a
          ) ||
          /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
            a.substr(0, 4)
          )
        )
          check = true;
      })(navigator.userAgent || navigator.vendor || window.opera);
      return check;
    },
  },
  mounted() {
    this.setupLeafletMap();
    if(this.checkmobile){
      this.showControl = true; 
    }
  },
};
</script>

<style>
html {
  height: 100%;
}
body {
  height: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px 0;
  height: calc(100% - 60px);
}
.allContainer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-content: space-around;
  /* overflow: hidden; */
}
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
  supported by Chrome, Edge, Opera and Firefox */
}
.button {
  font-size: 10vh;
  border: transparent;
  padding: 0 1vh;
}
.messageBox {
  border: 1px solid black;
}
.textBox {
  font-size: 2vh;
  height: 30vh;
  width: 100%;
  white-space: pre-wrap;
  overflow: scroll;
}
.messageContainer {
  text-align: left;
}
.rotateButtons {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
  flex: 1 0 auto;
}
.imageDisableDrag {
  user-drag: none;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
.el-loading-mask {
  background: rgba(255, 255, 255, 0.7);
}
.mapContainer {
  height: 90vh;
  width: 100vw;
}
</style>
