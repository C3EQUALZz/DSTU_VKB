import { defineStore } from "pinia";

const useSnippetsStore = defineStore("snippets", {
  state: () => ({
    id: null,
    files: [],
    folders: [],
  }),
});

export { useSnippetsStore };
