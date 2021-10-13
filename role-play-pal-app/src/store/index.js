import { createStore } from 'vuex'

export default createStore({
  state: {
    user: { 
      token: "",
      username: "",
      isAuthenticated: false,
    }
  },
  mutations: {
    initializeStore(state) { 
      if (localStorage.getItem('token')) { 
          state.user.token = localStorage.getItem('token') 
          state.user.username = localStorage.getItem('username')
          state.user.isAuthenticated = true 
      } else {
          state.user.token = '' 
          state.user.isAuthenticated = false 
          state.user.username = ''
      }
    },
    logUser(state, dat) {
      state.user.token = dat.token
      state.user.username = dat.username
      localStorage.setItem('token', dat.token);
      localStorage.setItem('username', dat.username);
    }
  },
  actions: {
  },
  modules: {
   
  }
})
