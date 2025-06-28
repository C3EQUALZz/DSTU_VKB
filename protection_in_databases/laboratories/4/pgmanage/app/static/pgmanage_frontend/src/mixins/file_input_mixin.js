import {
  allowedFileTypes,
  maxFileSizeInKB,
  maxFileSizeInMB,
  mimeTypeMap,
} from "../constants";
import { showToast } from "../notification_control";
import { emitter } from "../emitter";
import { tabsStore } from "../stores/stores_initializer";

export default {
  methods: {
    handleFileInputChange(e) {
      let fileType, fileExtension;
      const [file] = e.target.files;

      fileType = file.type === "" ? "" : file.type;

      if (fileType === "") {
        let splitName = file.name.split(".");
        fileExtension = splitName[splitName.length - 1].toLowerCase();

        fileType = mimeTypeMap[fileExtension] ?? "text/plain";
      }

      if (!allowedFileTypes.includes(fileType)) {
        showToast("error", `File with type '${fileType}' is not supported.`);
        return;
      }

      if (file.size > maxFileSizeInKB) {
        showToast(
          "error",
          `Please select a file that is ${maxFileSizeInMB}MB or less.`
        );
        return;
      }
      try {
        if (window.FileReader) {
          let reader = new FileReader();
          reader.onload = () => {
            emitter.emit(`${this.tabId}_copy_to_editor`, reader.result);
          };
          reader.readAsText(file);

          let selectedTab;
          if (this.$options.name === "SnippetTab") {
            let snippetPanel = tabsStore.tabs.find(
              (tab) => tab.name === "Snippets"
            );
            selectedTab = snippetPanel?.metaData?.selectedTab;
          } else {
            selectedTab = tabsStore.selectedPrimaryTab?.metaData?.selectedTab;
          }
          if (selectedTab) {
            selectedTab.name = file.name;
            selectedTab.metaData.editingFile = true;
          }
        }
      } catch (err) {
        showToast("error", err);
        e.preventDefault();
        e.stopPropagation();
      }
    },
  },
};
