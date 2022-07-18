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
      <div class="items-end bg-white">



        <q-card v-if="loading" class="center"
          style=" display: flex; justify-content: center; align-items: center; flex-direction: column;">
          <div class="q-pa-md column justify-center items-center content-center q-gutter-md">
            <q-spinner-ball align="center" class="bg-white" size="6em" />
            <div class="buscando" style="font-size: 2em; ">Buscando...</div>
          </div>


        </q-card>

        <q-card v-else class="bg-teal text-white  q-pa-md row items-start q-gutter-md ">



          <div class="test-container q-pa-md row items-end q-gutter-md">

            <div class="chartArea full-width row  justify-center items-center content-center shadow-10">
              <GChart type="AreaChart" :data="chartData" :options="chartOptions" :resizeDebounce="500" />
            </div>

            <div class="reasultArea row q-gutter-xs justify-evenly">
              <q-card class="my-card bg-green text-white col-5 shadow-10">
                <q-card-section>
                  <div class="text-h6">
                    <q-icon name="file_download" /> Download
                  </div>
                  <div class="text-subtitle3">Atual: {{ actualDownload }} Mbps</div>
                  <div class="text-subtitle3">Mínimo: {{ minDownload }} Mbps</div>
                  <div class="text-subtitle3">Máximo: {{ maxDownload }} Mbps</div>
                  <div class="text-subtitle3">Média: {{ mediaDownload }} Mbps</div>
                </q-card-section>
              </q-card>
              <q-card class="my-card bg-blue text-white col-5 shadow-10 ">
                <q-card-section>
                  <div class="text-h6">
                    <q-icon name="file_upload" /> Upload
                  </div>
                  <div class="text-subtitle3">Atual: {{ actualUpload }} Mbps</div>
                  <div class="text-subtitle3">Mínimo: {{ minUpload }} Mbps</div>
                  <div class="text-subtitle3">Máximo: {{ maxUpload }} Mbps</div>
                  <div class="text-subtitle3">Média: {{ mediaUpload }} Mbps</div>
                </q-card-section>
              </q-card>
            </div>
          </div>





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

      let hour = new Date().getHours()
      let minutes = new Date().getMinutes()
      let seconds = new Date().getSeconds()

      let srtHorario = `${hour}:${minutes}:${seconds}`

      this.loading = false
      console.log(msg)
      this.actualDownload = msg.download
      this.actualUpload = msg.upload

      this.minUpload = msg.minUpload
      this.minDownload = msg.minDownload

      this.maxUpload = msg.maxUpload
      this.maxDownload = msg.maxDownload

      this.mediaUpload = msg.mediaUpload
      this.mediaDownload = msg.mediaDownload

      this.chartData.push([srtHorario, msg.download, msg.upload])



    })
    this.$socket.on('ErrorTest', msg => {
      this.testArea = false
      this.$q.notify({
        type: 'warning',
        message: msg.message
      })
    })
    this.$socket.on('FinishTest', msg => {
      this.actualDownload = 0
      this.actualUpload = 0
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
      loading: ref(false),
      actualUpload: ref(null),
      actualDownload: ref(null),
      minUpload: ref(null),
      minDownload: ref(null),
      maxUpload: ref(null),
      maxDownload: ref(null),
      mediaUpload: ref(null),
      mediaDownload: ref(null)
    }
  },
  data() {
    return {

      chartData: [
        ['Tempo', 'Download', 'Upload'],
        ['12:22', 112, 60],
        ['12:21', 122, 66],
        ['12:24', 119, 69],
      ],
      chartOptions: {
        title: `Consumo do Cliente - ${this.text}`,
        legend: { position: 'bottom' },
        vAxis: { format: '# Mbps' },
        // chartArea: { width: '50%', height: '70%' },
        width: 500,
        height: 250,
        titleTextStyle: {
          fontSize: 14, // 12, 18 whatever you want (don't specify px)
          bold: true   // true or false
        }
      },

      UploadData: [],
      DownloadData: []
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

      this.chartData = [
        ['Tempo', 'Download', 'Upload']
      ]
      this.UploadData = []
      this.DownloadData = []

      this.chartOptions.title = `Consumo do Cliente - ${this.text}`

      this.$socket.emit('StartTest', { username: this.text, durationTime: durationTime })
    }
  },
}

)
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


.reasultArea {
  height: 100%;
  width: 100%;
}

.test-container {
  background: whitesmoke;
}

.chartArea {
  background: yellow;
}
</style>


