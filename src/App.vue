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
    };
  },
  methods: {
    moveForward() {
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=forward")
          .then((resp) => {
            console.log('ok')
            console.log(resp);
          })
          .catch((err) => {
            console.log('error')
            console.log(err);
          });
      }, 1000);
    },
    moveBackward(){
      this.wheelMotion = setInterval(() => {
        axios
          .get(process.env.VUE_APP_BACKEND_SERVER + "?car=backward")
          .then((resp) => {
            console.log(resp);
          })
          .catch((err) => {
            console.log(err);
          });
      }, 1000);
    },
    stopMotion() {
      clearInterval(this.wheelMotion);
      axios.get("http://192.168.4.1:8080/?car=stop")
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
.button{
  font-size: 10vh;
  border: transparent
}
</style>
