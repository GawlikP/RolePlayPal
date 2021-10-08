import { createStore } from 'vuex'

export default createStore({
  state: {
    user: { 
      token: "",
      username: ""
    }
  },
  mutations: {
    logUser(state, dat) {
      state.user.token = dat.token
      state.user.username = dat.username
    }
  },
  actions: {
  },
  modules: {
   
  }
})
