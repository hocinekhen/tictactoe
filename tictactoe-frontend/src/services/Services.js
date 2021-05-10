import http from "../http-common";

class Services {
  get_all_games() {
    return http.get("/api/v1/games");
  }


  get_game_details(game_id) {

    return http.get(`/api/v1/games/${game_id}`);
  }
  get_game_details_by_url(url) {

    return http.get(url);
  }
  add_game(game_body) {

    return http.post(`/api/v1/games`, game_body);
  }
  update_game(game_id, game_body) {

    return http.put(`/api/v1/games/${game_id}`, game_body);
  }
  delete_game(game_id) {

    return http.delete(`/api/v1/games/${game_id}`);
  }
  get_game_info(game_id) {

    return http.get(`/api/v1/game_info/?game_id=${game_id}`);
  }
}

export default new Services();
