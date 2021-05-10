<template>
  <td class="cell" @click="strike">{{ current_mark }}</td>
</template>

<script>
export default {
  name: "Cell",

  components: {},

  data() {
    return {
      // enables the player to place a mark
      frozen: false,
    };
  },
  props: {
    name: {
      type: String,
    },
    // holds either X or O to be displayed in the td
    mark: {
      type: String,
      default: "",
    },
  },
  computed: {
    // helper property to get the non-active player
    current_mark: {
      get() {
        return this.mark;
      },
      set(newval) {
        return newval;
      },
    },
    is_marked: {
      get() {
        return this.current_mark != "-";
      },
      set(newval) {
        return newval;
      },
    },
  },
  watch: {},
  methods: {
    strike() {
      if (!this.is_marked) {
        // gets either X or O from the Grid component
        this.current_mark = this.$parent.activePlayer;
        //this.frozen = true

        // fires an event to notify the Grid component that a mark is placed
        Event.$emit("strike", this.name);
      }
    },
  },

  mounted() {
    Event.$on("freeze", () => console.log("freeze"));
    Event.$on("clearCell", () => {
      this.current_mark = "";

      this.frozen = false;
    });
  },
};
</script>
<style >
.cell {
  width: 33.333%;
  height: 90px;
  border: 6px solid #2c3e50;
  font-size: 3.5em;
  font-family: "Gochi Hand", sans-serif;
}

.cell:hover {
  background-color: #7f8c8d;
}

.cell::after {
  content: "";
  display: block;
}

.cell:first-of-type {
  border-left-color: transparent;
  border-top-color: transparent;
}

.cell:nth-of-type(2) {
  border-top-color: transparent;
}

.cell:nth-of-type(3) {
  border-right-color: transparent;
  border-top-color: transparent;
}

tr:nth-of-type(3) .cell {
  border-bottom-color: transparent;
}
</style>
