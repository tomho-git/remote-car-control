<template>
  <div id="app" class="noselect">
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
    <div class="messageContainer">
      Message Box:
      <div class="messageBox">
        <div class="textBox" v-html="messageList"></div>
      </div>
    </div>
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
        .err((err) => {
          this.addMessage("ERROR: " + err);
        });
    },
    addMessage(message) {
      if (this.lastTimeStamp != this.getCurrentTimeStamp()) {
        var messageWithTimeStamp =
          "<" + this.getCurrentTimeStamp() + "> " + message;
        if (this.messageList) {
          this.messageList = this.messageList + "\n" + messageWithTimeStamp;
        } else {
          this.messageList = messageWithTimeStamp;
        }
        this.lastTimeStamp = this.getCurrentTimeStamp()
      }
    },
    getCurrentTimeStamp() {
      return moment(new Date()).format("YYYY-MM-DD HH:mm:ss");
    },
  },
  mounted() {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
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
  font-size: 2.5vh;
  height: 30vh;
  width: 100%;
  white-space: pre-wrap;
  overflow: scroll;
}
.messageContainer {
  margin-top: 5vh;
  text-align: left;
}
.rotateButtons {
  display: flex;
  justify-content: space-between;
}
.imageDisableDrag {
  user-drag: none;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>
