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
        area: Math.round(area*1000)/1000.0, // in m2
        length: Math.round(length*1000)/1000.0, // in km
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
  },
  mounted() {
    this.setupLeafletMap();
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
