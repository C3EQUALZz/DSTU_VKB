import 'vite/modulepreload-polyfill';
import 'bootstrap/scss/bootstrap.scss'
import './assets/css/font-poppins.css'
import './assets/css/font-ubuntu-mono.css'
import $ from 'jquery';
import 'daterangepicker'
import ace from 'ace-builds'
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-sql'
import 'ace-builds/src-noconflict/mode-pgsql'
import 'ace-builds/src-noconflict/mode-mysql'
import 'ace-builds/src-noconflict/mode-plsql'
import 'ace-builds/src-noconflict/mode-json';
import 'ace-builds/src-noconflict/mode-plain_text';
import 'ace-builds/src-noconflict/mode-xml';
import 'ace-builds/src-noconflict/ext-language_tools'
import 'ace-builds/src-noconflict/ext-searchbox'
import 'ace-builds/src-noconflict/worker-json';
import 'ace-builds/src-noconflict/worker-xml';
import "./ace_extras/ext-hoverlink.js"
import './ace_extras/themes/theme-omnidb.js';
import './ace_extras/themes/theme-omnidb_dark.js';
import './workspace'
import './components/postgresql_modals'
import './assets/scss/pgmanage.scss'
import omniURL from './ace_extras/themes/theme-omnidb.js?url'
import omniDarkURL from './ace_extras/themes/theme-omnidb_dark.js?url'
import extendedPgsqlUrl from "./ace_extras/mode-pgsql-extended.js?url";
import extendedMysqlUrl from "./ace_extras/mode-mysql-extended.js?url";
import workerJsonUrl from  'ace-builds/src-noconflict/worker-json.js?url';
import workerXmlUrl from  'ace-builds/src-noconflict/worker-xml.js?url';
import axios from 'axios'
import { getCookie } from './ajax_control.js';
import App from './App.vue'
import { createApp } from 'vue';
import ToastPlugin from 'vue-toast-notification';
import { setupLogger } from './logging/logger_setup.js';
import {
  settingsStore,
  pinia,
  tabsStore,
  connectionsStore,
  snippetsStore,
  utilityJobStore,
  dbMetadataStore,
  messageModalStore,
  cellDataModalStore,
  fileManagerStore,
  utilitiesMenuStore,
  commandsHistoryStore,
} from "./stores/stores_initializer.js";

window.jQuery = window.$ = $;
ace.config.setModuleUrl('ace/theme/omnidb', omniURL)
ace.config.setModuleUrl('ace/theme/omnidb_dark', omniDarkURL)
ace.config.setModuleUrl('ace/mode/pgsql_extended', extendedPgsqlUrl)
ace.config.setModuleUrl('ace/mode/mysql_extended', extendedMysqlUrl)
ace.config.setModuleUrl('ace/mode/json_worker', workerJsonUrl)
ace.config.setModuleUrl('ace/mode/xml_worker', workerXmlUrl)
ace.config.set("loadWorkerFromBlob", false)

axios.defaults.headers.common['X-CSRFToken'] = getCookie(v_csrf_cookie_name);
axios.defaults.baseURL = app_base_path;

const stores = [
  settingsStore,
  tabsStore,
  connectionsStore,
  snippetsStore,
  utilityJobStore,
  dbMetadataStore,
  messageModalStore,
  cellDataModalStore,
  fileManagerStore,
  utilitiesMenuStore,
  commandsHistoryStore,
];

document.addEventListener('auxclick', function(event) {
  if (event.button === 1) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    return false;
  }
});

document.addEventListener('auxclick', function(event) {
  if (event.button === 1) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    return false;
  }
});

settingsStore.getSettings().then(() => {
  const app = createApp(App);
  setupLogger(app, stores);
  if (__VITE_ENTERPRISE__) {
    import("@conditional/index").then(({ default: enterprisePlugin }) => {
      app.use(enterprisePlugin);
      app.use(ToastPlugin, {
        duration: 0,
      });
      app.use(pinia);
      app.mount("#app");
    });
  } else {
    app.use(ToastPlugin, {
      duration: 0,
    });
    app.use(pinia);
    app.mount("#app");
  }
});
