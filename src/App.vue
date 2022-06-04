<template>
  <div id="app">
    <div>
      <button
        @mousedown="moveForward()"
        @mouseup="stopMotion()"
        @touchstart="moveForward()"
        @touchend="stopMotion()"
        class="noselect button"
      >
        ↑
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
        ↶
      </button>
      <button
        @mousedown="rotateClockwise()"
        @mouseup="stopMotion()"
        @touchstart="rotateClockwise()"
        @touchend="stopMotion()"
        class="noselect button"
      >
        ↷
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
        ↓
      </button>
    </div>
    <div class="messageContainer">
      Message Box:
      <div class="messageBox">
        <div class="textBox">{{ message }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "App",
  components: {},
  data: function () {
    return {
      wheelMotion: null,
      message: "this is test message",
    };
  },
  methods: {
    moveForward() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=forward")
          .then((resp) => {})
          .catch((err) => {});
      }, 1000);
    },
    moveBackward() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=backward")
          .then((resp) => {})
          .catch((err) => {});
      }, 1000);
    },
    rotateAntiClockwise() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=anticlockwise")
          .then((resp) => {})
          .catch((err) => {});
      }, 300);
    },
    rotateClockwise() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=clockwise")
          .then((resp) => {})
          .catch((err) => {});
      }, 300);
    },
    stopMotion() {
      clearInterval(this.wheelMotion);
      axios.get("http://192.168.4.1:8080/?car=stop");
    },
  },
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
}
.messageBox {
  border: 1px solid black;
}
.textBox {
  min-height: 30vh;
  width: 100%;
}
.messageContainer {
  margin-top: 5vh;
  text-align: left;
}
.rotateButtons {
  display: flex;
  justify-content: space-between;
}
</style>
