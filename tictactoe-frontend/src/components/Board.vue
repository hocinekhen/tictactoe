<template>
  <div>
    <div class="gameStatus" :class="current_game.status">
      {{ current_game.status }}
    </div>
    <table class="grid">
      <tr>
        <cell name="1" :mark="cells['1']"></cell>
        <cell name="2" :mark="cells['2']"></cell>
        <cell name="3" :mark="cells['3']"></cell>
      </tr>
      <tr>
        <cell name="4" :mark="cells['4']"></cell>
        <cell name="5" :mark="cells['5']"></cell>
        <cell name="6" :mark="cells['6']"></cell>
      </tr>
      <tr>
        <cell name="7" :mark="cells['7']"></cell>
        <cell name="8" :mark="cells['8']"></cell>
        <cell name="9" :mark="cells['9']"></cell>
      </tr>
    </table>
  </div>
</template>

<script>
import Cell from "./Cell.vue";
export default {
  name: "Board",

  components: {
    cell: Cell,
  },

  data() {
    return {
      // can be O or X
    };
  },
  props: {
    activePlayer: {
      type: String,
      default: "O",
    },
    // stores the placement of X and O in cells by their cell number
    cells: {
      type: Object,
      default: function () {
        return {
          1: "",
          2: "",
          3: "",
          4: "",
          5: "",
          6: "",
          7: "",
          8: "",
          9: "",
        };
      },
    },
    current_game: {
      type: Object,
      default: function () {
        return {
          status: "Running",
        };
      },
    },
  },
  computed: {
    // helper property to get the non-active player
    nonActivePlayer() {
      if (this.activePlayer === "O") {
        return "X";
      }

      return "O";
    },
  },
  watch: {},
  methods: {
    // changes the active player to the non-active player with the help of the nonActivePlayer computed property
    changePlayer() {
      console.log("change player");
      this.activePlayer = this.nonActivePlayer;
      console.log(this.activePlayer);
    },
  },

  mounted() {
    // listens for a strike made by the user on cell
    // it is called by the Cell component
    Event.$on("strike", (cellNumber) => {
      if (this.current_game.status.toLowerCase() != "running") return;
      // sets either X or O in the clicked cell of the cells array
      this.cells[cellNumber] = this.activePlayer;
      this.changePlayer();
    });
    Event.$on("gridReset", () => {
      Object.assign(this.$data, this.$options.data());
    });
  },
};
</script>
<style >
.grid {
  background-color: #34495e;
  color: #fff;
  width: 100%;
  border-collapse: collapse;
}

.gameStatus {
  margin: 0px;
  padding: 15px;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  background-color: #f1c40f;
  color: #fff;
  font-size: 1.4em;
  font-weight: bold;
}

.RUNNING {
  background-color: #f1c40f;
}

.X_WON,
.O_WON {
  background-color: #2ecc71;
}

.DRAW {
  background-color: #9b59b6;
}
</style>