<template>
  <div class="tab-pane" :id="`nav_explain_${tabId}`" role="tabpanel" :aria-labelledby="`nav_explain_tab_${tabId}`">
    <div class="explain-wrap pt-2">
      <div class="result-div">
        <template v-if="!query && !plan">
          <p class="lead text-center text-muted mt-5">
            Nothing to visualize. Please click Explain or Analyze button on the
            toolbar above.
          </p>
        </template>

        <template v-else>
          <pev2 class="h-100" :plan-source="plan" :plan-query="query" :key="reRenderCounter" />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { Plan } from "pev2";
export default {
  components: {
    pev2: Plan,
  },
  props: {
    tabId: String,
    plan: String,
    query: String,
  },
  data() {
    return {
      reRenderCounter: 0,
    };
  },
  watch: {
    plan: function () {
      this.reRenderCounter++;
    },
  },
  methods: {},
};
</script>

<style scoped>
.explain-wrap {
  height: 100%;
}

.result-div {
  height: 100%;
}
</style>
