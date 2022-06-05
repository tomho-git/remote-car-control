<template>
  <div id="app" class="noselect allContainer">
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
    <el-dialog title="Tips" :visible.sync="dialogVisible" width="100%">
      <div>Latitude: {{ currentLocation.lat }}</div>
      <div>Longitude: {{ currentLocation.long }}</div>
      <div>Height: (in mm){{ currentLocation.height }}</div>
      <div>Accuracy: (in mm){{ currentLocation.accuracy }}</div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

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
    };
  },
  methods: {
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
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?gps=start")
        .then((resp) => {
          this.addMessage("Start Recording");
          this.isRecording = true;
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
        });
    },

    stopRecording() {
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?gps=end")
        .then((resp) => {
          this.addMessage("Stop Recording");
          this.isRecording = false;
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
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
            "<div><" + this.getCurrentTimeStamp() + "> " + message + '</div>';
        }
        if (this.messageList) {
          this.messageList = this.messageList + messageWithTimeStamp;
        } else {
          this.messageList = messageWithTimeStamp;
        }
        this.lastTimeStamp = this.getCurrentTimeStamp();
        this.scrolltoBottom();
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
      console.log("123456");
      axios
        .get(process.env.VUE_APP_BACKEND_SERVER + "?gps=latest")
        .then((resp) => {
          this.currentLocation = resp.data;
          this.dialogVisible = true;
        })
        .catch((err) => {
          this.addMessage("ERROR: " + err);
        });
    },
  },
  mounted() {},
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
::v-deep .el-button.is-round {
}
</style>
