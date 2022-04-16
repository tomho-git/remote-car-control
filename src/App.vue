<template>
  <div id="app">
    <button @mousedown="turnOn" @mouseup="turnOff"> test </button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  components: {
  },
  data: function () {
  return {
    ledOnTimer: null, 
  }
},
  methods:{
    turnOn(){
      this.ledOnTimer = setInterval(()=>{
        axios.get('http://192.168.1.8:8080/?light=on')
      .then(resp=>{
        console.log(resp)
      })
      .catch(err=>{
        console.log(err)
      })
      }, 100)
    }, 
    turnOff(){
      clearInterval(this.ledOnTimer);
    }
  }
}
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
</style>
