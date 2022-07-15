<template>
  <q-page class="flex column flex-center">
    <h3 style="color: #fff">Informe o usuário PPPoE</h3>
    <div class="username-input q-gutter-md">
      <q-input class="input-username" v-model="text" type="text" placeholder="Username" />
      <q-select standout="text-white" filled v-model="timeOfTest" :options="timesOfTest" label="Duração do teste" />
    </div>
    <q-btn color="primary" icon="swap_vert" label="Buscar" @click="Teste" />

  </q-page>


  <div>
    <q-dialog v-model="testArea" persistent transition-show="scale" transition-hide="scale">
      <div class="q-pa-md q-gutter-sm bg-teal">



        <q-card v-if="loading" class="center"
          style=" display: flex; justify-content: center; align-items: center; flex-direction: column;">
          <q-spinner-ball align="center" class="bg-teal none" size="6em" />

        </q-card>

        <q-card v-else class="bg-teal text-white">
          <div class="q-pa-md row items-start q-gutter-md">
            <q-card class="my-card bg-green text-white">
              <q-card-section>
                <div class="text-h6">Download</div>
                <div class="text-subtitle2">{{ actualDownload }} Mbps</div>
              </q-card-section>
            </q-card>
            <q-card class="my-card bg-blue text-white">
              <q-card-section>
                <div class="text-h6">Upload</div>
                <div class="text-subtitle2">{{ actualUpload }} Mbps</div>
              </q-card-section>
            </q-card>
          </div>
          <GChart type="AreaChart" :data="chartData" :options="chartOptions" :resizeDebounce="600" />




        </q-card>
        <q-btn flat label="OK" v-close-popup />
      </div>

    </q-dialog>
  </div>



</template>

<script>
import { defineComponent, ref } from 'vue'
import { GChart } from 'vue-google-charts'

export default defineComponent({
  name: 'App',
  components: { GChart },
  created() {
    this.$socket.on('RunningTest', msg => {
      this.loading = false
      console.log(msg)
      this.actualDownload = msg.download
      this.actualUpload = msg.upload
      this.chartData.push(['t', msg.download, msg.upload])

    })
    this.$socket.on('ErrorTest', msg => {
      this.testArea = false
      this.$q.notify({
        type: 'warning',
        message: msg.message
      })
    })
    this.$socket.on('FinishTest', msg => {
      this.actualDownload = null
      this.actualUpload = null
      this.$q.notify({
        type: 'positive',
        message: msg.message
      })
    })

  },
  setup() {
    return {
      text: ref(''),
      timeOfTest: ref('15 Segundos'),
      timesOfTest: ['15 Segundos', '30 Segundos', '45 Segundos'],
      testArea: ref(false),
      loading: ref(true),
      actualUpload: ref(null),
      actualDownload: ref(null),
      UploadData: ref(null),
      DownloadData: ref(null),
    }
  },
  data() {
    return {
      chartData: [
        ['Tempo', 'Download', 'Upload']
      ],
      chartOptions: {
        title: `Consumo do cliente`,
        legend: { position: 'bottom' },
        vAxis: { format: '# Mbps' }
      }
    }
  },
  methods: {
    Teste() {
      if (this.text == "" || this.timeOfTest == "") {
        this.$q.notify({
          type: 'negative',
          message: 'O Usuário não pode estar em branco'
        })
        return
      }


      let durationTime = this.timeOfTest.split(' ')[0]
      this.loading = true
      this.testArea = true

      this.actualUpload = null
      this.actualDownload = null
      this.UploadData = null
      this.DownloadData = null

      this.$socket.emit('StartTest', { username: this.text, durationTime: durationTime })
    }
  }
})
</script>
<style>
.username-input {
  background: -webkit-linear-gradient(rgb(211, 211, 211), rgb(185, 252, 237));
  padding-left: 1em;
  padding-right: 1.5em;
  padding-bottom: 1em;
  border-radius: 7px;
  margin-bottom: 2em;

}
</style>


