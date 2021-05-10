<template>
  <div>
    <v-app>
      <v-row class="pa-6">
        <v-col cols="4">
          <v-card max-width="600">
            <v-btn color="green" @click="addgame"> New Game</v-btn>
            <h2>Saved Games</h2>
            <v-list>
              <v-list-item-group
                v-model="model"
                active-class="border"
                color="indigo"
              >
                <v-list-item
                  v-for="(item, i) in games"
                  :key="i"
                  @click="game_selected(item)"
                >
                  <v-list-item-icon>
                    <v-icon v-text="item.icon"></v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title v-text="item.id"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-col>
        <v-col cols="8">
          <v-row class="ml-2">
          <div style="text-align: left">
          <p>Current Player: {{current_game_info.current_player}}</p>
          <p>Player1 (Computer): {{current_game_info.player1}}</p>
          <p>Player2 (You): {{current_game_info.player2}}</p>
          </div>
          </v-row>
          <div id="board" >
            <board :cells="cells" :current_game="current_game"
              :activePlayer="current_game_info.current_player"></board>
            <button class="delete_" @click="delete_">Delete</button>
          </div>
        </v-col>
      </v-row>
    </v-app>
  </div>
</template>

<script>
import Services from "./services/Services";
import Board from "./components/Board.vue";
export default {
  name: "App",

  components: {
    board: Board,
  },

  data: () => ({
    sidebarMenu: false,
    cells_string: "---------",
    cells: {
      1: "-",
      2: "-",
      3: "-",
      4: "-",
      5: "-",
      6: "-",
      7: "-",
      8: "-",
      9: "-",
    },
    current_game: {},
    games: [],
    current_game_info :{},
    model: 0,
  }),
  watch: {
    current_game() {
      this.cells = this.stringToCells(this.current_game.board);
    },
  },
  methods: {
    game_selected(game) {
      if (game == this.current_game) return;
      this.current_game = game;
      this.cells = this.stringToCells(game.board);
      this.get_game_info()
    },
    addgame() {
      let new_game = {
        board: "---------",
      };

      Services.add_game(new_game)
        .then((res) => {
          let url = res.data.location;
          Services.get_game_details_by_url(url)
            .then((data) => {
              let new_game = data.data;
              this.games.unshift(new_game);
              this.current_game = new_game;
              this.get_game_info()
            })
            .catch((error) => {
              let message = error.response.data.reason;
              this.$notification.warning(message);
            });
        })
        .catch((error) => {
          let message = error.response.data.reason;
          this.$notification.warning(message);
        });
    },
    get_games() {
      Services.get_all_games()
        .then((data) => {
          this.games = data.data;
          if (this.games.length > 0) {
            this.current_game = this.games[0];
            this.get_game_info()
          }
          else
          this.$notification.warning("in order to play, create new game!");
        })
        .catch((error) => {
          let message = error.response.data.reason;
          this.$notification.warning(message);
        });
    },
    get_game_info() {
      Services.get_game_info(this.current_game.id)
        .then((data) => {
          this.current_game_info = data.data
        })
        .catch((error) => {
          let message = error.response.data.reason;
          this.$notification.warning(message);
        });
    },
    delete_() {
      if (!this.current_game.id) {
        this.$notification.warning("choose a game to delete!");
        return;
      }
      Services.delete_game(this.current_game.id)
        .then((success) => {
          console.log(success);
          this.$notification.success("Game deleted successfully!");
          this.games = this.games.filter((x) => x != this.current_game);
          if (this.games.length > 0) this.current_game = this.games[0];
        })
        .catch((error) => {
          let message = error.response.data.reason;
          this.$notification.warning(message);
        });
    },
    updateGameBoard(game, new_board) {
      Services.update_game(game.id, { board: new_board })
        .then((data) => {
          this.current_game = data.data;
          this.get_game_info(game.id)
        })
        .catch((error) => {
          let message = error.response.data.reason;
          this.$notification.warning(message);
        });
    },

    cellsToString(cells) {
      let result = "";
      for (let i = 1; i < 10; i++) {
        result += cells[i.toString()];
      }
      return result;
    },
    stringToCells(str) {
      let cells = {};
      for (let i = 0; i < 9; i++) {
        cells[(i + 1).toString()] = str[i];
      }
      return cells;
    },
  },
  mounted() {
    Event.$on("strike", (cellNumber) => {
      console.log(cellNumber);
      if (this.current_game.status.toLowerCase() != "running") return;
      // sets either X or O in the clicked cell of the cells array
      let new_board = this.cellsToString(this.cells);
      this.updateGameBoard(this.current_game, new_board);
    });
    this.get_games();
  },
};
</script>
<style>
body {
  background-color: #fff;
  color: #fff;
  font-family: "Dosis", Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: 0px;
}

#board {
  max-width: 290px;
  color: #34495e;
}

h1 {
  text-transform: uppercase;
  font-weight: bold;
  font-size: 3em;
}

.delete_ {
  background-color: #e74c3c;
  color: #fff;
  border: 0px;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  font-family: "Dosis", Helvetica, sans-serif;
  font-size: 1.4em;
  font-weight: bold;
  margin: 0px;
  padding: 15px;
  width: 100%;
}

.delete_:hover {
  background-color: #c0392b;
  cursor: pointer;
}

.border {
  border: 2px dashed orange;
}
</style>