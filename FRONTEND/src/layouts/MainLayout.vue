<template>
  <q-layout view="hHh lpR fFf">

    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title align="center" class="title">
          Monitoramento de consumo PPPoE
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>
<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'MainLayout',
  setup() {

  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@1,600&display=swap');

.title{
  font-family: 'Montserrat', sans-serif;
  font-size: 2em;

}
</style>
