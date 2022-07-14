<template>
  <q-page class="flex column flex-center">
    <h3>Informe do PPPoE</h3>
    <div class="username-input">
      <q-input class="input-username" v-model="text" type="text" placeholder="Username" />
    </div>
    <q-btn color="primary" icon="swap_vert" label="Buscar" @click="Teste" />

  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'App',
  components: {},
  created() {
    this.$socket.on('RunningTest', msg=>{
      console.log(msg)
    })
  },
  setup(){
    return{
      text:ref('')
    }
  },
  methods:{
    Teste(){
      this.$socket.emit('StartTest', this.text)
    }
  }
})
</script>
<style>
.username-input {
  background: -webkit-linear-gradient(rgb(211, 211, 211), rgb(185, 252, 237));
  padding-left: 1em;
  padding-right: 1em;
  border-radius: 7px;
  margin-bottom: 2em;

}
</style>


